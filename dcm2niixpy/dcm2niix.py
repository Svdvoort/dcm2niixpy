import re
import os
from spython.main import Client
from typing import Dict, Union


class DCM2NIIX:
    def __init__(self) -> None:
        self.SINGULARITY_KEYWORD = "singularity"
        self.DOCKER_KEYWORD = "docker"
        self.root_singularity_url = "library://svdvoort/default/dcm2niix"
        self.version = "1.0.20210317"

        self.container_runner = self.SINGULARITY_KEYWORD
        self.singularity_url = self.root_singularity_url + ":" + self.version

        self.compression_level = 6
        self.adjacent_dicom = False

        self.options: Dict[str, str] = {}
        self.compress = False

    @property
    def compress(self) -> str:
        return self.options["-z"]

    @compress.setter
    def compress(self, compress_setting: Union[bool, str, int]) -> None:
        settings_conversion = {True: "y", False: "n", 3: "3"}
        if compress_setting in settings_conversion:
            compress_setting = settings_conversion[compress_setting]

        valid_settings = ["y", "o", "i", "n", "3"]
        if compress_setting not in valid_settings:
            raise TypeError(
                "Compress setting should be one of {valid_settings}, you passed {input}".format(
                    valid_settings=valid_settings,
                    input=compress_setting,
                ),
            )

        self.options["-z"] = compress_setting

    def convert(self, input_path: str, output_path: str = None, options: list = None):
        if output_path is None:
            output_path = input_path
        if options is None:
            options = []

        options = [*self.default_options, *options]
        command_line_args = [*options, "-o", "/output", "/input"]

        bindings = self._make_input_output_binding(input_path, output_path)

        output = Client.run(self.singularity_url, command_line_args, bind=bindings, stream=True)

        output_info = DCM2NIIX_OUTPUT()
        output_info.parse_output(output)
        output_info.output_path = os.path.join(output_path, output_info.file_name)

        return output_info

    def _make_input_output_binding(self, input_path: str, output_path: str) -> list:
        return [input_path + ":/input", output_path + ":/output"]


class DCM2NIIX_OUTPUT:
    def __init__(self):
        self.converted_regex = "Convert (\d+) DICOM as ([^\s]+) \((\d+x\d+x\d+x\d+)\)"
        self.warning_regex = "Warning: (.*)"

        self.image_shape = None
        self.warnings = []
        self.file_name = None
        self.output_path = None
        self.n_slices = None
        self.no_direction = False

    def parse_output(self, output):
        for i_line in output:
            i_line = i_line.strip()
            print(i_line)

            self._parse_converted_info(i_line)
            self._parse_warning(i_line)

    def _parse_converted_info(self, info_line):
        converted_info = re.search(self.converted_regex, info_line)
        if converted_info:
            self.n_slices = converted_info.group(1)
            self.output_path = os.path.normpath(converted_info.group(2) + ".nii.gz")
            self.file_name = os.path.basename(self.output_path)
            image_shape = converted_info.group(3).split("x")
            image_shape = [int(i_image_shape) for i_image_shape in image_shape]
            self.image_shape = image_shape

    def _parse_warning(self, info_line):
        warnings = re.search(self.warning_regex, info_line)
        if warnings:
            warning = warnings.group(1)
            if (
                warning
                == "Unable to determine slice direction: please check whether slices are flipped"
            ):
                self.no_direction = True
            self.warnings.append(warning)

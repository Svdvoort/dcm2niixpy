import re
import os
from spython.main import Client


class DCM2NIIX:
    def __init__(self, default_options: list = None) -> None:
        self.root_singularity_url = "library://svdvoort/default/dcm2niix"
        self.version = "1.0.20210317"
        self.singularity_url = self.root_singularity_url + ":" + self.version
        if default_options is None:
            self.default_options = []
        else:
            self.default_options = default_options

        self.compression_level = 6
        self.adjacent_dicom = False

        # self.bids_sidecar = False
        # self.anonymize_bids = False
        # self.comment = None
        # self.directory_search_depth = 5
        # self.export_as_nrrd = False
        # self.filename = "%f_%p_%t_%s"
        # self.generate_defaults = False
        # self.ignore_derived = False
        # self.scale_16_bit = False
        # self.merge_2D = False

        # self.compress = False

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

    @property
    def compress(self):
        self._compress = True

    @compress.setter
    def compress(self, compress_setting: bool):
        if not isinstance(compress_setting, bool):
            raise TypeError(
                "Compress setting should be a boolean, you passed a {input_type}".format(
                    input_type=type(compress_setting)
                )
            )


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

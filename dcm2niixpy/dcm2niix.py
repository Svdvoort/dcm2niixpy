import os
import re
import shutil

from typing import Dict
from typing import Union

import spython.utils

from spython.main import Client


class DCM2NIIX:
    def __init__(
        self,
        version: str,
        container_backend="singularity",
        download: bool = False,
        download_folder: str = None,
    ) -> None:
        """
        Initialize the DCM2NIIX object.

        Args:
            container_backend (str, optional): Either "docker" or "singularity". Defaults to "singularity".
            version (str): Docker tag of version to use. Defaults to None.
            download (bool, optional): Whether to download the container instead of pulling and running everytime. Defaults to False.
            download_folder (str, optional): Location to download the container to. Defaults to None.
        """

        self.SINGULARITY_KEYWORD = "singularity"
        self.DOCKER_KEYWORD = "docker"
        self.SINGULARITY_ROOT_URL = "docker://svdvoort/dcm2niix"
        self.DOCKER_ROOT_URL = "svdvoort/dcm2niix"

        # TODO check whether the version is actually able for use
        self.version = version

        self.container_backend = container_backend
        self.container_url = self._construct_container_url()
        self.download_container = download
        self.download_folder = download_folder
        self.download_name = None
        if self.download_container:
            self.download_name = "dcm2niix_" + self.version + ".sif"
            self._download_container()

        self.options: Dict[str, str] = {}

        self.compression_level = 6
        self.adjacent_dicoms = False
        self.bids_sidecar = True
        self.anonymize_bids_sidecar = True
        self.directory_search_depth = 5
        self.export_as_nrrd = False
        self.filename = "%f_%p_%t_%s"
        self.generate_defaults = False
        self.ignore_derived = False
        self.losslessly_scale = False
        self.merge_2d_slices = "auto"
        self.rename = False
        self.single_file_mode = False
        self.private_text_notes = False
        self.verbose = 0
        self.conflict_write_behavior = 2
        self.crop_3D = False
        self.byte_order = "o"
        self.progress = False

        self.compress = False

    ######
    # Container functions
    ######

    def _check_singularity_installation(self) -> bool:
        """
        Check whether the singularity installation is available.

        Returns:
            bool: True if singularity is installed
        """
        return spython.utils.check_install()

    def _construct_container_url(self) -> str:
        if self.container_backend == self.SINGULARITY_KEYWORD:
            return self.SINGULARITY_ROOT_URL + ":" + self.version
        elif self.container_backend == self.DOCKER_KEYWORD:
            return self.DOCKER_ROOT_URL + ":" + self.version
        else:
            return ""

    @property
    def container_backend(self) -> str:
        """
        Get the container backend.

        Returns:
            str: Either "docker" or "singularity".
        """
        return self._container_backend

    @container_backend.setter
    def container_backend(self, container_backend: str) -> None:
        """
        Set the container backend.

        Args:
            container_backend (str): Either "docker" or "singularity".

        Raises:
            NotImplementedError: If not docker or singularity.
            OSError: If using a backend that is not installed.
        """
        if container_backend not in [self.DOCKER_KEYWORD, self.SINGULARITY_KEYWORD]:
            raise NotImplementedError(
                "Container backend should be either 'docker' or 'singularity'. You passed {input}".format(
                    input=container_backend
                )
            )

        if container_backend == self.SINGULARITY_KEYWORD:
            # Check whether singularity is installed locally
            has_singularity = self._check_singularity_installation()
            if not has_singularity:
                raise OSError(
                    "You have attempted to run with 'singularity' container backend, but singularity is not installed"
                )
            else:
                self._container_backend = self.SINGULARITY_KEYWORD
        elif container_backend == self.DOCKER_KEYWORD:
            has_docker = shutil.which(self.DOCKER_KEYWORD) is not None
            if not has_docker:
                raise OSError(
                    "You have attempted to run with 'docker' container backend, but docker is not installed"
                )
            else:
                self._container_backend = self.DOCKER_KEYWORD

    def _download_container(self) -> None:
        if self.download_container:
            if not os.path.exists(os.path.join(self.download_folder, self.download_name)):
                Client.pull(
                    image=self.container_url,
                    pull_folder=self.download_folder,
                    ext="sif",
                    name=self.download_name,
                )

    ######
    # Helper functions
    #####
    def _convert_settings(
        self, conversion_index: dict, setting: Union[str, bool, int]
    ) -> Union[str, bool, int]:
        """
        Go from internal settings to the settings that are passed to the dcm2niix command.

        Args:
            conversion_index (dict): Dictionary with the required conversions.
            setting (Union[str, bool, int]): The setting to convert.

        Returns:
            Union[str, bool, int]: Converted setting.
        """
        if setting in conversion_index:
            return conversion_index[setting]
        else:
            return setting

    def _check_valid_setting(
        self, setting_name: str, valid_settings: list, setting: Union[str, bool, int]
    ):
        """
        Check whether a setting is valid.

        Args:
            setting_name (str): _description_
            valid_settings (list): _description_
            setting (_type_): _description_

        Raises:
            ValueError: _description_
        """
        if setting not in valid_settings:
            err_msg = "{setting_name} setting should be one of '{valid_settings}', you passed '{input}'".format(
                setting_name=setting_name,
                valid_settings=", ".join(valid_settings),
                input=setting,
            )

            raise ValueError(err_msg)

    def _check_valid_setting_type(
        self, setting_name: str, valid_setting_types: list, setting_type: type
    ):
        """
        Check whether a certain setting has the valid type for the setting.

        Args:
            setting_name (str): Name of the setting.
            valid_setting_types (list): Which types are valid for that setting
            setting_type (type): Type of the setting.

        Raises:
            TypeError: If the setting type is not valid.
        """
        if setting_type not in valid_setting_types:
            valid_setting_types = [
                i_valid_setting.__name__ for i_valid_setting in valid_setting_types
            ]
            err_msg = "{setting_name} setting should be one of '{valid_types}', you passed an argument with type '{input_type}'".format(
                setting_name=setting_name,
                valid_types=", ".join(valid_setting_types),
                input_type=setting_type.__name__,
            )

            raise TypeError(err_msg)

    #########
    ## Options
    #########

    @property
    def compression_level(self) -> int:
        """
        gz compression level (1=fastest, 9=smallest)

        Returns:
            int: compression level
        """
        return int(self.options["compression_level"])

    @compression_level.setter
    def compression_level(self, setting: Union[str, int] = 6) -> None:
        """
        Set the gz compression level, (1=fastest, 9=smallest)

        Args:
            setting (Union[str, int], optional): The compression level. Defaults to 6.
        """
        setting_name = "Compression level"
        settings_conversion = {
            0: "0",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
        }
        valid_setting_types = [str, int]

        valid_settings = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self._check_valid_setting_type(setting_name, valid_setting_types, type(setting))

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting(setting_name, valid_settings, setting)

        self.options["compression_level"] = setting

    @property
    def adjacent_dicoms(self) -> bool:
        "Adjacent DICOMs (images from same series always in same folder) for faster conversion (n/y, default n)"
        settings_conversion = {"y": True, "n": False}
        return self._convert_settings(settings_conversion, self.options["-a"])

    @adjacent_dicoms.setter
    def adjacent_dicoms(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]
        valid_setting_types = [str, bool]
        setting_name = "Adjacent DICOM"

        self._check_valid_setting_type(setting_name, valid_setting_types, type(setting))

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting(setting_name, valid_settings, setting)

        self.options["-a"] = setting

    @property
    def bids_sidecar(self) -> str:
        "BIDS sidecar (y/n/o [o=only: no NIfTI], default y)"
        return self.options["-b"]

    @bids_sidecar.setter
    def bids_sidecar(self, setting: Union[str, bool]):
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n", "o"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("BIDS sidecar", valid_settings, setting)

        self.options["-b"] = setting

    @property
    def anonymize_bids_sidecar(self) -> str:
        "anonymize BIDS (y/n, default y)"
        return self.options["-ba"]

    @anonymize_bids_sidecar.setter
    def anonymize_bids_sidecar(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Anonymize BIDS sidecar", valid_settings, setting)

        self.options["-ba"] = setting

    @property
    def comments_in_aux(self) -> str:
        "comment stored in NIfTI aux_file (provide up to 24 characters e.g. '-c first_visit')"
        if "-c" in self.options:
            return self.options["-c"]
        else:
            return None

    @comments_in_aux.setter
    def comments_in_aux(self, setting: str) -> None:
        self.options["-c"] = setting

    @property
    def directory_search_depth(self) -> str:
        "directory search depth. Convert DICOMs in sub-folders of in_folder? (0..9, default 5)"
        return self.options["-d"]

    @directory_search_depth.setter
    def directory_search_depth(self, setting: Union[str, int]) -> None:
        settings_conversion = {
            0: "0",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
        }
        valid_settings = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Directory search depth", valid_settings, setting)

        self.options["-d"] = setting

    @property
    def export_as_nrrd(self) -> str:
        "export as NRRD instead of NIfTI (y/n, default n)"
        return self.options["-e"]

    @export_as_nrrd.setter
    def export_as_nrrd(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Export as NRRD", valid_settings, setting)

        self.options["-e"] = setting

    @property
    def filename(self) -> str:
        "filename (%a=antenna (coil) name, %b=basename, %c=comments, %d=description, %e=echo number, %f=folder name, %i=ID of patient, %j=seriesInstanceUID, %k=studyInstanceUID, %m=manufacturer, %n=name of patient, %o=mediaObjectInstanceUID, %p=protocol, %r=instance number, %s=series number, %t=time, %u=acquisition number, %v=vendor, %x=study ID; %z=sequence name; default '%f_%p_%t_%s')"
        return self.options["-f"]

    @filename.setter
    def filename(self, setting: str) -> None:
        self.options["-f"] = setting

    @property
    def generate_defaults(self) -> str:
        "generate defaults file (y/n/o/i [o=only: reset and write defaults; i=ignore: reset defaults], default n)"
        return self.options["-g"]

    @generate_defaults.setter
    def generate_defaults(self, setting) -> str:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n", "o", "i"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Generate defaults", valid_settings, setting)

        self.options["-g"] = setting

    @property
    def ignore_derived(self) -> str:
        "ignore derived, localizer and 2D images (y/n, default n)"
        return self.options["-i"]

    @ignore_derived.setter
    def ignore_derived(self, setting) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Ignore derived", valid_settings, setting)

        self.options["-i"] = setting

    @property
    def losslessly_scale(self) -> str:
        "losslessly scale 16-bit integers to use dynamic range (y/n/o [yes=scale, no=no, but uint16->int16, o=original], default n)"
        return self.options["-l"]

    @losslessly_scale.setter
    def losslessly_scale(self, setting) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n", "o"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Losslessly scale", valid_settings, setting)

        self.options["-l"] = setting

    @property
    def merge_2d_slices(self) -> str:
        "merge 2D slices from same series regardless of echo, exposure, etc. (n/y or 0/1/2, default 2) [no, yes, auto]"
        return self.options["-m"]

    @merge_2d_slices.setter
    def merge_2d_slices(self, setting) -> None:
        settings_conversion = {True: "y", False: "n", 0: "0", 1: "1", 2: "2", "auto": "2"}
        valid_settings = ["y", "n", "0", "1", "2"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Merge 2D slices", valid_settings, setting)

        self.options["-m"] = setting

    @property
    def convert_only_this_crc(self) -> str:
        "only convert this series CRC number - can be used up to 16 times (default convert all)"
        if "-n" in self.options:
            return self.options["-n"]
        else:
            return None

    @convert_only_this_crc.setter
    def convert_only_this_crc(self, setting) -> None:
        self.options["-n"] = setting

    @property
    def output_directory(self) -> None:
        "output directory (omit to save to input folder)"
        if "-o" in self.options:
            return self.options["-o"]
        else:
            return None

    @output_directory.setter
    def output_directory(self, setting: str) -> None:
        if not os.path.exists(setting):
            os.makedirs(setting)
        self.options["-o"] = setting

    @property
    def philips_precise_float_scaling(self) -> str:
        "Philips precise float (not display) scaling (y/n, default y)"
        return self.options["-p"]

    @philips_precise_float_scaling.setter
    def philips_precise_float_scaling(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Philips precise float scaling", valid_settings, setting)

        self.options["-p"] = setting

    @property
    def rename(self) -> str:
        "rename instead of convert DICOMs (y/n, default n)"
        return self.options["-r"]

    @rename.setter
    def rename(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Rename", valid_settings, setting)

        self.options["-r"] = setting

    @property
    def single_file_mode(self) -> str:
        "single file mode, do not convert other images in folder (y/n, default n)"
        return self.options["-s"]

    @single_file_mode.setter
    def single_file_mode(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Single file mode", valid_settings, setting)

        self.options["-s"] = setting

    @property
    def private_text_notes(self) -> str:
        "text notes includes private patient details (y/n, default n)"
        return self.options["-t"]

    @private_text_notes.setter
    def private_text_notes(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Private text notes", valid_settings, setting)

        self.options["-t"] = setting

    @property
    def verbose(self) -> str:
        "verbose (n/y or 0/1/2, default 0) [no, yes, logorrheic]"
        return self.options["-v"]

    @verbose.setter
    def verbose(self, setting: Union[str, bool, int]) -> None:
        settings_conversion = {True: "y", False: "n", 0: "0", 1: "1", 2: "2"}
        valid_settings = ["y", "n", "0", "1", "2"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Verbose", valid_settings, setting)

        self.options["-v"] = setting

    @property
    def conflict_write_behavior(self) -> str:
        "write behavior for name conflicts (0,1,2, default 2: 0=skip duplicates, 1=overwrite, 2=add suffix)"
        return self.options["-w"]

    @conflict_write_behavior.setter
    def conflict_write_behavior(self, setting: Union[str, int]) -> None:
        settings_conversion = {0: "0", 1: "1", 2: "2"}
        valid_settings = ["0", "1", "2"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Conflict write behavior", valid_settings, setting)

        self.options["-w"] = setting

    @property
    def crop_3D(self) -> str:
        "crop 3D acquisitions (y/n/i, default n, use 'i'gnore to neither crop nor rotate 3D acquistions)"
        return self.options["-x"]

    @crop_3D.setter
    def crop_3D(self, setting: Union[str, bool]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n", "o"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Crop 3D acquisitions", valid_settings, setting)

        self.options["-x"] = setting

    @property
    def compress(self) -> str:
        return self.options["-z"]

    @compress.setter
    def compress(self, setting: Union[bool, str, int]) -> None:
        settings_conversion = {True: "y", False: "n", 3: "3"}
        valid_settings = ["y", "o", "i", "n", "3"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Compression", valid_settings, setting)

        self.options["-z"] = setting

    @property
    def byte_order(self) -> str:
        return self.options["--big-endian"]

    @byte_order.setter
    def byte_order(self, setting: Union[bool, str]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n", "o"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Byte order", valid_settings, setting)

        self.options["--big-endian"] = setting

    @property
    def progress(self) -> str:
        return self.options["--progress"]

    @progress.setter
    def progress(self, setting: Union[bool, str]) -> None:
        settings_conversion = {True: "y", False: "n"}
        valid_settings = ["y", "n"]

        setting = self._convert_settings(settings_conversion, setting)

        self._check_valid_setting("Progress", valid_settings, setting)

        self.options["--progress"] = setting

    @property
    def terse(self) -> str:
        return self.options["terse"]

    @terse.setter
    def terse(self, setting: bool) -> None:
        valid_settings = [True, False]
        self._check_valid_setting("Terse", valid_settings, setting)
        self.options["terse"] = setting

    def _convert_options_to_arg_list(self) -> list:
        arg_list = []
        for i_key, i_val in self.options.items():
            if i_key[0] == "-":
                arg_list.append(i_key)
                arg_list.append(i_val)
            elif i_key == "compression_level":
                arg_list.append("-" + i_val)
            elif i_key == "terse" and i_val:
                arg_list.append("--terse")

        return arg_list

    def convert(self, input_path: str, output_path: str = None, options: list = None):
        if output_path is None:
            output_path = input_path
        if options is None:
            options = []

        arg_list = self._convert_options_to_arg_list()

        command_line_args = [*arg_list, "-o", "/output", "/input"]

        bindings = self._make_input_output_binding(input_path, output_path)

        if not self.download_container:
            output = Client.run(self.container_url, command_line_args, bind=bindings, stream=True)
        else:
            output = Client.run(
                os.path.join(self.download_folder, self.download_name),
                command_line_args,
                bind=bindings,
                stream=True,
            )

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

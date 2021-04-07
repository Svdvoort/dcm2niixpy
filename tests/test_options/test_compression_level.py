import pytest

import dcm2niixpy.dcm2niix


def test_initial_compression_level_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    compression_level = dcm2niix.compression_level  # act

    assert isinstance(compression_level, int)
    assert compression_level == 6


def test_invalid_type_compression_level_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()
    raised_error_msg = r"Compression level setting should be one of 'str, int', you passed an argument with type 'bool'"

    with pytest.raises(TypeError, match=raised_error_msg):
        dcm2niix.compression_level = True


def test_invalid_compression_level_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()
    raised_error_msg = r"Compression level setting should be one of '0, 1, 2, 3, 4, 5, 6, 7, 8, 9', you passed '15'"

    with pytest.raises(ValueError, match=raised_error_msg):
        dcm2niix.compression_level = 15


def test_int_compression_level_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()
    to_test_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for i_level in to_test_levels:
        dcm2niix.compression_level = i_level

        assert isinstance(dcm2niix.compression_level, int)
        assert dcm2niix.compression_level == i_level


def test_str_compression_level_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()
    to_test_levels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    for i_level in to_test_levels:
        dcm2niix.compression_level = i_level

        assert isinstance(dcm2niix.compression_level, int)
        assert dcm2niix.compression_level == int(i_level)

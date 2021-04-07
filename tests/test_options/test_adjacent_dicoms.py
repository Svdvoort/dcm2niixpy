import pytest

import dcm2niixpy.dcm2niix


def test_initial_adjacent_dicom_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    adjacent_dicoms = dcm2niix.adjacent_dicoms  # act

    assert isinstance(adjacent_dicoms, bool)
    assert adjacent_dicoms is False


def test_invalid_type_adjacent_dicom_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    raised_error_msg = r"Adjacent DICOM setting should be one of 'str, bool', you passed an argument with type 'int'"

    with pytest.raises(TypeError, match=raised_error_msg):
        dcm2niix.adjacent_dicoms = 5


def test_invalid_adjacent_dicom_setting():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()
    raised_error_msg = r"Adjacent DICOM setting should be one of 'y, n', you passed '5'"

    with pytest.raises(ValueError, match=raised_error_msg):
        dcm2niix.adjacent_dicoms = "5"


def test_adjacent_dicom_setting_true():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    dcm2niix.adjacent_dicoms = True

    assert dcm2niix.adjacent_dicoms is True


def test_adjacent_dicom_setting_y():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    dcm2niix.adjacent_dicoms = "y"

    assert dcm2niix.adjacent_dicoms is True


def test_adjacent_dicom_setting_false():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    dcm2niix.adjacent_dicoms = False

    assert dcm2niix.adjacent_dicoms is False


def test_adjacent_dicom_setting_n():
    dcm2niix = dcm2niixpy.dcm2niix.DCM2NIIX()

    dcm2niix.adjacent_dicoms = "n"

    assert dcm2niix.adjacent_dicoms is False

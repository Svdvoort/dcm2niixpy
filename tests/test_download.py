import os
import tempfile

import dcm2niixpy


def test_download_specific_version_container(test_version):
    expected_output_name = "dcm2niix_{test_version}.sif".format(test_version=test_version)

    with tempfile.TemporaryDirectory() as tmp_dir:
        dcm2niix = dcm2niixpy.DCM2NIIX(download=True, download_folder=tmp_dir, version=test_version)
        dcm2niix._download_container()

        assert os.path.exists(os.path.join(tmp_dir, expected_output_name))


def test_run_downloaded_container(test_version, testdata_dir):
    covert_dir = os.path.join(testdata_dir, "BRAIN_MR")

    with tempfile.TemporaryDirectory() as tmp_dir:
        dcm2niix = dcm2niixpy.DCM2NIIX(version=test_version, download=True, download_folder=tmp_dir)
        dcm2niix.compress = True
        dcm2niix.filename = "TEST"

        dcm2niix.convert(covert_dir, tmp_dir)

        assert os.path.exists(os.path.join(tmp_dir, "TEST.nii.gz"))

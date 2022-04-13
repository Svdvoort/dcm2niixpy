import dcm2niixpy


def test_initial_compression_setting(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_y(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = "y"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "y"


def test_set_compression_setting_o(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = "o"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "o"


def test_set_compression_setting_i(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = "i"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "i"


def test_set_compression_setting_n(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = "n"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_3_str(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = "3"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "3"


def test_set_compression_setting_true(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = True

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "y"


def test_set_compression_setting_false(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = False

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_3_int(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = 3

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "3"


def test_set_compression_setting_twice(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    dcm2niix.compress = True
    dcm2niix.compress = False

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"

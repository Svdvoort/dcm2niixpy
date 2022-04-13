import dcm2niixpy


def test_initial_compression_setting():
    dcm2niix = dcm2niixpy.DCM2NIIX()

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_y():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = "y"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "y"


def test_set_compression_setting_o():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = "o"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "o"


def test_set_compression_setting_i():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = "i"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "i"


def test_set_compression_setting_n():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = "n"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_3_str():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = "3"

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "3"


def test_set_compression_setting_true():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = True

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "y"


def test_set_compression_setting_false():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = False

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"


def test_set_compression_setting_3_int():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = 3

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "3"


def test_set_compression_setting_twice():
    dcm2niix = dcm2niixpy.DCM2NIIX()
    dcm2niix.compress = True
    dcm2niix.compress = False

    compression_setting = dcm2niix.compress  # act

    assert compression_setting == "n"

import dcm2niixpy


def test_with_no_options(test_version):
    dcm2niix = dcm2niixpy.DCM2NIIX(test_version)
    default_options = [
        "-6",
        "-a",
        "n",
        "-b",
        "y",
        "-ba",
        "y",
        "-d",
        "5",
        "-e",
        "n",
        "-f",
        "%f_%p_%t_%s",
        "-g",
        "n",
        "-i",
        "n",
        "-l",
        "n",
        "-m",
        "2",
        "-r",
        "n",
        "-s",
        "n",
        "-t",
        "n",
        "-v",
        "0",
        "-w",
        "2",
        "-x",
        "n",
        "--big-endian",
        "o",
        "--progress",
        "n",
        "-z",
        "n",
    ]

    result = dcm2niix._convert_options_to_arg_list()

    assert isinstance(result, list)
    assert result == default_options

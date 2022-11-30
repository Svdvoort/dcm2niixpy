Tutorial
======================

dcm2niixpy is a package that allows running of dcm2niix in a pythonic way.
**Currently dcm2niixpy relies on Singularity as backend to run the dcm2niix container**.

Without singularity installed this package cannot run dcm2niix.

Installation
----------------

dcm2niixpy can be installed as follows:

``pip install dcm2niixpy``

Apart from the pip install you need to make sure that Singularity is also installed.

Simple conversion
-------------------

The easiest way to use dcm2niixpy is initiating an instance, and running with all the default settings.

Convert a DICOM folder in it's simplest form:

>>> import dcm2niixpy
>>> dcm2niix = dcm2niixpy.DCM2NIIX(version="1.0.20220720")
>>> dcm2niix.convert("/path/to/dicom/folder")

You are always required to specify the ``version`` argument when initializing dcm2niixpy.
This determines which version of dcm2niix will be used in the backend.
An overview of the available tags can be found on `The docker hub <https://hub.docker.com/r/svdvoort/dcm2niix/tags>`_

The converted NIFTI file will be located in the DICOM folder

Setting filenames
------------------

You can specify where and under which name the converted file should be saved:

>>> import dcm2niixpy
>>> dcm2niix = dcm2niixpy.DCM2NIIX(version="1.0.20220720")
>>> dcm2niix.filename = "/path/to/output/image.nii.gz"
>>> dcm2niix.convert("/path/to/dicom/folder")

The converted file will then be saved as ``/path/to/output/image.nii.gz``

Setting dcm2niix options
-------------------------

All of the settings that are available for dcm2niix can be passed through the pythonic interface.

For example:

>>> import dcm2niixpy
>>> dcm2niix = dcm2niixpy.DCM2NIIX(version="1.0.20220720")
>>> dcm2niix.directory_search_depth = 1
>>> dcm2niix.filename = "/path/to/output/image.nii.gz"
>>> dcm2niix.convert("/path/to/dicom/folder")

Sets the directory search depth (``-d`` option in dcm2niix) to 1.
A complete overview of all parameters can be found on the modules page: :py:class:`dcm2niixpy.dcm2niix`

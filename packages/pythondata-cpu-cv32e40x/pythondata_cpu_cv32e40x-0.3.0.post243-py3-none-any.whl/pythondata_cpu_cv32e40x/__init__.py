import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post243"
version_tuple = (0, 3, 0, 243)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post243")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post115"
data_version_tuple = (0, 3, 0, 115)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post115")
except ImportError:
    pass
data_git_hash = "90e95bd90d897ab57542066e99a382a1bb2e77d0"
data_git_describe = "0.3.0-115-g90e95bd9"
data_git_msg = """\
commit 90e95bd90d897ab57542066e99a382a1bb2e77d0
Merge: 22cf8949 f6225350
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu May 19 13:30:55 2022 +0200

    Merge pull request #545 from Silabs-ArjanB/ArjanB_bitma
    
    Fixed dependency between Zc and Zbb

"""

# Tool version info
tool_version_str = "0.0.post128"
tool_version_tuple = (0, 0, 128)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post128")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn

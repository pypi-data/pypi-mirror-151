import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post241"
version_tuple = (0, 3, 0, 241)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post241")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post113"
data_version_tuple = (0, 3, 0, 113)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post113")
except ImportError:
    pass
data_git_hash = "22cf89493f0cfa86ad1fbf471086928da7a36e01"
data_git_describe = "0.3.0-113-g22cf8949"
data_git_msg = """\
commit 22cf89493f0cfa86ad1fbf471086928da7a36e01
Merge: d7d8298e 7f79e521
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu May 19 11:50:01 2022 +0200

    Merge pull request #544 from Silabs-ArjanB/ArjanB_irqr
    
    Reordered content in exceptions and interrupts chapter for clarity

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

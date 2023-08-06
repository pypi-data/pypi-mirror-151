import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post237"
version_tuple = (0, 3, 0, 237)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post237")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post109"
data_version_tuple = (0, 3, 0, 109)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post109")
except ImportError:
    pass
data_git_hash = "63985640f2d11aebe183a53655b3f226fde17bfd"
data_git_describe = "0.3.0-109-g63985640"
data_git_msg = """\
commit 63985640f2d11aebe183a53655b3f226fde17bfd
Merge: 2183a8f5 81617bb7
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed May 18 10:44:29 2022 +0200

    Merge pull request #542 from silabs-oysteink/silabs-oysteink_lastop
    
    Introduced "last_op" to alle pipeline stages. Needed for Zc* instruct…

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

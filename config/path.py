import os
from configparser import ConfigParser

conf = ConfigParser()
# ROOT PATH
RootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# CONFIG PATH
ConfigDir = os.path.join(RootPath, 'config')

# Config File
ConfigFile = os.path.join(ConfigDir, "config.ini")

# PACKAGE PATH
PackageDir = os.path.join(RootPath, 'package')

# IPA PATH
conf.read(ConfigFile)
IOS = os.path.join(PackageDir, conf.get('package', 'iOS'))

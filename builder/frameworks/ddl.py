import sys
from os.path import join, isfile

from SCons.Script import DefaultEnvironment, SConscript

print("ddl.py running")

env = DefaultEnvironment()
build_script = join(env.PioPlatform().get_package_dir("framework-hc32f46x-ddl"), "tools", "platformio", "platformio-build-ddl.py")

if not isfile(build_script):
    sys.stderr.write("Error: Missing PlatformIO build script %s!\n" % build_script)
    env.Exit(1)

SConscript(build_script)

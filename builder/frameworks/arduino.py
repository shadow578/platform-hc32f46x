import sys
from os.path import join, isfile

from SCons.Script import DefaultEnvironment, SConscript


env = DefaultEnvironment()
build_script = join(env.PioPlatform().get_package_dir("framework-arduino-hc32f46x"), "tools", "platformio", "platformio-build-arduino.py")

if not isfile(build_script):
    sys.stderr.write(f"Error: Missing PlatformIO build script {build_script}!\n")
    env.Exit(1)

SConscript(build_script)

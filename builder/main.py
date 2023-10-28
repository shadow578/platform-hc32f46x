import sys
from os.path import join

from SCons.Script import (
    COMMAND_LINE_TARGETS,
    AlwaysBuild,
    Builder,
    Default,
    DefaultEnvironment,
)


# resolve environment
env = DefaultEnvironment()


# use arm-none-eabi-* binaries
env.Replace(
    AR="arm-none-eabi-gcc-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    GDB="arm-none-eabi-gdb",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ARFLAGS=["rc"],
    
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD="$SIZETOOL -B -d $SOURCES",
    
    # note: size regexprs are defined in framework build, as they
    # depend on the linker script used

    PROGSUFFIX=".elf"
)

# configure builder
env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        )
    ),

    LINKFLAGS=[
        # don't care about RWX sections, we're running from flash anyway
        "-Wl,--no-warn-rwx-segment",
    ],
)


# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

if not env.get("PIOFRAMEWORK"):
    sys.stderr.write("Error: PIOFRAMEWORK is not defined")
    env.Exit(1)


#
# Target: Build executable and linkable firmware
#
target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.hex")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToBin(join("$BUILD_DIR", "${PROGNAME}"), target_elf)
    #env.Depends(target_firm, "checkprogsize") #todo checkprogsize

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)


#
# Target: Print binary size
#
target_size = env.AddPlatformTarget(
    "size",
    target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"),
    "Program Size",
    "Calculate program size",
)


#
# Setup default targets
#
Default([target_buildprog, target_size])

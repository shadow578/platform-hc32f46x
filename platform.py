# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import subprocess

from platformio import proc
from platformio.managers.platform import PlatformBase

def is_pyocd_installed():
    """Check if pyOCD is installed."""
    try:
        import pyocd
        return pyocd.__version__ == "0.36.0"
    except ImportError:
        return False

def install_pyocd():
    """Install pyOCD package."""
    args = [
        proc.get_pythonexe_path(),
        "-m",
        "pip",
        "install",
        "pyocd==0.36.0"
    ]

    return subprocess.call(args) == 0

class Hc32f46xPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        # install pyOCD 0.36.0 package
        # TODO this is a workaround needed until PlatformIO decided they'd want to support 
        # a pyOCD version that isn't absolutely ancient...
        if not is_pyocd_installed():
            sys.stderr.write("Warning: pyOCD is not installed. Installing...\n")
            if not install_pyocd():
                sys.stderr.write("Error: Couldn't install dependencies for pyOCD!\n")
                sys.exit(1)
        
        return super().configure_default_packages(variables, targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug["tools"] = {}

        # add configuratins for OpenOCD based debugging probes
        for interface in ("stlink", "cmsis-dap"):
            # skip if the tool is already defined
            if interface in debug["tools"]:
                continue

            # get target script from board manifest
            pyocd_target = debug.get("pyocd_target")
            assert pyocd_target, (
                f"Missed target configuration for {board.id}")
            
            # create OpenOCD server arguments
            server_args = [
                "-m", "pyocd",
                "gdbserver",
                "--no-wait",
                "--target", pyocd_target,
            ]
            server_args.extend(debug.get("pyocd_extra_args", []))
            
            # assign the tool configuration
            debug["tools"][interface] = {
                "server": {
                    #"package": "tool-openocd",
                    "executable": "$PYTHONEXE",
                    "arguments": server_args,
                    "ready_pattern": "GDB server started on port 3333",
                },
                "port": ":3333",
                "init_cmds": [
                    "define pio_reset_halt_target",
                    "   monitor reset halt",
                    "end",
                    "define pio_reset_run_target",
                    "   monitor reset",
                    "end",
                    "target remote $DEBUG_PORT",
                    "$INIT_BREAK",
                    "$LOAD_CMDS"
                ],
            }

        board.manifest["debug"] = debug
        return board

    def configure_debug_session(self, debug_config):
        env_options = debug_config.env_options

        # get user-defined debug_extra_cmds
        if "debug_extra_cmds" in env_options:
            debug_extra_cmds = env_options["debug_extra_cmds"]
        else:
            debug_extra_cmds = []

        # add extra commands to GDB
        # TODO adding GDP commands in this way seems really hacky...
        env_options["debug_extra_cmds"] = [
            #"target extended-remote localhost:3333",
            "set mem inaccessible-by-default off",
            *debug_extra_cmds,
        ]

        if debug_config.speed:
            server_executable = (debug_config.server or {}).get("executable", "").lower()
            if "openocd" in server_executable:
                debug_config.server["arguments"].extend(
                    ["-c", "adapter speed %s" % debug_config.speed]
                )
            elif "jlink" in server_executable:
                debug_config.server["arguments"].extend(
                    ["-speed", debug_config.speed]
                )
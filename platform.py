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

import os

from platformio.managers.platform import PlatformBase

class Hc32f46xPlatform(PlatformBase):

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
            openocd_target = debug.get("openocd_target")
            assert openocd_target, (
                f"Missed target configuration for {board.id}")
            
            # if the target name starts with 'HC32:', it should use 
            # a target script provided by this platform, otherwise
            # it should use a script provided by OpenOCD
            if openocd_target.startswith("HC32:"):
                openocd_custom_scripts_dir = os.path.join(
                    self.get_dir(), "misc", "openocd"
                )
                target_script = os.path.join(
                    openocd_custom_scripts_dir, "target",  openocd_target[5:] + ".cfg"
                )
            else:
                target_script = f"target/{openocd_target}.cfg"
            
            # create OpenOCD server arguments
            server_args = [
                "-s", "$PACKAGE_DIR/openocd/scripts",
                "-f", f"interface/{interface}.cfg",
                "-c", f"transport select {('hla_swd' if interface == 'stlink' else 'swd')}",
                "-f", target_script
            ]
            server_args.extend(debug.get("openocd_extra_args", []))
            
            # assign the tool configuration
            debug["tools"][interface] = {
                "server": {
                    "package": "tool-openocd",
                    "executable": "bin/openocd",
                    "arguments": server_args
                }
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
            "mem 0x00000000 0x0007FFFF ro",
            "mem 0x1FFF8000 0x20026FFF rw",
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
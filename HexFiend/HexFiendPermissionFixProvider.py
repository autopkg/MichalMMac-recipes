#!/usr/bin/python
#
# Copyright 2015 Michal Moravec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for HexFiendPermissionFixProvider class"""

import os
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["HexFiendPermissionFixProvider"]

class HexFiendPermissionFixProvider(Processor):
    """Fixes 700/600 permission on Sparkle framework bundle"""
    description = __doc__
    input_variables = { }
    output_variables = { }

    def main(self):
        '''Do our processor task!'''
        recipe_cache_dir = self.env["RECIPE_CACHE_DIR"]
        name = self.env["NAME"]
        sparkle_framework = 'Hex Fiend.app/Contents/Frameworks/Sparkle.framework'
        sparkle_binary = 'Versions/A/Sparkle'
        sparkle_relaunch = 'Versions/A/Resources/relaunch'
        frameworkpath = os.path.join(recipe_cache_dir, name, sparkle_framework )
        subprocess.call(['chmod', '-R', 'go+rX' , os.path.realpath(frameworkpath) ])
        binarypath = os.path.join(recipe_cache_dir, name, sparkle_framework, sparkle_binary)
        subprocess.call(['chmod', '-R', 'go+x' , os.path.realpath(binarypath) ])
        relaunchpath = os.path.join(recipe_cache_dir, name, sparkle_framework, sparkle_relaunch)
        subprocess.call(['chmod', '-R', 'go+x' , os.path.realpath(relaunchpath) ])

if __name__ == "__main__":
    PROCESSOR = HexFiendPermissionFixProvider()
    PROCESSOR.execute_shell()

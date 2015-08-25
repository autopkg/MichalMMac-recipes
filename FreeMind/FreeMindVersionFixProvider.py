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
"""See docstring for FreeMindVersionFixProvider class"""

import re

from autopkglib import Processor, ProcessorError

__all__ = ["FreeMindVersionFixProvider"]

class FreeMindVersionFixProvider(Processor):
    """Fixes Freemind fraked up version X.X.X (build: Y) to X.X.X.Y"""
    description = __doc__
    input_variables = {
            "version": {
            "required": True,
            "description": "Original FreeMind version"
            } 
    }
    output_variables = {
        "version": {
            "description": "Fixed FreeMind version."
        }
    }

    def main(self):
        '''Do our processor task!'''
        original_version = self.env["version"]
        p = re.compile('^(?P<vers>([0-9]\.){2}[0-9])[ ]\(build:[ ](?P<build>[0-9])\)')
        fixed_version = p.sub('\g<vers>.\g<build>', original_version)
        self.env["version"] = fixed_version

if __name__ == "__main__":
    PROCESSOR = FreeMindVersionFixProvider()
    PROCESSOR.execute_shell()

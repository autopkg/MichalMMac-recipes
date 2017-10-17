#!/usr/bin/env python

from autopkglib import Processor, ProcessorError


__all__ = ["StoreVariable"]

class StoreVariable(Processor):
    """Provides a download URL for the latest LibreOffice"""
    input_variables = {
        "variable_content": {
            "required": True,
            "description": "Variable string content",
        },
    }
    
    output_variables = {
       "var_store": {
            "required": True,
            "description": "Stored variable",
        },
    }
   
    description = __doc__
     
    def main(self):
        self.env["var_store"] = self.env["variable_content"]


if __name__ == "__main__":
    processor = LibreOfficeURLProvider()
    processor.execute_shell()
#!/usr/bin/env python3
#
# Ipynb to Text module
#
# This is responsible for converting ipynb json files to batspp text.
#
## TODO: add sopport for images (ipynb display_data output type).

"""
Ipynb to Text module

This is responsible for converting ipynb json files to batspp text
"""

# Standard packages
import json

# Installed packages
## NOTE: this is empty for now

# Local packages
## NOTE: this is empty for now


class IpynbToBatspp:
    """
    This is responsible for converting ipynb json test to Batspp style text
    """

    def convert(self, ipynb: str) -> str:
        """
        Convert ipynb json to batspp text
        """
        result = ""
        ipynb = json.loads(ipynb)
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                result += self.convert_markdown_cell_to_comment(cell)
            elif cell['cell_type'] == 'code':
                result += self.convert_code_cell_to_commands(cell)
        return result

    def convert_markdown_cell_to_comment(self, markdown_cell: dict) -> str:
        """
        Convert markdown to batspp comment
        """
        return merge_lines(markdown_cell['source'], line_start="# ")

    def convert_code_cell_to_commands(self, code_cell: dict) -> str:
        """
        Convert code to batspp command
        """
        result = ""

        # Source to command
        result = "$ " + code_cell['source'][0]
        result += merge_lines(code_cell['source'][1:], line_start="$ ")

        # Output to text
        for output in code_cell['outputs']:

            # Stream output type
            if output['output_type'] == 'stream':
                result += merge_lines(output['text'])

            # Error output type
            elif output['output_type'] == 'error':
                result += merge_lines(output['ename'])

            else:
                ## NOTE: display_data (used for images) is not supported for now
                raise Exception("Output type not sopported for now: " + output['output_type'])

        return result

def merge_lines(lines:list, line_start="") -> str:
    """
    Merge lines into single string,
    ensuring that every line has a LINE_START
    and a trailing newline
    """
    result = ""
    for line in lines:
        result += line_start + line
    return ensure_trailing_newline(result)

def ensure_trailing_newline(text:str) -> str:
    """Ensure text has a trailing newline"""
    if not text.endswith('\n'):
        text += '\n'
    return text

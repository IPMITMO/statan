import re

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class MatlabIndentationBear(LocalBear):
    LANGUAGES = {'Matlab', 'Octave'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @deprecate_settings(indent_size='tab_width')
    def run(self, filename, file, indent_size: int=2):
        """
        This bear features a simple algorithm to calculate the right
        indentation for Matlab/Octave code. However, it will not handle hanging
        indentation or conditions ranging over several lines yet.

        :param indent_size: Number of spaces per indentation level.
        """
        new_file = tuple(self.reindent(file, indent_size))

        if new_file != tuple(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'The indentation could be changed to improve readability.',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    @staticmethod
    def reindent(file, indentation):
        indent, nextindent = 0, 0
        for line_nr, line in enumerate(file, start=1):
            indent = nextindent
            indent, nextindent = MatlabIndentationBear.get_indent(line,
                                                                  indent,
                                                                  nextindent)
            stripped = line.lstrip()
            if stripped:
                yield indent*indentation*' ' + stripped
            else:
                yield line

    @staticmethod
    def get_indent(line, indent, nextindent):
        ctrlstart = r'\s*(function|if|while|for|switch)'
        ctrlcont = r'\s*(elseif|else|case|catch|otherwise)'
        ctrlend = r'\s*(end|endfunction|endif|endwhile|endfor|endswitch)'
        if re.match(ctrlstart, line) is not None:
            return indent, nextindent+1
        elif re.match(ctrlcont, line) is not None:
            return indent-1, nextindent
        elif re.match(ctrlend, line) is not None:
            return indent-1, nextindent-1
        else:
            return indent, indent

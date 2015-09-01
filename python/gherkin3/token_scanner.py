import io
import os
from .token import Token
from .gherkin_line import GherkinLine
try:
    python2 = True
    from cStringIO import StringIO
except ImportError:
    python2 = False
    from io import StringIO


class TokenScanner(object):
    def __init__(self, path_or_str):
        if isinstance(path_or_str, str):
            if os.path.exists(path_or_str):
                self.io = io.open(path_or_str, 'rU')
            else:
                self.io = io.StringIO(path_or_str)
        self.line_number = 0

    def read(self):
        self.line_number += 1
        location = {'line': self.line_number}
        line = self.io.readline()
        if python2:
            line = line.decode('utf-8')
        return Token((GherkinLine(line, self.line_number) if line else line), location)
    
    def __del__(self):
        # close file descriptor if it's still open
        try:
            self.io.close()
        except AttributeError:
            pass


import os
import unittest

from gen.generate import Generator


class FileGenerator(Generator):

    def __init__(self, output_file=None):
        super(FileGenerator, self).__init__()
        self.output_file = output_file
        self.output_dir = None
        self.parent_generator = None

    def get_output_dir(self):
        output_dir = None

        if self.parent_generator is None:
            output_dir = self.parent_generator.get_output_dir()

        if self.output_dir is not None:
            if output_dir is None:
                output_dir = self.output_dir
            else:
                output_dir += os.sep + self.output_dir

        return output_dir

    def get_output_file(self):

        if self.output_file is None:
            raise ValueError('FileGenerator output_file class variable is None')

        output_dir = self.get_output_dir()

        if output_dir is None:
            return self.output_file
        else:
            return output_dir + os.sep + self.output_file



###############################################################################
#
# Unit Tests
#

class TestFileGenerator(unittest.TestCase):

    def testConstructor(self):
        fg = FileGenerator()
        self.assertNotEqual(fg, None)
        fg.generate()


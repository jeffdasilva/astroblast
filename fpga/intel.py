import os
import unittest

from gen.file import FileGenerator
from gen.generate import Generator
from gen.project import ProjectGenerator

# decorate the generator classes by overriding the templates directory

class IntelFpgaGenerator(Generator):
    def __init__(self):
        super(IntelFpgaGenerator, self).__init__()
        self.template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates" + os.sep + "intelFPGA"

class IntelFpgaFileGenerator(FileGenerator):
    def __init__(self, output_file=None):
        super(IntelFpgaFileGenerator, self).__init__(output_file=output_file)
        self.template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates" + os.sep + "intelFPGA"

class IntelFpgaProjectGenerator(ProjectGenerator):
    def __init__(self, output_dir=None):
        super(IntelFpgaProjectGenerator, self).__init__(output_dir=output_dir)
        self.template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates" + os.sep + "intelFPGA"

###############################################################################
#
# Unit Tests
#

class TestIntelFpgaGenerator(unittest.TestCase):

    def testConstructor(self):
        g = IntelFpgaGenerator()
        self.assertNotEqual(g, None)

        fg = IntelFpgaFileGenerator()
        self.assertNotEqual(fg, None)

        pg = IntelFpgaProjectGenerator()
        self.assertNotEqual(pg, None)

    def testTemplateDir(self):

        fg = IntelFpgaFileGenerator()
        fg.append_template("../test/fpga_mock.txt")
        print Generator.generate(fg)
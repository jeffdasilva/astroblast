import os
import unittest

from gen.file import FileGenerator
from gen.generate import Generator
from gen.project import ProjectGenerator

# Decorate the generator classes by overriding the templates directory
class IntelFpgaGenerator(Generator):
    def __init__(self):
        super(IntelFpgaGenerator, self).__init__()
        self.template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates" + os.sep + "intelFPGA"

class IntelFpgaFileGenerator(FileGenerator, IntelFpgaGenerator):
    def __init__(self, output_file=None):
        super(IntelFpgaFileGenerator, self).__init__(output_file=output_file)

class IntelFpgaProjectGenerator(ProjectGenerator, IntelFpgaFileGenerator):
    def __init__(self, output_dir=None):
        super(IntelFpgaProjectGenerator, self).__init__(output_dir=output_dir)

###############################################################################
#
# Unit Tests
#

class TestIntelFpgaGenerator(unittest.TestCase):

    def testConstructor(self):

        expected_template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates" + os.sep + "intelFPGA"

        g = IntelFpgaGenerator()
        self.assertNotEqual(g, None)
        self.assertEqual(g.template_dir, expected_template_dir)

        fg = IntelFpgaFileGenerator()
        self.assertNotEqual(fg, None)
        self.assertEqual(fg.template_dir, expected_template_dir)

        pg = IntelFpgaProjectGenerator()
        self.assertNotEqual(pg, None)
        self.assertEqual(pg.template_dir, expected_template_dir)


    def testTemplateDir(self):

        fg = IntelFpgaFileGenerator()
        fg.append_template("../test/fpga_mock.txt")
        print Generator.generate(fg)
import os
import unittest

from gen.file import FileGenerator


class ProjectGenerator(FileGenerator):

    def __init__(self, output_dir="None"):
        super(ProjectGenerator, self).__init__(output_file=".astroblast")
        self.output_dir = output_dir

        self.files = []

    def append_file(self, file_generator):

        if file_generator.parent_generator is not None:
            raise ValueError('File being added to ProjectGenerator already has a parent')

        file_generator.parent_generator = self

        output_filename = file_generator.get_output_file()

        for f in self.files:
            if f.get_output_file() == output_filename:
                file_generator.parent_generator = None
                raise ValueError('Cannot add file with the same name to this project - ' + output_filename)

        self.files.append(file_generator)

    def generate(self):

        for f in self.files:
            f.generate()

        FileGenerator.generate(self)

###############################################################################
#
# Unit Tests
#

class TestProjectGenerator(unittest.TestCase):

    def setUp(self):
        self.test_root_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + \
            ".." + os.sep + "work" + os.sep + "unittest.tmp" + os.sep + "gen" + \
            os.sep + "project"

    def testConstructor(self):
        pg = ProjectGenerator()
        self.assertNotEqual(pg, None)

    def testErrorCases(self):
        pg = ProjectGenerator()

        foo = FileGenerator("foo.tmp")
        bar = FileGenerator("bar.tmp")

        self.assertEqual(len(pg.files),0)
        pg.append_file(foo)
        self.assertEqual(len(pg.files),1)
        pg.append_file(bar)
        self.assertEqual(len(pg.files),2)

        try:
            pg.append_file(bar)
            self.assertTrue(False, "You should never reach here")
        except ValueError:
            pass
        self.assertEqual(len(pg.files),2)

        try:
            pg.append_file(FileGenerator("foo.tmp"))
            self.assertTrue(False, "You should never reach here")
        except ValueError:
            pass
        self.assertEqual(len(pg.files),2)



if __name__ == "__main__":
    unittest.main()
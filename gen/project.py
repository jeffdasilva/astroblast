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

        generation_occured = False

        for f in self.files:
            generation_occured |= f.generate()

        generation_occured |= FileGenerator.generate(self)

        return generation_occured

###############################################################################
#
# Unit Tests
#

class TestProjectGenerator(unittest.TestCase):

    def setUp(self):
        from gen.file import TestFileGenerator
        self.test_root_dir = TestFileGenerator.get_unittest_dir(__file__, '../work/unittest.tmp/gen/project')

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


    def testGenerate(self):
        pg = ProjectGenerator()
        foo = FileGenerator("foo.tmp")
        bar = FileGenerator("bar.tmp")
        pg.append_file(foo)
        pg.append_file(bar)
        pg.output_dir = self.test_root_dir + '/proj1'

        pg.generate()
        self.assertFalse(pg.generate())

        foo.append_template("test/mock.txt")
        self.assertTrue(pg.generate())
        self.assertFalse(pg.generate())

        pg.snr.append(('<add stuff here>',"astroblast!"))
        self.assertTrue(pg.generate())
        self.assertFalse(pg.generate())

if __name__ == "__main__":
    unittest.main()
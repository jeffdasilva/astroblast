
import errno
import os
import unittest

from gen.generate import Generator


class FileGenerator(Generator):

    def __init__(self, output_file=None):
        super(FileGenerator, self).__init__()
        self.output_file = output_file
        self.output_dir = None

    def get_output_dir(self):
        output_dir = None

        if self.parent_generator is not None:
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

    def mkdir_p(self,path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def read(self,path):
        fp = open(path, "r")
        text = fp.read()
        fp.close()
        return text

    def write(self,path,text):
        pathdir = os.path.dirname(path)
        self.mkdir_p(pathdir)

        fp = open(path, "w")
        fp.write(text)
        fp.close()
        return True

    def generate(self):
        filename = self.get_output_file()
        text = Generator.generate(self)

        if os.path.exists(filename):
            old_text = self.read(filename)
            if old_text == text:
                return False

        return self.write(filename,text)


###############################################################################
#
# Unit Tests
#

class TestFileGenerator(unittest.TestCase):

    def setUp(self):
        self.test_root_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + \
            ".." + os.sep + "work" + os.sep + "unittest.tmp" + os.sep + "gen" + \
            os.sep + "file"

    def testConstructor(self):
        fg = FileGenerator()
        self.assertNotEqual(fg, None)

    def testSimpleFileGen(self):
        fg = FileGenerator()
        fg.output_dir = self.test_root_dir
        fg.output_file = "foo/bar/test.tmp"

        fg.text = ""
        fg.generate()
        self.assertEquals(fg.generate(), False)
        fg.text = "foobar"
        self.assertEquals(fg.generate(), True)
        self.assertEquals(fg.generate(), False)
        self.assertEquals(fg.generate(), False)

        fg.snr.append(('oo','00'))
        self.assertEquals(fg.generate(), True)
        self.assertEquals(fg.generate(), False)

        self.assertEquals(fg.read(fg.get_output_file()), "f00bar")

    def testFileGenFromTemplate(self):
        fg = FileGenerator()
        fg.output_dir = self.test_root_dir
        fg.output_file = "mock.tmp"
        fg.append_template("test/mock.txt")
        fg.generate()
        self.assertEquals(fg.generate(), False)

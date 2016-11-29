#!/usr/bin/env python
import os
import re
import unittest


class Generator(object):

    def __init__(self):
        self.parent_generator = None
        self.text = None
        self.snr = []
        self.template_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "templates"

    def validate(self):
        assert(self.snr is not None)
        assert(self.get_snr() is not None)

        if self.parent_generator is not None:
            self.parent_generator.validate()

    def get_template_dir(self):
        return self.template_dir

    def append(self, text):

        if text is None:
            raise ValueError('text input to append is None')

        if isinstance(text, Generator):
            if text.parent_generator is not None:
                raise ValueError('Generator being added already has a parent generator')
            text.parent_generator = self

        if self.text is None:
            self.text = text
            return
        elif isinstance(text, basestring) and isinstance(self.text, basestring):
            self.text += text
            return

        if not isinstance(text, (list,tuple)):
            text = [ text ]

        if not isinstance(self.text, (list,tuple)):
            self.text = [ self.text ]
        else:
            for ele in text:
                if isinstance(ele, Generator):
                    ele.parent_generator = self

        self.text = self.text + text

    def append_template(self, template_file):
        abs_file = os.path.join(self.get_template_dir(), template_file)
        if not os.path.isfile(abs_file):
            raise ValueError("Template file " + abs_file + " does not exist")

        f = open(abs_file,'r')
        text = f.read()
        f.close()

        self.append(text)

    def get_snr(self):
        if self.parent_generator is not None:
            assert(self.parent_generator.snr is not None)
            assert(self.parent_generator.get_snr() is not None)
            return self.snr + self.parent_generator.get_snr()
        else:
            return self.snr

    def generate_string(self, text):
        for regex_tuple in self.get_snr():
            text = re.sub(regex_tuple[0],regex_tuple[1],text)
        return text

    def generate_list(self, text_list):
        text = ""
        for ele in text_list:
            text += self.generate_by_type(ele)
        return text

    def generate_by_type(self,text_obj):
        if text_obj is None:
            return ""
        elif isinstance(text_obj, basestring):
            return self.generate_string(text_obj)
        elif isinstance(text_obj, Generator):
            return text_obj.generate()
        elif isinstance(text_obj, (list,tuple)):
            return self.generate_list(text_obj)
        else:
            raise ValueError('self.text type is not valid')

    def generate(self):
        return self.generate_by_type(self.text)


###############################################################################
#
# Unit Tests
#


class TestGenerator(unittest.TestCase):

    def testConstructor(self):
        g = Generator()
        self.assertNotEqual(g, None)
        text = g.generate()
        self.assertEqual(text, "")

    def testGetTemplateDir(self):
        g = Generator()
        self.assertTrue(os.path.isfile(g.get_template_dir() + os.sep + "test" + os.sep + "mock.txt"))

    def testTempateGen(self):
        g = Generator()
        g.append_template('test/mock.txt')
        g.snr.append(('EOF','EOF.'))
        self.assertEqual(g.generate().splitlines()[-1],"EOF.")

    def testSimple(self):
        g = Generator()
        self.assertEqual(g.generate(), "")

        g.text = "This is a very simple generate text test.\n"
        print g.generate()
        self.assertEqual(g.generate(), g.text)

        g.text += " ...adding a multi-line test test:"
        g.text += '''
line1
line2
line3
DONE.
'''
        print g.generate()
        self.assertEqual(g.generate(), g.text)
        self.assertEqual(g.generate().splitlines()[-1],"DONE.")

    def testSearchAndReplace(self):
        g = Generator()
        g.text = "Hello World!"
        print g.generate()
        g.snr.append(('Hello', 'Good Morning'))
        g.snr.append(('W.*d!', 'Cruel World?'))
        g.snr.append(('Morning', 'Afternoon'))
        g.snr.append((r'(G[o]*d)',r'Have a \1'))
        print g.generate()
        self.assertEqual(g.generate(), "Have a Good Afternoon Cruel World?")

    def testListGen(self):
        g = Generator()
        g.text = ['This is ', 'a list ', ['of',' strings']]
        text = g.generate()
        self.assertEqual(text, 'This is a list of strings')
        g.text += [ (' and ', 'tuples!')]
        self.assertEqual(g.generate(), 'This is a list of strings and tuples!')
        g.snr.append(('tuples','a tuple of strings'))
        self.assertEqual(g.generate(), 'This is a list of strings and a tuple of strings!')

    def testSubGenerator(self):
        pg = Generator()
        pg.append("I am the parent generator\n")
        cg = Generator()
        cg.append("I am the child generator\n")
        pg.append(cg)
        self.assertEqual(pg.generate(),"I am the parent generator\nI am the child generator\n")

        cg.snr.append(('gener8r', 'XGen'))
        pg.snr.append(('generator', 'gener8r'))
        self.assertEqual(pg.generate(),"I am the parent gener8r\nI am the child gener8r\n")

        cg.snr.append(("I am", "I'm"))
        pg.snr.append(("I'm", "Im"))
        self.assertEqual(pg.generate(),"I am the parent gener8r\nIm the child gener8r\n")



if __name__ == "__main__":
    unittest.main()
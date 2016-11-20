#!/usr/bin/env python
import re
import unittest


class Generate(object):

    def __init__(self):
        self.text = ""
        self.snr = []
    
    def generate(self):
        gen_text = self.text
        
        for regex_tuple in self.snr:
            gen_text = re.sub(regex_tuple[0],regex_tuple[1],gen_text)
        
        return gen_text


###############################################################################
#
# Unit Tests
#


class TestGenerate(unittest.TestCase):

    def testConstructor(self):
        g = Generate()
        self.assertNotEqual(g, None)
        text = g.generate()
        self.assertEqual(text, "")

    def testSimple(self):
        g = Generate()
        self.assertEqual(g.generate(), "")
        
        g.text += "This is a very simple generate text test.\n"        
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
        g = Generate()
        g.text += "Hello World!"
        print g.generate()
        g.snr.append(('Hello', 'Good Morning'))
        g.snr.append(('W.*d!', 'Cruel World?'))
        g.snr.append(('Morning', 'Afternoon'))
        g.snr.append((r'(G[o]*d)',r'Have a \1'))
        print g.generate()
        self.assertEqual(g.generate(), "Have a Good Afternoon Cruel World?")
        
        
if __name__ == "__main__":
    unittest.main()
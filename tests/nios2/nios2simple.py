#!/usr/bin/env python

import os
import unittest

from fpga.quartus import QuartusProject


class Nios2TestSimple(unittest.TestCase):

    def setUp(self):
        from gen.file import TestFileGenerator
        self.test_root_dir = TestFileGenerator.get_unittest_dir(__file__, '../../work/tests/nios2')

    def test_generate_simple(self):

        qpf = QuartusProject("nios2simple")
        qpf.output_dir = os.path.join(self.test_root_dir,'simple')

        qpf.device_family = "CycloneV"
        qpf.device = "5CSEMA4U23C6"

        qpf.generate()


if __name__ == "__main__":
    unittest.main()
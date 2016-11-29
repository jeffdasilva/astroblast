import unittest

from fpga.intel import IntelFpgaProject, IntelFpgaFile


class QuartusProject(IntelFpgaProject):

    def __init__(self, project_name, project_dir=None):

        super(QuartusProject, self).__init__(output_dir=project_dir)
        self.project_name = project_name

        self.makefile = IntelFpgaFile('Makefile')
        self.makefile.append_template("Makefile")
        self.append_file(self.makefile)

        self.qsf = IntelFpgaFile(self.project_name + '_generate.tcl')
        self.append_file(self.qsf)

        self.sdc = IntelFpgaFile(self.project_name + '_timing_constraints.sdc')
        self.append_file(self.sdc)

        self.verilog_top = IntelFpgaFile(self.project_name + '_top.v')
        self.append_file(self.verilog_top)

        self.device_family = None

    def get_snr(self):
        return super(QuartusProject, self).get_snr()


###############################################################################
#
# Unit Tests
#

class TestQuartusProject(unittest.TestCase):

    def setUp(self):
        from gen.file import TestFileGenerator
        self.test_root_dir = TestFileGenerator.get_unittest_dir(__file__, '../work/unittest.tmp/fpga/quartus')

    def testConstructor(self):
        qpf = QuartusProject('test')
        self.assertNotEqual(qpf, None)
        qpf.validate()

    def testOneWire(self):
        qpf = QuartusProject('onewire')
        self.assertNotEqual(qpf, None)
        qpf.output_dir = self.test_root_dir
        qpf.generate()

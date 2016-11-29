import os
import unittest

from fpga.intel import IntelFpgaProject, IntelFpgaFile


class QuartusProject(IntelFpgaProject):

    UNKNOWN_DEVICE = "Unknown"

    def __init__(self, project_name, project_dir=None):

        super(QuartusProject, self).__init__(output_dir=project_dir)
        self.project_name = project_name

        self.makefile = IntelFpgaFile('Makefile')
        self.makefile.append_template("Makefile")
        self.append_file(self.makefile)

        self.qsf = IntelFpgaFile(self.project_name + '_quartus_generate.tcl')
        self.qsf.append_template("generate_quartus_project.tcl")
        self.append_file(self.qsf)

        self.sdc = IntelFpgaFile(self.project_name + '_timing_constraints.sdc')
        self.append_file(self.sdc)

        self.top_level_entity = IntelFpgaFile(self.project_name + '_top.v')
        self.append_file(self.top_level_entity)

        self.device = None
        self.device_family = None

    def get_device_family(self):
        if self.device_family is None:
            return QuartusProject.UNKNOWN_DEVICE
        else:
            return self.device_family

    def get_device(self):
        if self.device is None:
            return QuartusProject.UNKNOWN_DEVICE
        else:
            return self.device

    def get_snr(self):

        snr = []
        snr.append(('@DEVICE_FAMILY@', self.get_device_family()))
        snr.append(('@DEVICE@', self.get_device()))

        if self.sdc is not None:
            snr.append(('@SDC_FILE@', self.sdc.output_file))

        if self.top_level_entity is not None:
            top_level_entity_no_ext = self.top_level_entity.output_file.split('.',1)[0]
            snr.append(('@TOP_LEVEL_ENTITY@', top_level_entity_no_ext))


        return snr + super(QuartusProject, self).get_snr()


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

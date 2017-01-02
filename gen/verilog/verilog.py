import unittest

from gen.generate import Generator


class VerilogConstruct(Generator):
    uid_count = 0

    def __init__(self,name=None):
        super(VerilogConstruct, self).__init__()
        self.name = name
        self.uid = VerilogConstruct.uid_count
        VerilogConstruct.uid_count += 1

    def get_name(self):
        if self.name is None:
            self.name = str(self.__class__.__name__).lower() + "_" + str(self.uid)
        return self.name

    def comment(self, comment, ):
        return "// " + comment + "\n"

    def toHex(self, val, nbits, signed=True):
        if signed:
            val = (val + (1 << nbits)) % (1 << nbits)
        val = val & ((1 << nbits)-1)
        return hex(val).rstrip("L").lstrip("0x")

    def toHdlHex(self, val, width, signed=True):
        return str(width) + "'h" + self.toHex(val=val, nbits=width, signed=signed)


class Entity(VerilogConstruct):

    def __init__(self, name=None):
        super(Entity, self).__init__(name=name)
        self.parameters = []
        self.ports = []
        self.wires = []
        self.entities = []
        pass

    def get_text(self):

        self.text = None
        self.append(self.comment("Module: " + self.get_name()))
        self.append("module " + self.get_name() + " (\n")

        # ports
        num_of_ports = len(self.ports)
        for port in self.ports:
            self.append("    " + port.get_name())
            num_of_ports -= 1
            if num_of_ports > 0:
                self.append(",")
            self.append("\n")
        self.append(");\n")

        self.append("\n")

        # parameters
        if len(self.parameters) > 0:
            for parameter in self.parameters:
                self.append("    " + parameter.generate())
            self.append("\n")

        # parameters
        if len(self.ports) > 0:
            for port in self.ports:
                self.append("    " + str(port.get_type()) + " " + port.get_name())

                if port.width is None or port.width == 1:
                    pass
                else:
                    self.append("[")
                    if isinstance(port.width,Parameter):
                        self.append(port.width.get_name() + "-1")
                    elif isinstance(port.width,(int,long)):
                        self.append(str(port.width-1))
                    else:
                        self.append(str(port.width) + "-1")

                    self.append(":0]")
                self.append(";\n")

            self.append("\n")

        for ele in self.wires + self.ports:
            self.append(ele.generate())
        self.append("\n")

        if len(self.entities) > 0:
            for entity in self.entities:
                self.append(entity.instance().generate())
            self.append("\n")

        self.append("endmodule  " + self.comment("end of module " + self.get_name()))

        return self.text

class Wire(VerilogConstruct):
    def __init__(self, name=None, width=None):
        super(Wire, self).__init__(name=name)
        self.width = width

class Port(Wire):

    INPUT_TYPE = "input"
    OUTPUT_TYPE = "output"
    INOUT_TYPE = "inout"

    def __init__(self, name=None, port_type=None, width=None):
        super(Port, self).__init__(name=name, width=width)
        self.type = port_type

    def get_type(self):
        if self.type is None:
            return Port.INOUT_TYPE

        return self.type

class Parameter(VerilogConstruct):
    def __init__(self, name=None, value=None):
        super(Parameter, self).__init__(name=name)
        self.value = value

    def get_value(self):
        if self.value is None:
            return "0"

        if isinstance(self.value, basestring):
            return self.value

        return str(self.value)

    def get_name(self):
        if self.name is None:
            self.name = super(Parameter, self).get_name().upper()
        return self.name

    def get_text(self):
        self.text = None
        self.append("parameter " + self.get_name() + " = " + self.get_value() + ";\n")
        return self.text

###############################################################################
#
# Unit Tests
#

class TestEntity(unittest.TestCase):

    def testConstructor(self):
        m = Entity()
        text = m.generate()
        self.assertGreater(len(text),10)
        m.ports.append(Port())

        p = Port()
        p.name = "foo"
        p.width = 10
        p.type = Port.OUTPUT_TYPE

        m.ports.append(p)
        m.parameters.append(Parameter())
        ph = Parameter(name="OneHundred", value=100)
        m.parameters.append(ph)
        m.ports.append(Port(width=ph))

        text = m.generate()
        print text


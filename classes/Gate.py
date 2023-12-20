class Gate:
    gate_counter = 0

    # Characterizing gates by their type, number of fanins and fanouts
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.inputs = []
        self.outputs = []
        self.__class__.gate_counter += 1
        self.gate_counter = self.__class__.gate_counter

    # Connecting each wire inputs to their outputs
    def connect(self, inputs, outputs):
        for wire in inputs:
            wire.connect(self)
            self.inputs.append(wire)

        # Can have more than 1 output in case of fanouts
        for wire in outputs:
            wire.connect(self)
            self.outputs.append(wire)

    # Get general information of the gate's connections and outputs
    def get_info(self):
        wires_in_labels = []
        wires_out_labels = []
        output = 0
        print(
            """
Gate info:
----------"""
        )
        print("Gate type:", self.gate_type)
        print("Inputs:")
        for wire_in in self.inputs:
            wires_in_labels.append(wire_in.label)
        print(wires_in_labels)
        print("Outputs:")
        for wire_out in self.outputs:
            wires_out_labels.append(wire_out.label)
            output = wire_out.value
        print(wires_out_labels)
        print("output", output)

    # Get the logic of the gate
    # The procedure is to check for all inputs their condition
    # And apply the right output value for all fanouts of the gate
    def operate(self):
        if self.gate_type == "AND":
            if all(wire.get_effective_value == 1 for wire in self.inputs):
                for output in self.outputs:
                    output.value = 1
            else:
                for output in self.outputs:
                    output.value = 0

        if self.gate_type == "OR":
            if any(wire.get_effective_value == 1 for wire in self.inputs):
                for output in self.outputs:
                    output.value = 1
            else:
                for output in self.outputs:
                    output.value = 0

        if self.gate_type == "NAND":
            if all(wire.get_effective_value() == 1 for wire in self.inputs):
                for output in self.outputs:
                    output.value = 0
            else:
                for output in self.outputs:
                    output.value = 1

        if self.gate_type == "NOR":
            if any(wire.get_effective_value == 1 for wire in self.inputs):
                for output in self.outputs:
                    output.value = 0
            else:
                for output in self.outputs:
                    output.value = 1

        if self.gate_type == "XOR":
            if sum(wire.get_effective_value() % 2 == 1 for wire in self.inputs):
                for output in self.outputs:
                    output.value = 1
            else:
                for output in self.outputs:
                    output.value = 0

        if self.gate_type == "XNOR":
            if sum(self.inputs.value) % 2 == 0:
                for output in self.outputs:
                    output.value = 1
            else:
                for output in self.outputs:
                    output.value = 0


# Creating different classes for NOT and BUFFER as they can take only one input each
class NotGate(Gate):
    def __init__(self):
        super().__init__("NOT")

    def connect(self, inputs, outputs):
        for input_wire in inputs:
            self.inputs.append(input_wire)
        for output_wire in outputs:
            output_wire.connect(self)
            self.outputs.append(output_wire)

    def operate(self):
        if self.inputs[0].get_effective_value() == 1:
            for output in self.outputs:
                output.value = 0
        else:
            for output in self.outputs:
                output.value = 1


class BufferGate(Gate):
    def __init__(self):
        super().__init__("BUFFER")

    def connect(self, input_wire, output_wire):
        self.inputs.append(input_wire)
        output_wire.connect(self)
        self.outputs.append(output_wire)

    def operate(self):
        value = self.inputs[0].get_effective_value()
        for output in self.outputs:
            output.value = value

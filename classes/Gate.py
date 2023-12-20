class Gate:
    gate_counter = 0  # Class variable to keep track of the number of Gate instances

    # Constructor for Gate class
    def __init__(self, gate_type):
        self.gate_type = gate_type  # Type of the gate (e.g., AND, OR)
        self.inputs = []  # List to store input wires
        self.outputs = []  # List to store output wires
        self.__class__.gate_counter += 1  # Increment the gate counter
        self.gate_counter = (
            self.__class__.gate_counter
        )  # Instance-specific gate counter

    # Method to connect input and output wires to the gate
    def connect(self, inputs, outputs):
        for wire in inputs:
            wire.connect(self)  # Connect each input wire to this gate
            self.inputs.append(wire)  # Add the input wire to the inputs list

        # Can have multiple outputs in case of fanouts
        for wire in outputs:
            wire.connect(self)  # Connect each output wire to this gate
            self.outputs.append(wire)  # Add the output wire to the outputs list

    # Method to display information about the gate
    def get_info(self):
        wires_in_labels = [
            wire_in.label for wire_in in self.inputs
        ]  # List of input wire labels
        wires_out_labels = [
            wire_out.label for wire_out in self.outputs
        ]  # List of output wire labels
        output = (
            self.outputs[-1].value if self.outputs else 0
        )  # Last output value or 0 if no outputs

        # Print the gate information
        print("\nGate info:\n----------")
        print("Gate type:", self.gate_type)
        print("Inputs:", wires_in_labels)
        print("Outputs:", wires_out_labels)
        print("output", output)

    # Method to perform the logic operation of the gate
    def operate(self):
        # Implementing logic for different gate types
        if self.gate_type == "AND":
            output_value = (
                1 if all(wire.get_effective_value() == 1 for wire in self.inputs) else 0
            )

        elif self.gate_type == "OR":
            output_value = (
                1 if any(wire.get_effective_value() == 1 for wire in self.inputs) else 0
            )

        elif self.gate_type == "NAND":
            output_value = (
                0 if all(wire.get_effective_value() == 1 for wire in self.inputs) else 1
            )

        elif self.gate_type == "NOR":
            output_value = (
                0 if any(wire.get_effective_value() == 1 for wire in self.inputs) else 1
            )

        elif self.gate_type == "XOR":
            output_value = (
                1
                if sum(wire.get_effective_value() % 2 == 1 for wire in self.inputs)
                else 0
            )

        elif self.gate_type == "XNOR":
            output_value = 1 if sum(self.inputs.value) % 2 == 0 else 0

        # Setting the output value for all output wires
        for output in self.outputs:
            output.value = output_value


# Subclass for NOT gate, inheriting from Gate
class NotGate(Gate):
    # Constructor for NotGate class
    def __init__(self):
        super().__init__("NOT")  # Initialize with gate type "NOT"

    # Override the connect method for NOT gate
    def connect(self, inputs, outputs):
        # A NOT gate can only have one input and one or more outputs
        self.inputs.append(inputs[0])
        for output_wire in outputs:
            output_wire.connect(self)
            self.outputs.append(output_wire)

    # Override the operate method for NOT gate
    def operate(self):
        # NOT operation: invert the input value
        output_value = 0 if self.inputs[0].get_effective_value() == 1 else 1
        for output in self.outputs:
            output.value = output_value


# Subclass for BUFFER gate, inheriting from Gate
class BufferGate(Gate):
    # Constructor for BufferGate class
    def __init__(self):
        super().__init__("BUFFER")  # Initialize with gate type "BUFFER"

    # Override the connect method for BUFFER gate
    def connect(self, input_wire, output_wire):
        # A BUFFER gate can only have one input and one or more outputs
        self.inputs.append(input_wire)
        output_wire.connect(self)
        self.outputs.append(output_wire)

    # Override the operate method for BUFFER gate
    def operate(self):
        # BUFFER operation: pass the input value to the output
        output_value = self.inputs[0].get_effective_value()
        for output in self.outputs:
            output.value = output_value

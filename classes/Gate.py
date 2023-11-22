class Gate:
    # Characterizing gates by their type, number of fanins and fanouts
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.inputs = []
        self.outputs = []

    # Connecting each wire inputs to their outputs
    def connect(self, inputs, outputs):
        for wire in inputs:
            wire.connect(self)
            self.inputs.append(wire)

        # Can have more than 1 output in case of fanouts
        for wire in outputs:
            wire.connect(self)
            self.outputs.append(wire)

    # Although will never be used as the circuit will be automatically generated
    # I thought it would be fun to have this :)
    def disconnect(self, label):
        wire_found = False
        if not wire_found:
            for wire in self.inputs:
                if wire.label == label:
                    self.inputs.remove(wire)
                    wire_found = True
            for wire in self.outputs:
                if wire.label == label:
                    self.outputs.remove(wire)
                    wire_found = True
            # If trying to remove a wire not even connected to the gate
            if wire_found == False:
                print("This wire is not connected to this gate")

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
            if all(wire.get_effective_value == 1 for wire in self.inputs):
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
            if sum(wire.get_effective_value % 2 == 1 for wire in self.inputs):
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

    # To be developed later, maybe in a separate file to inject values
    # And maybe faults at the same token
    def set_input_vector(self, vector):
        for value in vector:
            for wire_in in self.inputs:
                if wire_in.is_input == True:
                    wire_in.set_single_input(value)

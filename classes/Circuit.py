from BenchmarkParsing import *
from classes.Wire import *
from classes.Gate import *


class Circuit:
    def __init__(self, file_path):
        self.parsed_file = parse_bench_file(file_path)
        print(self.parsed_file)

        self.circuitName = self.parsed_file["circuit_name"]
        self.gates = {}  # Dictionary to store Gate objects
        self.wires = {}  # Dictionary to store Wire objects
        self.input_count = 0
        self.output_count = 0
        self.create_circuit()

        self.expectedInput = []
        self.expectedOutput = []
        self.inputVector = []
        self.outputVector = []

    def create_circuit(self):
        # Create Wire objects for inputs, outputs, and internal connections
        self.input_count = self.parsed_file["inputs_count"]
        self.output_count = self.parsed_file["outputs_count"]
   
        for label in self.parsed_file["wires list"]:
            if str(label) in str(self.parsed_file["inputs"]):
                self.wires[str(label)] = Wire(str(label), is_input=True)
            elif str(label) in str(self.parsed_file["outputs"]):
                self.wires[str(label)] = Wire(str(label), is_output=True)
            else:
                self.wires[str(label)] = Wire(str(label))
        
     
        # Create Gate objects and connect wires
        for gate_label, gate_inputs in self.parsed_file["gates"].items():
            gate_type = self.parsed_file["gate_types"][str(gate_label)][1]
            if gate_type == "NOT":
                gate = NotGate()
            elif gate_type == "BUFFER":
                gate = BufferGate()
            else:
                gate = Gate(gate_type)

            self.inputs = [self.wires[(str(input_label))] for input_label in gate_inputs]
            
            # Check if there are any fanouts
            for input_label in gate_inputs:
                # print(input_label)
                # print(gate_label)
                if input_label.__contains__('-'):
                    if (gate_label == input_label.split('-')[0]):
                        self.outputs.append(self.wires[input_label])
                    else:
                        self.outputs = [self.wires[gate_label]]

            gate.connect(self.inputs, self.outputs)
            self.gates[gate_label] = gate

        # for output in self.gates.keys():
        #     for wire in self.gates[output].outputs:
        #         print(wire.label, wire.value)


    def pass_expected(self, expectedInputVector, expectedOutputVector):
        if len(expectedInputVector) != self.input_count:
            raise ValueError(
                "Expected Input Vector length does not match the number of input wires"
            )
        if len(expectedOutputVector) != self.output_count:
            raise ValueError(
                "Expected Output Vector length does not match the number of output wires"
            )
        self.expectedInput = expectedInputVector
        self.expectedOutput = expectedOutputVector
        print("Expected Input Vector: " + str(self.expectedInput))
        print("Expected Output Vector: " + str(self.expectedOutput))
        
    def set_input_values(self, input_vector):
        if len(input_vector) != self.input_count:
            raise ValueError(
                "Input Vector length does not match the number of input wires"
            )

        for index, wire_label in enumerate(self.parsed_file["inputs"]):
            # Check if the wire label has a fanout (indicated by a dash)
            # print("Dealing with wire:")
            # print(wire_label)
            if self.parsed_file["fanout_count"][wire_label] > 0:
                for i in range(1, self.parsed_file["fanout_count"][wire_label] + 1):
                # Iterate through the fanouts and set their values
                    fanout_wire = str(self.parsed_file["wires list"][self.parsed_file["wires list"].index(str(wire_label))+i])
                    self.wires[fanout_wire].set_single_input(input_vector[index])
                    # print(f"Wire {fanout_wire} value: {self.wires[str(fanout_wire)].value}")
            # else:
                # Set value for the wire label itself
            self.wires[str(wire_label)].set_single_input(input_vector[index])
                # print(f"Wire {wire_label} value: {self.wires[str(wire_label)].value}")


    def simulate(self):
        for gate_label in self.parsed_file["gates"]:

            self.gates[gate_label].operate()
            for output in self.gates[gate_label].outputs:
                if self.parsed_file["fanout_count"][int(output.label)] > 0:
                    for i in range(1, self.parsed_file["fanout_count"][int(output.label)] + 1):
                    # Iterate through the fanouts and set their values
                        fanout_wire = str(self.parsed_file["wires list"][self.parsed_file["wires list"].index(str(output.label))+i])
                        self.wires[fanout_wire].set_single_input(output.value)
                        # print(f"Wire {fanout_wire} value: {self.wires[str(fanout_wire)].value}")
                # for output in self.gates[gate_label].outputs:
                    # print('output label:')
                    # print(output.label)
                    # print('output value:')
                    # print(output.value)


    def compute_output(self):
        output_vector = []
        for output_label in self.parsed_file["outputs"]:
            output_vector.append(self.wires[str(output_label)].value)
        return output_vector

    def run_simulation(self, input_vector):
        self.set_input_values(input_vector)
        # print("Simulating for input vector", input_vector)
        self.simulate()
        return self.compute_output()

    # Preparing the graph by getting a dictionary of vertices and nodes
    def get_vertices(self):
        nodes = self.parsed_file["gates"].keys()  # The output wires
        values = self.parsed_file["gates"].values()  # The input wires
        gate_types = self.parsed_file[
            "gate_types"
        ].values()  # The gate types of each input-output pair

        vertices = []
        vertices_labels = {}
        counter = 0  # Counter

        for node, value, gate_type in zip(nodes, values, gate_types):
            # Check for the first input
            vertices.append([value[0], node])
            left_in = tuple(vertices[counter])
            vertices_labels[left_in] = (
                str(self.parsed_file["gate_types"][node][0])
                + "-"
                + str(self.parsed_file["gate_types"][node][1])
            )

            counter += 1

            # Do not check for the second input if the gate is a NOT or a BUFFER
            if gate_type[1] == "NOT" or gate_type[1] == "BUFFER":
                continue

            # Check for the second input otherwise
            else:
                vertices.append([value[1], node])
                right_in = tuple(vertices[counter])
                vertices_labels[right_in] = (
                    str(self.parsed_file["gate_types"][node][0])
                    + "-"
                    + str(self.parsed_file["gate_types"][node][1])
                )
                counter += 1

        return vertices_labels

    # Method to color code each node as 0 or 1 (representing wires)
    def get_colors(self):
        colors = {}
        for wire_label in self.wires.keys():
            if self.wires[wire_label].get_effective_value() == 1:
                colors[wire_label] = "green"
            else:
                colors[wire_label] = "red"
        return colors

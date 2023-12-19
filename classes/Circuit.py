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

        for label in (
            self.parsed_file["inputs"]
            + self.parsed_file["outputs"]
            + list(self.parsed_file["gates"].keys())
        ):
            is_input = label in self.parsed_file["inputs"]
            is_output = label in self.parsed_file["outputs"]
            self.wires[label] = Wire(label, is_input, is_output)

        # Create Gate objects and connect wires
        for gate_label, gate_inputs in self.parsed_file["gates"].items():
            gate_type = self.parsed_file["gate_types"][gate_label][1]
            if gate_type == "NOT":
                gate = NotGate()
            elif gate_type == "BUFFER":
                gate = BufferGate()
            else:
                gate = Gate(gate_type)

            self.inputs = [self.wires[input_label] for input_label in gate_inputs]
            self.outputs = [self.wires[gate_label]]

            gate.connect(self.inputs, self.outputs)
            self.gates[gate_label] = gate

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
            self.wires[wire_label].set_single_input(input_vector[index])

    def simulate(self):
        for gate_label in self.parsed_file["gates"]:
            self.gates[gate_label].operate()

    def compute_output(self):
        output_vector = []
        for output_label in self.parsed_file["outputs"]:
            output_vector.append(self.wires[output_label].value)
        return output_vector

    def run_simulation(self, input_vector):
        self.set_input_values(input_vector)
        print("Simulating for input vector", input_vector)
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

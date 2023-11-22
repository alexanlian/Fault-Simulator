from BenchmarkParsing import *
from classes.Wire import *
from classes.Gate import *

class Circuit:
    def __init__(self, file_path):
        self.parsed_file = parse_bench_file(file_path)
        print(self.parsed_file)

        self.gates = {}  # Dictionary to store Gate objects
        self.wires = {}  # Dictionary to store Wire objects
        self.create_circuit()

        self.expectedInput = []
        self.expectedOutput = []
        self.inputVector = []
        self.outputVector = []

    def create_circuit(self):
        # Create Wire objects for inputs, outputs, and internal connections
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
            gate_type = self.parsed_file["gate_types"][gate_label]
            gate = Gate(gate_type)

            inputs = [self.wires[input_label] for input_label in gate_inputs]
            outputs = [self.wires[gate_label]]

            gate.connect(inputs, outputs)
            self.gates[gate_label] = gate

    def pass_expected(self, expectedInputVector, expectedOutputVector):
        self.expectedInput = expectedInputVector
        self.expectedOutput = expectedOutputVector
        print("Expected Input Vector: " + str(self.expectedInput))
        print("Expected Output Vector: " + str(self.expectedOutput))

    def set_input_values(self, input_vector):
        if len(input_vector) != len(self.parsed_file["inputs"]):
            raise ValueError(
                "Input vector length does not match the number of input wires"
            )

        for idx, wire_label in enumerate(self.parsed_file["inputs"]):
            self.wires[wire_label].set_single_input(input_vector[idx])

    def simulate(self):
        # It's important to order the gates according to their dependencies
        # For simplicity, we assume that the gates are listed in a topologically sorted manner in the benchmark
        for gate_label in self.parsed_file["gates"]:
            self.gates[gate_label].operate()

    def compute_output(self):
        output_vector = []
        for output_label in self.parsed_file["outputs"]:
            output_vector.append(self.wires[output_label].value)
        return output_vector

    def run_simulation(self, input_vector):
        self.set_input_values(input_vector)
        self.simulate()
        return self.compute_output()

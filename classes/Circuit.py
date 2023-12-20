from BenchmarkParsing import *
from classes.Wire import *
from classes.Gate import *


class Circuit:
    # Constructor for the Circuit class
    def __init__(self, file_path):
        self.parsed_file = parse_bench_file(file_path)  # Parse the circuit file
        print(self.parsed_file)  # Print the parsed file content

        self.circuitName = self.parsed_file["circuit_name"]  # Name of the circuit
        self.gates = {}  # Dictionary to store Gate objects
        self.wires = {}  # Dictionary to store Wire objects
        self.input_count = 0  # Number of input wires
        self.output_count = 0  # Number of output wires
        self.create_circuit()  # Method to create the circuit

        # Initialize vectors for expected and actual input/output values
        self.expectedInput = []
        self.expectedOutput = []
        self.inputVector = []
        self.outputVector = []

    # Method to create the circuit based on the parsed file
    def create_circuit(self):
        # Initialize input and output counts
        self.input_count = self.parsed_file["inputs_count"]
        self.output_count = self.parsed_file["outputs_count"]

        # Create Wire objects for all wires in the circuit
        for label in self.parsed_file["wires list"]:
            if str(label) in str(self.parsed_file["inputs"]):
                self.wires[str(label)] = Wire(str(label), is_input=True)
            elif str(label) in str(self.parsed_file["outputs"]):
                self.wires[str(label)] = Wire(str(label), is_output=True)
            else:
                self.wires[str(label)] = Wire(str(label))

        # Create Gate objects and connect the wires to these gates
        for gate_label, gate_inputs in self.parsed_file["gates"].items():
            gate_type = self.parsed_file["gate_types"][str(gate_label)][1]
            # Instantiate the appropriate gate type
            if gate_type == "NOT":
                gate = NotGate()
            elif gate_type == "BUFFER":
                gate = BufferGate()
            else:
                gate = Gate(gate_type)

            self.inputs = [self.wires[str(input_label)] for input_label in gate_inputs]
            self.outputs = []  # Initialize outputs list

            # Connecting wires to the gate, handling fanouts if present
            for input_label in gate_inputs:
                if "-" in input_label:
                    if gate_label == input_label.split("-")[0]:
                        self.outputs.append(self.wires[input_label])
                    else:
                        self.outputs = [self.wires[gate_label]]

            gate.connect(self.inputs, self.outputs)
            self.gates[gate_label] = gate

    # Method to pass the expected input and output vectors for the circuit
    def pass_expected(self, expectedInputVector, expectedOutputVector):
        # Validate the length of the input and output vectors
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

    # Method to set the input values for the circuit
    def set_input_values(self, input_vector):
        # Validate the length of the input vector
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


    # Method to simulate the circuit
    def simulate(self):
        for gate_label in self.parsed_file["gates"]:
            self.gates[gate_label].operate()
            # Set output values for the gates and their fanouts
            for output in self.gates[gate_label].outputs:
                if self.parsed_file["fanout_count"][int(output.label)] > 0:
                    for i in range(
                        1, self.parsed_file["fanout_count"][int(output.label)] + 1
                    ):
                        fanout_wire = str(
                            self.parsed_file["wires list"][
                                self.parsed_file["wires list"].index(str(output.label))
                                + i
                            ]
                        )
                        self.wires[fanout_wire].set_single_input(output.value)

    # Method to compute the output vector of the circuit
    def compute_output(self):
        output_vector = [
            self.wires[str(output_label)].value
            for output_label in self.parsed_file["outputs"]
        ]
        return output_vector

    # Method to run the simulation for a given input vector
    def run_simulation(self, input_vector):
        self.set_input_values(input_vector)
        self.simulate()
        return self.compute_output()
    
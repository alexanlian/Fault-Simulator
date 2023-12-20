from BenchmarkParsing import parse_bench_file
import matplotlib.pyplot as plt
from classes.Gate import Gate, NotGate, BufferGate
from classes.Wire import Wire
from classes.Circuit import Circuit
from classes.FaultSimulation import FaultSimulator
from classes.CircuitGraph import CircuitGraph

# Create a circuit instance by parsing a benchmark file
circuitExample = Circuit("bench-files\c17.bench.txt")
# Display information about the number of inputs and outputs in the circuit
print(
    "This circuit has",
    circuitExample.input_count,
    "inputs and ",
    circuitExample.output_count,
    "outputs.",
)

# Ask the user to enter an input vector for the circuit
print("Please enter your input vector:")
input_vector = []
for count in range(circuitExample.input_count):
    # Loop to ensure correct input (either 0 or 1) for each input
    while True:
        user_input = input(f"Input#{count + 1}: ")
        if len(user_input) == 1 and user_input in "01":
            input_vector.append(int(user_input))
            break
        else:
            print("Please enter either 0 or 1 only.")

# Run the circuit simulation with the provided input vector and display results
output_vector = circuitExample.run_simulation(input_vector)
print("Simulation Results without Faults:", output_vector)

# Pass the input and output vectors to the circuit for expected results
circuitExample.pass_expected(input_vector, output_vector)

# Display labels and values of all wires in the circuit
for wire in circuitExample.wires.keys():
    print("labels and values")
    print(circuitExample.wires[wire].label, circuitExample.wires[wire].value)

# Define a list of faults to simulate
fault_list = ["1", "2"]
# Create an instance of the FaultSimulator
fault_sim = FaultSimulator(circuitExample)
# Run the fault simulation and print the results
fault_sim.run_fault_simulation(fault_list)

# visualize the circuit using CircuitGraph
# graph = CircuitGraph(circuitExample)
# graph.draw_topological_graph()

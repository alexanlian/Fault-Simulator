from BenchmarkParsing import parse_bench_file
import matplotlib.pyplot as plt
from classes.Gate import Gate, NotGate, BufferGate
from classes.Wire import Wire
from classes.Circuit import Circuit
from classes.FaultSimulation import FaultSimulator
from classes.CircuitGraph import CircuitGraph

# testing circuit creation
circuitExample = Circuit("bench-files\c17.bench.txt")
print(
    "This circuit has",
    circuitExample.input_count,
    "inputs and ",
    circuitExample.output_count,
    "outputs.",
)
print("Please enter your input vector:")
input_vector = []
for count in range(circuitExample.input_count):
    while True:
        user_input = input(f"Input#{count + 1}: ")
        if len(user_input) == 1 and user_input in "01":
            input_vector.append(int(user_input))
            break
        else:
            print("Please enter either 0 or 1 only.")

# Run the simulation without faults
output_vector = circuitExample.run_simulation(input_vector)
print("Simulation Results without Faults:", output_vector)
circuitExample.pass_expected(input_vector, output_vector)
for wire in circuitExample.wires.keys():
    print("labels and values")
    print(circuitExample.wires[wire].label, circuitExample.wires[wire].value)


# fault_list = ['1','2']
# fault_sim = FaultSimulator(circuitExample)
# print(fault_sim.run_fault_simulation(fault_list))

# graph = CircuitGraph(circuitExample)
# graph.draw_topological_graph()

from BenchmarkParsing import parse_bench_file
import matplotlib.pyplot as plt
from classes.Gate import Gate
from classes.Wire import Wire
from classes.Circuit import Circuit
from classes.FaultSimulation import FaultSimulator
import time

# testing circuit creation
circuitExample = Circuit("bench-files\c17.bench.txt")
circuitExample.pass_expected([1, 0, 1, 1, 0], [1, 0])

# Run the simulation without faults
results = circuitExample.run_simulation([1, 0, 1, 1, 0])
print("Simulation Results without Faults:", results)

fault_simulator = FaultSimulator(circuitExample)

# Define a list of faults
fault_list = [
    # Format: (wire_label, stuck_at_value)
    (3, 0),  # Wire 3 stuck-at-0
    (6, 1),  # Wire 6 stuck-at-1
    # Add more faults as needed
]

# Run the fault simulation
simulation_time, fault_coverage = fault_simulator.run_fault_simulation(
    fault_list, [[1, 0, 1, 1, 0]]
)

# Display the results
print("Simulation Time:", simulation_time)
print("Fault Coverage:", fault_coverage)

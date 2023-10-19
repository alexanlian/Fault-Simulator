from BenchmarkParsing import parse_bench_file
import networkx as nx
import matplotlib.pyplot as plt

from classes.Gate import Gate
from classes.Wire import Wire


# Specify the file path for c17
file_path = "bench-files\c17.bench.txt"

# Parse the bench file and print the parsed information
parsed_file = parse_bench_file(file_path)

print("Parsed information:")
print(parsed_file)


# Simulation of connecting 2 wires to an AND gate
gate1 = Gate('AND')
wire0 = Wire('0', is_input=True)
wire1 = Wire('1', is_input=True)
wire10 = Wire('10', is_output=True)
gate1.connect([wire0, wire1], [wire10])
gate1.get_info()
wire1.get_connections()
wire0.set_single_input(1)
wire1.set_single_input(0)
gate1.operate()
gate1.get_info()

# Simulation of connecting an existing wire with a new one to an OR gate
gate2 = Gate('OR')
wire2 = Wire('2', is_input=True)
wire12 = Wire('12', is_output=True)
wire2.set_single_input(1)
gate2.connect([wire1, wire2], [wire12])
gate2.operate()
gate2.get_info()

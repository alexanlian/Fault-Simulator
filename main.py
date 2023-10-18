def parse_bench_file(file_path):
    # Open the specified file in read mode
    with open(file_path, 'r') as file:
        # Read the content of the file
        file_content = file.read()

    # Initialize lists and counters to store information
    inputs = []  # List to store input numbers
    outputs = []  # List to store output numbers
    inverters_count = 0  # Initialize inverter count
    gates = {}  # Dictionary to store gate expressions

    # Iterate through each line in the file
    for line in file_content.split('\n'):
        line = line.strip()  # Remove leading and trailing whitespaces

        # Check if the line starts with 'INPUT'
        if line.startswith('INPUT'):
            # Extract the input number and add it to the inputs list
            inputs.append(int(line.split('(')[1].split(')')[0]))

        # Check if the line starts with 'OUTPUT'
        elif line.startswith('OUTPUT'):
            # Extract the output number and add it to the outputs list
            outputs.append(int(line.split('(')[1].split(')')[0]))

        # Check if the line starts with '#', indicating metadata
        elif line.startswith('#'):
            parts = line.split(' ')
            if parts[1].lower() == 'inverter':
                # Extract the inverter count from the metadata
                inverters_count = int(parts[2])

        # Check if the line contains a gate assignment
        elif line and '=' in line:
            parts = line.split('=')
            # Extract the gate number and gate expression
            gate_number = int(parts[0].strip())
            gate_expression = parts[1].strip().replace(' ', '').split('(')[1].split(')')[0]
            # Store the gate expression in the gates dictionary
            gates[gate_number] = gate_expression

    # Return a dictionary containing the parsed information
    return {
        "inputs": inputs,
        "outputs": outputs,
        "inverters": inverters_count,
        "gates": gates
    }


# Specify the file path for c17
c17_file_path = "BENCH files\c17.bench.txt"

# Parse the bench file and print the parsed information
parsed_c17 = parse_bench_file(c17_file_path)

print("Parsed c17 information:")
print(parsed_c17)

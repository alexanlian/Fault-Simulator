def parse_bench_file(file_path):
    # Open the specified file in read mode
    with open(file_path, "r") as file:
        # Read the content of the file
        file_content = file.read()

    # Initialize lists and counters to store information
    circuit_name = ""
    inputs_count = 0
    outputs_count = 0
    inputs = []  # List to store input numbers
    outputs = []  # List to store output numbers
    inverters_count = 0  # Initialize inverter count
    gates = {}  # Dictionary to store gate expressions and types
    wires = []

    # Define a dictionary to map gate numbers to gate types
    gate_types = {}
    gate_counter = 1

    # Iterate through each line in the file
    for line in file_content.split("\n"):
        line = line.strip()  # Remove leading and trailing whitespaces

        if line.startswith("# c"):
            circuit_name = str(line[2:])

        if line.endswith("inputs"):
            inputs_count = int(line[2:].replace(' inputs',''))

        if line.endswith("outputs"):
            outputs_count = int(line[2].replace(' inputs',''))

        # Check if the line starts with 'INPUT'
        if line.startswith("INPUT"):
            # Extract the input number and add it to the inputs list
            inputs.append(int(line.split("(")[1].split(")")[0]))
            wires.append(int(line.split("(")[1].split(")")[0]))

        # Check if the line starts with 'OUTPUT'
        elif line.startswith("OUTPUT"):
            # Extract the output number and add it to the outputs list
            outputs.append(int(line.split("(")[1].split(")")[0]))

        # Check if the line starts with '#', indicating metadata
        elif line.startswith("#"):
            parts = line.split(" ")
            if parts[1].lower() == "inverter":
                # Extract the inverter count from the metadata
                inverters_count = int(parts[2])

        # Check if the line contains a gate assignment
        elif line and "=" in line:
            parts = line.split("=")
            # Extract the gate number, gate expression, and gate type
            gate_number = int(parts[0].strip())  # Convert gate_number to an integer
            gate_info = parts[1].strip().split("(")
            gate_type = gate_info[0]
            gate_expression = (
                gate_info[1].split(")")[0].split(",")
            )  # Convert to a list of integers
            gate_expression = [
                int(x) for x in gate_expression
            ]  # Convert each element to an integer
            # Store the gate expression and type in the gates dictionary
            gates[gate_number] = gate_expression  # Store as a list of integers
            gate_types[gate_number] = [str(gate_counter), gate_type]
            gate_counter += 1
            
            wires.append(gate_number)
            for fan_ins in gates.values():
                fan_out_counter = 0
                for fan_in in fan_ins:
                    print(fan_in)
                    if gate_number == fan_in:
                        wires.append(str(str(gate_number)+"-"+fan_out_counter))
                        fan_out_counter += 1

            

    # Return a dictionary containing the parsed information
    return {
        "netlist": wires,
        "circuit_name": circuit_name,
        "inputs_count": inputs_count,
        "outputs_count": outputs_count,
        "inputs": inputs,
        "outputs": outputs,
        "inverters": inverters_count,
        "gates": gates,
        "gate_types": gate_types,  # Include gate types in the result
    }

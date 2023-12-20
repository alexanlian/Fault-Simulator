def parse_bench_file(file_path):
    # Open the specified file in read mode
    with open(file_path, "r") as file:
        # Read the entire content of the file into a string
        file_content = file.read()

    # Initialize variables to store circuit information
    circuit_name = ""  # Name of the circuit
    inputs_count = 0  # Number of inputs
    outputs_count = 0  # Number of outputs
    inputs = []  # List to store input identifiers
    outputs = []  # List to store output identifiers
    inverters_count = 0  # Number of inverters
    gates = {}  # Dictionary to store gate information
    wires = {}  # Dictionary to store wire (netlist) information
    fanout_count = {}  # Dictionary to track the fanout of each wire

    # Dictionary to map gate numbers to their types
    gate_types = {}
    gate_counter = 1  # Counter for gate numbers

    # Initialize a dictionary to track wires and fanouts
    wire_tracker = {}
    wire_list = []

    # Process each line in the file content
    for line in file_content.split("\n"):
        line = line.strip()  # Remove leading/trailing whitespace

        # Parse the circuit name
        if line.startswith("# c"):
            circuit_name = str(line[2:])

        # Parse the number of inputs
        if line.endswith("inputs"):
            inputs_count = int(line[2:].replace(" inputs", ""))

        # Parse the number of outputs
        if line.endswith("outputs"):
            outputs_count = int(line[2:].replace(" outputs", ""))

        # Parse inputs
        if line.startswith("INPUT"):
            inputs.append(int(line.split("(")[1].split(")")[0]))

        # Parse outputs
        elif line.startswith("OUTPUT"):
            outputs.append(int(line.split("(")[1].split(")")[0]))

        # Parse metadata about inverters
        elif line.startswith("#"):
            parts = line.split(" ")
            if parts[1].lower() == "inverter":
                inverters_count = int(parts[2])

        # Parse gate definitions
        elif line and "=" in line:
            parts = line.split("=")
            gate_number = int(parts[0].strip())
            gate_info = parts[1].strip().split("(")
            gate_type = gate_info[0]
            gate_expression = [int(x) for x in gate_info[1].split(")")[0].split(",")]

            # Store gate expression and type
            gates[gate_number] = gate_expression
            gate_types[str(gate_number)] = [str(gate_counter), gate_type]
            gate_counter += 1

    # Count the fan-ins for each wire
    for gate_expression in gates.values():
        for fan_in in gate_expression:
            if fan_in not in wire_tracker:
                wire_tracker[fan_in] = 1
            else:
                wire_tracker[fan_in] += 1

    # Set the output wires fan-in count to 1
    for output_wire in outputs:
        wire_tracker[output_wire] = 1

    # Update wire tracker for wires with only one connection
    for wire in wire_tracker.keys():
        if wire_tracker[wire] == 1:
            wire_tracker[wire] = 0

    # Copy the wire tracker to fanout counter
    fanout_counter = wire_tracker.copy()

    # Create a list of wires and their fanouts
    for wire in wire_tracker.keys():
        if wire_tracker[wire] == 0:
            wire_list.append(str(wire))
        else:
            wire_list.append(str(wire))
            for fan_out_count in range(wire_tracker[wire]):
                wire_list.append(str(wire) + "-" + str(fan_out_count + 1))

    # Update gates with fanout information
    for key in gates.keys():
        for index, value in enumerate(gates[key]):
            if wire_tracker[value] > 0:
                gates[key][index] = wire_list[
                    wire_list.index(str(value)) + (wire_tracker[value] - 1)
                ]
                wire_tracker[value] += 1

    # Convert gates dictionary to use string keys and values
    updated_gates = {}
    for key, value in gates.items():
        str_key = str(key)
        str_values = [str(val) if isinstance(val, int) else val for val in value]
        updated_gates[str_key] = str_values

    # Update the gates dictionary and clean up
    gates = updated_gates
    del updated_gates

    # Return the parsed circuit information as a dictionary
    return {
        "circuit_name": circuit_name,
        "inputs_count": inputs_count,
        "outputs_count": outputs_count,
        "fanout_count": fanout_counter,
        "inputs": inputs,
        "outputs": outputs,
        "inverters": inverters_count,
        "wires list": wire_list,
        "gates": gates,
        "gate_types": gate_types,
    }

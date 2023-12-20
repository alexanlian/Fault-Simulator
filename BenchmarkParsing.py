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
    wires = {}  # Dictionary to store wires (netlist)
    fanout_count = {}  # Dictionary to keep count of fanouts

    # Define a dictionary to map gate numbers to gate types
    gate_types = {}
    gate_counter = 1

    gate_expressions = []
    # Iterate through each line in the file
    for line in file_content.split("\n"):
        line = line.strip()  # Remove leading and trailing whitespaces

        if line.startswith("# c"):
            circuit_name = str(line[2:])

        if line.endswith("inputs"):
            inputs_count = int(line[2:].replace(" inputs", ""))

        if line.endswith("outputs"):
            outputs_count = int(line[2].replace(" inputs", ""))

        # Check if the line starts with 'INPUT'
        if line.startswith("INPUT"):
            # Extract the input number and add it to the inputs list
            inputs.append(int(line.split("(")[1].split(")")[0]))

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
            print("gate expression")
            print(gate_expression)
            # Store the gate expression and type in the gates dictionary
            gates[gate_number] = gate_expression  # Store as a list of integers
            gate_types[str(gate_number)] = [str(gate_counter), gate_type]
            gate_counter += 1

    wire_tracker = {}
    wire_list = []
    for gate_expression in gates.values():
        for fan_in in gate_expression:
            if fan_in not in wire_tracker:
                wire_tracker[fan_in] = 1
            else:
                wire_tracker[fan_in] += 1
    for output_wire in outputs:
        wire_tracker[output_wire] = 1

    for wire in wire_tracker.keys():
        if wire_tracker[wire] == 1:
            wire_tracker[wire] = 0

    print("Wire_tracker")
    print(wire_tracker)

    for wire in wire_tracker.keys():
        if wire_tracker[wire] == 0:
            wire_list.append(str(wire))
        else:
            wire_list.append(str(wire))
            for fan_out_count in range(wire_tracker[wire]):
                wire_list.append(str(wire) + "-" + str(fan_out_count + 1))

    for key in gates.keys():
        for index, value in enumerate(gates[key]):
            if wire_tracker[value] > 0:
                gates[key][index] = wire_list[
                    wire_list.index(str(value)) + (wire_tracker[value] - 1)
                ]
                wire_tracker[value] += 1

    updated_gates = {}
    for key, value in gates.items():
        str_key = str(key)  # Convert key to string
        str_values = [
            str(val) if isinsFtance(val, int) else val for val in value
        ]  # Convert integers in values to strings
        updated_gates[str_key] = str_values

    gates = updated_gates
    del updated_gates

    # Return a dictionary containing the parsed information
    return {
        # "gate_expressions": gate_expressions,
        "circuit_name": circuit_name,
        "inputs_count": inputs_count,
        "outputs_count": outputs_count,
        "inputs": inputs,
        "outputs": outputs,
        "inverters": inverters_count,
        "wires list": wire_list,
        "gates": gates,
        "gate_types": gate_types,  # Include gate types in the result
    }

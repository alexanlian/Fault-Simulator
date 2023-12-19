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
            gate_types[gate_number] = [str(gate_counter), gate_type]
            gate_counter += 1

            gate_expressions.append(gate_expression)

        #     # Update 'wires' dictionary with the gate output
            
        #     if str(gate_number) not in wires:
        #         wires[str(gate_number)] = True
        #         fanout_count[gate_number] = 0
        #     else:
        #         # Handling fanouts for the gate output
        #         fanout_count[gate_number] += 1
        #         wires[str(gate_number)+"-"+str(fanout_count[gate_number])] = True
              

        # # Update 'wires' dictionary with the gate inputs
        # for gate_expression in gate_expressions:
        #     for wire in gate_expression:
        #         if str(wire) not in wires:
        #             wires[str(wire)] = True
        #             fanout_count[wire] = 0
        #         else:
        #             # Handling fanouts for the gate inputs
        #             fanout_count[wire] += 1
        #             wires[str(wire)+"-"+str(fanout_count[wire])] = True
        #             if fanout_count[wire] == 2:
        #                 wires[str(wire)+"-"+str(fanout_count[wire]+1)] = True
        
    wire_tracker = {}
    wire_list = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for gate_expression in gate_expressions:
        for fan_in in gate_expression:
            if fan_in not in wire_tracker:
                wire_tracker[fan_in] = 1
            else:
                wire_tracker[fan_in] += 1
    print(wire_tracker)

    for wire in wire_tracker.keys():
        if wire_tracker[wire] == 1:
            wire_list.append(str(wire))
        else:
            wire_list.append(str(wire))
            for fan_out_count in range(wire_tracker[wire]):
                wire_list.append(str(wire)+str(alphabet[fan_out_count]))

    print(wire_list)
    # Return a dictionary containing the parsed information
    return {
        "gate_expressions": gate_expressions,
        "circuit_name": circuit_name,
        "inputs_count": inputs_count,
        "outputs_count": outputs_count,
        "inputs": inputs,
        "outputs": outputs,
        "inverters": inverters_count,
        "wires keys": wire_list,
        "fanout_count": fanout_count,
        "gates": gates,
        "gate_types": gate_types,  # Include gate types in the result
    }

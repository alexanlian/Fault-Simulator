class Wire:
    # Constructor for Wire class
    def __init__(self, label, is_input=False, is_output=False):
        self.label = label  # Label or identifier of the wire
        self.value = None  # Logical value carried by the wire (e.g., 0 or 1)
        self.is_input = is_input  # Flag to indicate if it's a primary input
        self.is_output = is_output  # Flag to indicate if it's a primary output
        self.connections = []  # List of gates to which this wire is connected
        self.fault = None  # Stores fault condition, if any (for fault analysis)

    # Method to connect a wire to a gate
    def connect(self, gate):
        self.connections.append(gate)  # Add the gate to the wire's connections list

    # Method to print the types of gates a wire is connected to
    def get_connections(self):
        for gate in self.connections:
            print(gate.gate_type)  # Print the type of each connected gate

    # Method to set the value of the wire
    def set_single_input(self, value):
        # Set the wire's value, primarily used for input wires
        self.value = value

    # Method to inject a fault into the wire
    def inject_fault(self, fault):
        self.fault = fault  # Set the fault condition (e.g., stuck-at fault)

    # Method to get the effective value of the wire
    def get_effective_value(self):
        # Return the fault value if a fault is injected, else return the actual value
        if self.fault is not None:
            return self.fault  # If there's a fault, return the fault value
        return self.value  # Otherwise, return the wire's actual value

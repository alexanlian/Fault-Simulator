class Wire:
    # Characterized by its value, label, if it's a primary input, a primary output or neither
    # Later on we add if there's a fault or not
    def __init__(self, label, is_input=False, is_output=False):
        self.label = label
        self.value = None
        self.is_input = is_input
        self.is_output = is_output
        self.connections = []
        self.fault = None

    # Register which gates this wire is connected to
    def connect(self, gate):
        self.connections.append(gate)

    # Get the gates by their types
    def get_connections(self):
        for gate in self.connections:
            print(gate.gate_type)

    # Set the inputs value
    # Again might be put in a separate file for setting values later on
    def set_single_input(self, value):
        if self.is_input == True:
            self.value = value
        else:
            print("Cannot set the value of a non-input wire")

    def inject_fault(self, fault):
        self.fault = fault

    def get_effective_value(self):
        if self.fault is not None:
            return self.fault  # stuck-at fault value
        return self.value
    
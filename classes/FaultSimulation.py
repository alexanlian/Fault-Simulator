import time

class FaultSimulator:
    def __init__(self, circuit):
        self.circuit = circuit

    def run_fault_simulation(self, fault_list, input_vectors):
        start_time = time.time()

        original_outputs = []
        fault_outputs = {fault: [] for fault in fault_list}

        # Run the circuit without faults
        for vector in input_vectors:
            self.circuit.set_input_values(vector)
            self.circuit.simulate()
            original_outputs.append(self.circuit.compute_output())

        # Run the circuit with each fault
        for fault in fault_list:
            wire_label, fault_value = fault
            self.circuit.wires[wire_label].inject_fault(fault_value)

            for vector in input_vectors:
                self.circuit.set_input_values(vector)
                self.circuit.simulate()
                fault_outputs[fault].append(self.circuit.compute_output())

            # Reset the fault for the next iteration
            self.circuit.wires[wire_label].inject_fault(None)

        end_time = time.time()
        simulation_time = end_time - start_time

        # Calculate fault coverage
        fault_coverage = self.calculate_fault_coverage(original_outputs, fault_outputs)

        return simulation_time, fault_coverage

    def calculate_fault_coverage(self, original_outputs, fault_outputs):
        detected_faults = 0

        for fault, outputs_with_fault in fault_outputs.items():
            # Iterate over each set of outputs with the given fault
            for i, fault_output in enumerate(outputs_with_fault):
                # Compare the fault output with the original output
                if fault_output != original_outputs[i]:
                    detected_faults += 1
                    break  # Move to the next fault once one detection is made

        total_faults = len(fault_outputs)
        if total_faults == 0:
            return 0  # Avoid division by zero

        fault_coverage = detected_faults / total_faults
        return fault_coverage

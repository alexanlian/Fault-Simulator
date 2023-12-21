import time
import math

class FaultSimulator:
    # Constructor for FaultSimulator class
    def __init__(self, circuit):
        self.circuit = circuit  # The circuit on which fault simulation is performed

    # Method to generate all possible input patterns based on the number of inputs
    def generate_input_patterns(self):
        pattern_count = int(
            math.pow(2, self.circuit.input_count)
        )  # Calculate the total number of patterns
        patterns = []  # List to hold integer representations of patterns
        patterns_str = []  # List to hold string representations of patterns

        for i in range(pattern_count):
            pattern = format(
                i, "0" + str(self.circuit.input_count) + "b"
            )  # Generate binary pattern
            patterns_str.append(pattern)  # Add string representation
            pattern_array = [
                int(bit) for bit in pattern
            ]  # Convert to array of integers
            patterns.append(pattern_array)  # Add integer representation
        return patterns, patterns_str

    # Method to run fault simulation given a list of faults
    def run_fault_simulation(self, fault_list):
        start_time = time.time()  # Start time of the simulation

        # Generate input patterns for the simulation
        input_patterns, patterns_str = self.generate_input_patterns()

        # Initialize dictionaries to store fault-free and faulty outputs
        fault_free_outputs = {}
        fault_sim_stats = {}

        # Run simulation for each input pattern and store fault-free outputs
        for pattern_list, pattern_str in zip(input_patterns, patterns_str):
            current_output = self.circuit.run_simulation(pattern_list)
            fault_free_outputs[pattern_str] = current_output
            fault_sim_stats[pattern_str] = [current_output]

        # Initialize counters for detected and undetectable faults
        detected_faults = 0
        undetectable_faults = 0

        # Fault Injection and Simulation
        for fault in fault_list:
            fault_detected = False
            for stuck_at_fault in range(
                2
            ):  # Test for both stuck-at-0 and stuck-at-1 faults
                for pattern_list, pattern_str in zip(input_patterns, patterns_str):
                    # Inject fault into the circuit
                    original_value = self.circuit.wires[fault].value
                    self.circuit.wires[fault].inject_fault(stuck_at_fault)

                    # Run simulation with the injected fault
                    faulty_output = self.circuit.run_simulation(pattern_list)

                    # Compare faulty output with fault-free output to detect faults
                    if faulty_output != fault_free_outputs[pattern_str]:
                        fault_detected = True
                        fault_sim_stats[pattern_str].append(
                            (fault, "stuck-at-" + str(stuck_at_fault), faulty_output)
                        )
                        break

                # Update counters based on fault detection
                if fault_detected:
                    detected_faults += 1
                else:
                    undetectable_faults += 1

            # Restore original wire value after testing each fault
            self.circuit.wires[fault].value = original_value

        # Calculate Fault Coverage and Fault Efficiency
        fault_coverage = detected_faults / (2 * len(fault_list))

        fault_efficiency = (
            detected_faults / ((2 * len(fault_list)) - undetectable_faults)
            if undetectable_faults != len(fault_list)
            else float("inf")
        )

        # Measure total simulation time
        end_time = time.time()
        simulation_time = end_time - start_time

        # Return simulation results

        print("Fault Simulation Stats: ")
        print(fault_sim_stats)

        print("Detected Faults:", detected_faults)

        print("Undetectable Faults:", undetectable_faults)

        print("Simulation Time:", simulation_time)

        print("Fault Coverage:", fault_coverage)

        print("Fault Efficiency:", fault_efficiency)

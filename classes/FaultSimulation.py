import time
import math


class FaultSimulator:
    def __init__(self, circuit):
        self.circuit = circuit

    def generate_input_patterns(self):
        pattern_count = int(math.pow(2, self.circuit.input_count))
        patterns = []
        patterns_str = []
        for i in range(pattern_count):
            pattern = format(i, "0" + str(self.circuit.input_count) + "b")
            # Convert the string pattern to an array of integers
            patterns_str.append(pattern)
            pattern_array = [int(bit) for bit in pattern]
            patterns.append(pattern_array)
        return patterns, patterns_str

    def run_fault_simulation(self, fault_list):
        start_time = time.time()
     
        # Generate input patterns
        input_patterns, patterns_str = self.generate_input_patterns()

        # Run fault-free simulation
        fault_free_outputs = {}
        fault_sim_stats = {}
        print("input_patterns")
        print(patterns_str)
        for pattern_list, pattern_str in zip(input_patterns, patterns_str):
            current_output = self.circuit.run_simulation(pattern_list)
            fault_free_outputs[pattern_str] = current_output
            # print("current output")
            # print(current_output)
            fault_sim_stats[pattern_str] = [current_output]

        # Initialize counters for detected and undetectable faults
        detected_faults = 0
        undetectable_faults = 0

        # Fault Injection and Simulation
        for fault in fault_list:
            fault_detected = False
            for stuck_at_fault in range(2):
                for pattern_list, pattern_str in zip(input_patterns, patterns_str):
                    # Modify the circuit for the current fault
                    original_value = self.circuit.wires[fault].value
                    print("original value: " + str(original_value))

                    # Modify the circuit for the current fault
                    self.circuit.wires[fault].inject_fault(stuck_at_fault)
                    print("Injected fault " + str(self.circuit.wires[fault].value))

                    # Run simulation with fault
                    faulty_output = self.circuit.run_simulation(pattern_list)
                    print("for pattern " + pattern_str)
                    print("faulty_output is :")
                    print(faulty_output)
                    # Compare with fault-free output
                    if faulty_output != fault_free_outputs[pattern_str]:
                        fault_detected = True
                        print("fault is detected here")
                        fault_sim_stats[pattern_str].append((fault, "stuck-at-"+str(stuck_at_fault),faulty_output))
                        break

                if fault_detected:
                    detected_faults += 1
                    print("number of faults detected so far: " + str(detected_faults))
                else:
                    undetectable_faults += 1
                    print("number of faults not detectable so far: " + str(undetectable_faults))

            self.circuit.wires[fault].value = original_value

        # Calculating Fault Coverage and Efficiency
        fault_coverage = detected_faults / len(fault_list)
        fault_efficiency = detected_faults / (len(fault_list) - undetectable_faults)

        # Measure simulation time
        end_time = time.time()
        simulation_time = end_time - start_time

        print(fault_sim_stats)

        return {
            "Detected faults: ": detected_faults,
            "Undetectable faults: ": undetectable_faults,
            "Simulation Time": simulation_time,
            "Fault Coverage": fault_coverage,
            "Fault Efficiency": fault_efficiency,
        }

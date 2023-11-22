from BenchmarkParsing import parse_bench_file


class Circuit:
    def __init__(self, file_path):
        self.parsed_file = parse_bench_file(file_path)
        print(self.parsed_file)
        self.expectedInput = []
        self.expectedOutput = []
        self.inputVector = []
        self.outputVector = []

    def pass_expected(self, expectedInputVector, expectedOutputVector):
        self.expectedInput = expectedInputVector
        self.expectedOutput = expectedOutputVector
        print("Expected Input Vector: " + str(self.expectedInput))
        print("Expected Output Vector: " + str(self.expectedOutput))

    def simulate(self, inputVector):
        self.inputVector = inputVector
        
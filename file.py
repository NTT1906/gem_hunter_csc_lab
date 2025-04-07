from pathlib import Path

def process_file(input_path):
    input_path = Path(input_path)
    return input_path.with_name('output_' + input_path.stem[6:] + input_path.suffix)

# Example usage
process_file('path/to/input_abcd.txt')
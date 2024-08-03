import json
from deepdiff import DeepDiff

def compare_json_files(file1_path, file2_path):
    # Load the two JSON files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    # Compare the JSON data
    diff = DeepDiff(data1, data2, ignore_order=True)

    if not diff:
        return True, "JSON files are identical"
    else:
        return False, f"JSON files are different: {diff}"

# Example usage
file1_path = "/nethome/lkiefer/pogo/CubiCasa5k/output_20240618_124614.json"
file2_path = "/nethome/lkiefer/pogo/CubiCasa5k/output_20240618_155016.json"
result, message = compare_json_files(file1_path, file2_path)
print(message)

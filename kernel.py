import utils
import re
def get_kernel_version():
    """
    Gets the Linux kernel version, returning only the major and minor version numbers.
    """
    command = "cat /proc/version"
    stdout = utils.execute_command(command)
    match = re.search(r'(\d+\.\d+)', stdout)
    if match:
        return match.group(1)
    else:
        return "Version not found"


def main():
    list_of_vector = "kernel_exploits"
    kernel_version = get_kernel_version()
    print(f"Kernel Version: {kernel_version}")

    print("\nSearching for exploits for the kernel version...")
    quary = "linux kernel " + kernel_version
    print(quary)
    exploits_output = utils.search_exploits(quary)

    exploit_ids = utils.extract_exploit_ids(exploits_output)
    if exploit_ids:
        print("Found potential exploit! IDs:", exploit_ids)
        # Copy all found exploits
        for exploit_id in exploit_ids:
            utils.copy_exploit(exploit_id, list_of_vector)
    else:
        print("No exploits found for the kernel version.")

   # exploit_file = 'kernel_exploits/50808.c'  # Placeholder for the actual exploit file name
    # if os.path.exists(exploit_file):
    #     compiled_exploit = compile_exploit(exploit_file)
    #     run_exploit(compiled_exploit or exploit_file, 'Kernel', '50808')
    #     am_i_root()
    # else:
    #     print(f"Exploit file {exploit_file} not found. Please download it manually.")

if __name__ == "__main__":
    main()
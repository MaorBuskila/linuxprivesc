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
    exploits_output = utils.search_exploits(quary)

    exploit_ids = utils.extract_exploit_ids(exploits_output)
    if exploit_ids:
        print("Found potential exploit! IDs:", exploit_ids)
        # Copy all found exploits
        for exploit_id in exploit_ids:
            utils.copy_exploit(exploit_id, list_of_vector)
    else:
        print("No exploits found for the kernel version.")


if __name__ == "__main__":
    main()
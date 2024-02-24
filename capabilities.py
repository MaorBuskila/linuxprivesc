import utils
import re
import json

def get_binaries_with_capabilities():
    """
    Lists binaries with special capabilities set, excluding the /mnt directory.
    """
    # Command to find files outside /mnt and check their capabilities
    command = "find / -path /mnt -prune -o -type f -print 2>/dev/null | xargs getcap 2>/dev/null"
    stdout = utils.execute_command(command)

    # Regex pattern to capture both binary path and full capabilities
    pattern = re.compile(r'^(?P<binary>[^\s]+) (?P<capability>cap_[^\s]+)', re.MULTILINE)
    matches = pattern.findall(stdout)

    # Convert matches to a list of tuples (binary, full capability string)
    binaries = [(match[0], match[1]) for match in matches]
    return binaries

def check_for_cap_setuid(binaries):
    """
    Checks if any of the provided binaries have the CAP_SETUID capability.
    """
    cap_setuid_binaries = [binary for binary, caps in binaries if 'cap_setuid' in caps]

    return cap_setuid_binaries


def extract_capabilities(binary):
    """Extracts capabilities code snippets from a JSON file."""
    json_path=f"GTFOBins/_gtfobins/{binary}.json"
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if 'capabilities' is in the 'functions' section
    if 'functions' in data and 'capabilities' in data['functions']:
        capabilities = data['functions']['capabilities']
        # Collect all code snippets for capabilities
        code_snippets = [cap['code'] for cap in capabilities]
        return code_snippets
    else:
        # Return a message or handle the case where 'capabilities' is not found
        return ["No capabilities found"]
def main():
    binaries_with_caps = get_binaries_with_capabilities()
    # binaries_with_caps = [('vim', 'cap_setuid+ep')]  # Example output from get_binaries_with_capabilities()
    if not binaries_with_caps:
        print("No binaries with special capabilities found.")
        return

    cap_setuid_binaries = check_for_cap_setuid(binaries_with_caps)
    if cap_setuid_binaries:
        print("Found binaries with CAP_SETUID set, potential backdoors:")
        for binary in cap_setuid_binaries:
            print(extract_capabilities(binary))
    else:
        print("No binaries with CAP_SETUID capability found.")

if __name__ == "__main__":
    main()
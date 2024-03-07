import utils
import re
import json
from subprocess import run, PIPE


def get_binaries_with_capabilities(ssh_client=None):
    """
    Lists binaries with special capabilities set, excluding the /mnt directory.
    """
    # Command to find files outside /mnt and check their capabilities
    command = "find / -path /mnt -prune -o -type f -print 2>/dev/null | xargs getcap 2>/dev/null"
    stdout  = utils.execute_command(command, ssh_client)
    # Regex pattern to capture both binary path and full capabilities
    pattern = re.compile(r'^(?P<binary>[^\s]+) = (?P<capability>[^\s]+)', re.MULTILINE)
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


def extract_capabilities(binary_path, binary_name):
    """Extracts capabilities code snippets from a JSON file."""
    json_path=f"GTFOBins/_gtfobins/{binary_name}.json"
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if 'capabilities' is in the 'functions' section
    if 'functions' in data and 'capabilities' in data['functions']:
        capabilities = data['functions']['capabilities']
        # Collect all code snippets for capabilities
        code_snippets = []
        for cap in capabilities:
            code = cap['code']
        # Replace './binary_name' with 'binary_path' in the code snippet
            code = code.replace(f"./{binary_name}", binary_path)
            code_snippets.append(code)
        return code_snippets
    else:
        # Return a message or handle the case where 'capabilities' is not found
        return ["No capabilities found"]


def capabilities_report(cap_setuid_binaries):

    #TODO need to add the decription of code from GTFOBINS
    report = "----- Capabilities Report -----\n\n"

    # Adding data to the report
    report += "Capabilities setuid binaries:\n" + f"{cap_setuid_binaries}\n\n"

    # Save the report to a file
    with open("Capabilities_Report.txt", "w") as file:
        file.write(report)

    print("Report generated successfully. Check 'Capabilities_Report.txt'.")
    

def main(ssh_client=None):
    binaries_with_caps = get_binaries_with_capabilities(ssh_client)
    # binaries_with_caps = [('vim', 'cap_setuid+ep')]  # Example output from get_binaries_with_capabilities()
    if not binaries_with_caps:
        print("No binaries with special capabilities found.")
        return

    cap_setuid_binaries = check_for_cap_setuid(binaries_with_caps)
    if cap_setuid_binaries:
        print("Found binaries with CAP_SETUID set, potential backdoors:")
        for binary_path in cap_setuid_binaries:
            binary_name = utils.execute_command(f"basename {binary_path}", ssh_client).strip()
            exploits = extract_capabilities(binary_path, binary_name)
    else:
        print("No binaries with CAP_SETUID capability found.")

    # for exploit in exploits:
    #     utils.run_bash_exploit(exploit, ssh_client)

    capabilities_report(cap_setuid_binaries)

if __name__ == "__main__":
    main()
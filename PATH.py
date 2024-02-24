import subprocess
import utils
def check_suid_binaries():
    """
    Checks for SUID binaries on the system and prints the list.
    """
    command = "find / -path /mnt -prune -o -type f -perm -4000 -print 2>/dev/null"
    return utils.execute_command(command)

if __name__ == "__main__":
    suid_binaries = check_suid_binaries()
    if isinstance(suid_binaries, list):
        print("SUID binaries found:")
        for binary in suid_binaries:
            print(binary)
    else:
        print(f"Error: {suid_binaries}")

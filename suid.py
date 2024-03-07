import subprocess
import utils
def check_suid_binaries(ssh_client):
    """
    Checks for SUID binaries on the system and prints the list.
    """
    command = "find / -path /mnt -prune -o -type f -perm -4000 -print 2>/dev/null"
    return utils.execute_command(command, ssh_client)

def main(ssh_client):
    suid_binaries = check_suid_binaries(ssh_client)
    if isinstance(suid_binaries, list):
        print("SUID binaries found:")
        for binary in suid_binaries:
            print(binary)
    else:
        print(f"Error: {suid_binaries}")
        
if __name__ == "__main__":
    main()
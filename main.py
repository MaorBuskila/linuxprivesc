import subprocess
import re
import os
import suid
import utils
import kernel

"""
***************************************************************************************
TODO:
replace the method the we use with searchsploit - the searching dholunt be on the victim machine.
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

def main():


    #SUDO


    # Check for SUID binaries using the suid_check module
    # print("\nChecking for SUID binaries on the system:")
    # suid_binaries = suid.check_suid_binaries()
    # if isinstance(suid_binaries, list):
    #     print("SUID binaries found:")
    #     for binary in suid_binaries:
    #         print(binary)
    # else:
    #     print(f"Error: {suid_binaries}")

    # exploit_file = 'kernel_exploits/50808.c'  # Placeholder for the actual exploit file name
    # if os.path.exists(exploit_file):
    #     compiled_exploit = compile_exploit(exploit_file)
    #     run_exploit(compiled_exploit or exploit_file, 'Kernel', '50808')
    #     am_i_root()
    # else:
    #     print(f"Exploit file {exploit_file} not found. Please download it manually.")




if __name__ == "__main__":
    main()

import subprocess
import utils
import paramiko


"""
***************************************************************************************
TODO:
replace the method the we use with searchsploit - the searching sholudnt be on the victim machine.
Decied if we want to do a real check by exploit the vul and report it to the user
Check how to intergrate GTFOBins
add Vector attacks:
    SUDO
    SUID (Set User ID):
    Cron Jobs:
    PATH:
    NFS (Network File System)


"""


def clone_gtfo_bins(repo_url, clone_directory):
    """
    Clones the GTFOBins GitHub repository into a specified directory.

    :param repo_url: The URL of the GTFOBins GitHub repository.
    :param clone_directory: The local directory where the repository should be cloned.
    """
    try:
        # Prepare the git clone command
        command = ["git", "clone", repo_url, clone_directory]

        # Execute the git clone command
        utils.execute_command(command)
        print(f"Getting GTFOBins... {clone_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone GTFOBins repository: {e}")

def display_banner():
    banner = """
    ███████╗███████╗ ██████╗  █████╗   ██╗      █████╗  ████████╗███████╗███╗   ███╗ █████╗ ████████╗███████╗
    ██╔════╝██╔════╝██╔════╝ ██╔══██╗  ██║     ██╔══██╗ ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
    █████╗  ███████╗██║      ███████║  ██║     ███████║    ██║   █████╗  ██╔████╔██║███████║   ██║   █████╗ 
    ██╔══╝  ╚════██║██║      ██╔══██║  ██║     ██╔══██║    ██║   ██╔══╝  ██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
    ███████╗███████║╚██████╗ ██║  ██║  ███████╗██║  ██║    ██║   ███████╗██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
    ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚══════╝╚═╝  ╚═╝    ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
    """
    print(banner)

def get_user_choice():
    print("\nDo you want to perform scanning:")
    print("1. Locally")
    print("2. Via SSH")
    choice = input("Enter your choice (1 for Local, 2 for SSH): ").strip()
    return choice

def get_ssh_credentials():
    # ssh_host = input("Enter SSH host: ")
    # ssh_user = input("Enter SSH username: ")
    # ssh_password = input("Enter SSH password: ")
    ssh_host = "10.10.241.63"
    ssh_user = "karen"
    ssh_password = "Password1"
    return ssh_host, ssh_user, ssh_password

def get_ssh_connection(host, username, password):
    """
    Establishes an SSH connection using Paramiko.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add host key
        client.connect(hostname=host, username=username, password=password)
        print(f"Successfully connected to {host} as {username}")
        return client
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
    except paramiko.SSHException as sshException:
        print(f"Could not establish SSH connection: {sshException}")
    except Exception as e:
        print(f"Failed to connect to {host} due to: {e}")

def choose_attack_vectors():
    print("\nChoose the vector attack options:")
    print("1. Kernel")
    print("2. Sudo")
    print("3. SUID")
    print("4. Capabilities")
    print("5. Cron Jobs")
    print("6. PATH")
    print("7. NFS (Network File System)")
    print("8. All")
    choice = input("Enter your choice (number or 'All'): ").strip()
    return choice

def execute_vector_attack(choice):
    if choice == "1":
        print("Executing Kernel attack vector...")
        subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # if choice == "2":
    #     print("Executing Kernel attack vector...")
    #     subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # if choice == "3":
    #     print("Executing Kernel attack vector...")
    #     subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    if choice == "4":
        print("Executing capabilities attack vector...")
        subprocess.run(["python3", "capabilities.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # if choice == "5":
    #     print("Executing Kernel attack vector...")
    #     subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # if choice == "6":
    #     print("Executing Kernel attack vector...")
    #     subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # if choice == "7":
    #     print("Executing Kernel attack vector...")
    #     subprocess.run(["python3", "kernel.py"])  # Replace "kernel_vector_script.py" with the actual script name
    # Add elif blocks here for other vectors
    elif choice == "8" or choice.lower() == "all":
        print("Executing all attack vectors...")
        # Add calls to subprocess.run for each vector script
    else:
        print(f"Invalid choice: {choice}")


# Example usage


def main():
    display_banner()
    # REPO_URL = "https://github.com/GTFOBins/GTFOBins.github.io.git"
    # CLONE_DIRECTORY = "./GTFOBins"  # Specify your desired clone directory
    # clone_gtfo_bins(REPO_URL, CLONE_DIRECTORY)
    # directory = 'GTFOBins/_gtfobins'  # Update this path to your directory
    # utils.iterate_and_convert_md_to_json(directory)

    user_choice = get_user_choice()

    if user_choice == "2":
        ssh_host, ssh_user, ssh_password = get_ssh_credentials()
        ssh_client = get_ssh_connection(ssh_host, ssh_user, ssh_password)
        if ssh_client:
            vector_choice = choose_attack_vectors()
            execute_vector_attack(vector_choice)
            ssh_client.close()
        
    elif user_choice != "1":
        print("Invalid choice. Exiting.")
        return

    vector_choice = choose_attack_vectors()
    execute_vector_attack(vector_choice)


# Kernel
# Sudo
# SUID
# Capabilities
# Cron Jobs
# PATH
# NFS (Network File System)



if __name__ == "__main__":
    main()

import subprocess
def execute_command(command):
    """
    Executes a command on the terminal and returns its output.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.wait()
    stdout, stderr = process.communicate()
    return stdout
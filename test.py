import subprocess

def run_find_command():
    command = "find / -path /mnt -prune -o -type f -perm -4000 -print 2>/dev/null"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    process.wait()
    print(stdout)
    # print(stderr)

if __name__ == "__main__":
    run_find_command()

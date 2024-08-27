import paramiko

# SSH connection details
hostname = "192.168.1.200"
port = 22
username = "root"
password = "your_password"  # Replace with your actual password
script_path = "/path/to/mycommand.sh"  # Path to the script on the remote server
output_file = "ssh_output.txt"  # Local file to store the output

# Create an SSH client
ssh = paramiko.SSHClient()

# Load SSH host keys and set policy to add the server's host key automatically
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the remote server
    ssh.connect(hostname, port, username, password)

    # Execute the command to run the shell script
    stdin, stdout, stderr = ssh.exec_command(f"bash {script_path}")

    # Read the output and error streams
    output = stdout.read().decode()
    error = stderr.read().decode()

    # Write the output to a local file
    with open(output_file, "w") as file:
        file.write("Output:\n")
        file.write(output)
        if error:
            file.write("\nError:\n")
            file.write(error)

    print(f"Output written to {output_file}")

finally:
    # Close the SSH connection
    ssh.close()

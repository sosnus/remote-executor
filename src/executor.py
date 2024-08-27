import paramiko

# SSH connection details
hostname = "srv24.mikr.us"

port = 10202
username = "root"
password = "SECRET"  # Replace with your actual password
script_path = "./action/docker-ps.sh"  # Path to the script on the remote server
# script_path = "./action/nginx-restart.sh"  # Path to the script on the remote server
output_file = "ssh_output.txt"  # Local file to store the output

# Read the content of the local script
with open(script_path, 'r') as file:
    script_content = file.read()

# Create an SSH client
ssh = paramiko.SSHClient()

# Load SSH host keys and set policy to add the server's host key automatically
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the remote server
    ssh.connect(hostname, port, username, password)
    
    # Execute the script on the remote server
    # Use a temporary file to hold the script on the remote server
    command = f"bash -c '{script_content}'"
    
    # Execute the command
    stdin, stdout, stderr = ssh.exec_command(command)

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

# Read and print the content of the output file
with open(output_file, 'r') as file:
    file_content = file.read()

print("\nContent of ssh_output.txt:")
print(file_content)
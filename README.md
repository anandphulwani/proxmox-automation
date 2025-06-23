# Before Running (One time only)
### Step 1: For a rented/third party server
#### Format the server using the available `Proxmox 8` template, wait for the process to complete, in case of OVHCloud provide you should recieve an email with the SSH/Web passwrod to access the server.
#### In case of OVHCloud, use IPMI/KVM to access the server (if available), otherwise use SSH to connect to the server at default port 22, use user `root` and password as it is provided in the email.
#### After login, use `passwd` command to change the password to your desired one and type `exit` to quit the SSH console and close it.

### Step 2: Install WSL2 & Ubuntu 22/24 Distro if not installed (Windows Users only)
In Control Panel->Programs->Turn Windows features on or off, Enable Windows Subsystem for Linux
Then run command prompt (CMD.exe) as administrator and execute
```bash
wsl.exe --install --no-distribution
# wsl --set-default-version 1 # if version 2 is not supported
wsl --install -d Ubuntu
wsl --version # Confirm you are on WSL 2
```
Now reboot the PC if prompted.
Use credentials `user` and a password, after entering and reaching console, close the WSL window.

### Step 3:
Now reopen the WSL.exe by running it as administrator. Then run the following commands (`apt-mark hold` only applicable on version 1)
```bash
cd ~
git clone <<LINK OF THIS REPO>>
# sudo apt-mark hold systemd systemd-timesyncd systemd-resolved libnss-systemd udev libudev1
# sudo apt-mark hold polkitd packagekit packagekit-tools software-properties-common ubuntu-wsl
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip -y
sudo apt install python3-ansible-runner ansible -y
```

### Step 4:
```bash
ssh-keygen -t rsa -b 4096 -C "<<EMAIL ADDRESS GOES HERE>>"
cp /home/user/.ssh/id_rsa.pub ./<<EMAIL ADDRESS GOES HERE>>.id_rsa.pub
cp /home/user/.ssh/id_rsa ./<<EMAIL ADDRESS GOES HERE>>.id_rsa
```

### Step 5: Remove old SSH keys of all the servers if any.
```bash
sudo ssh-keygen -f "/root/.ssh/known_hosts" -R "<<Host-IPAddr>>"
```
**Example Placeholders to Replace:**
- `<<Host-IPAddr>>` : Replace with the IP address of Host/Server.

### Step 6: Add new SSH key for all the servers
```bash
sudo ssh root@<<Host-IPAddr>>
```
Please type 'yes' and '↵' to accept the key and then `Ctrl+C` to exit.
**Example Placeholders to Replace:**
- `<<Host-IPAddr>>` : Replace with the IP address of Host/Server.


# How To Run

### Step 1: Copy  `inventory.yml.template` Template File
Copy the `inventory.yml.template` to `inventory.yml`:

```bash
cp inventory.yml.template inventory.yml
```

### Step 2: Replace Values in `inventory.yml`
Replace the placeholder values in `inventory.yml` with actual values. Look for all variables enclosed in `<< >>` and provide the appropriate values:

**Example Placeholders to Replace:**
- `<<HostGroup>>` : Replace with the host group name, `use any name` as it is used just for reference.
- `<<Host01-Hostname>>` : Replace with the hostname of Host01, `use any name` as it is used just for reference.
- `<<Host01-IPAddr>>` : Replace with the IP address of Host01.
- `<<Host01-Username>>` : Replace with the username to connect to Host01, usual value is `root`.
- `<<Host01-DefaultSSHPort>>` : Replace with the SSH port number for Host01, usual value is `22` if not a nested proxmox inside another proxmox, or the default port is changed.

### Step 3: Copy `vault.yml.template` Template File
Copy the `vault.yml.template` to `vault.yml`:

```bash
cp vault.yml.template vault.yml
```

### Step 4: Replace Values in `vault.yml`
Replace the placeholder values in `vault.yml` with actual values. Look for all variables enclosed in `<< >>` and provide the appropriate values.

### Step 5: Run the Playbook
Use one of the following commands to run the Ansible playbook:

**Option 1: Using a Python Script (`playbook_runner.py`)**
```bash
clear && sudo python playbook_runner.py
```

**Option 2: Using `ansible-playbook` Command**
```bash
clear && TERMINAL_WIDTH=$(tput cols) && sudo ansible-playbook -e "terminal_width=${TERMINAL_WIDTH}" -i inventory.yml playbook.yml --ask-pass
```

After `ssh_login_with_key.yml` is executed and the script ends gracefully, 
remove the `--ask-pass` parameter to make the command look like below
and use it to restart the script thereon.
```bash
clear && TERMINAL_WIDTH=$(tput cols) && sudo ansible-playbook -e "terminal_width=${TERMINAL_WIDTH}" -i inventory.yml playbook.yml
```

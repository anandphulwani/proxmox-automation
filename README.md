# Before Running (One time only)
### Step 1: For a rented/third party server
#### Format the server using the available `Proxmox 8` template, wait for the process to complete, in case of OVHCloud provide you should recieve an email with the SSH/Web passwrod to access the server.
#### In case of OVHCloud, use IPMI/KVM to access the server (if available), otherwise use SSH to connect to the server at default port 22, use user `root` and password as it is provided in the email.
#### After login, use `passwd` command to change the password to your desired one and type `exit` to quit the SSH console and close it.

### Step 2: Remove old SSH keys of all the servers if any.
```bash
sudo ssh-keygen -f "/root/.ssh/known_hosts" -R "<<Host-IPAddr>>"
```
**Example Placeholders to Replace:**
- `<<Host-IPAddr>>` : Replace with the IP address of Host/Server.

### Step 3: Add new SSH key for all the servers
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

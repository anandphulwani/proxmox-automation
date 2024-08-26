# How To Run

### Step 1: Copy Template File
Copy the `inventory.yml.template` to `inventory.yml`:

```bash
cp inventory.yml.template inventory.yml
```

### Step 2: Replace Values
Replace the placeholder values in `inventory.yml` with actual values. Look for all variables enclosed in `<< >>` and provide the appropriate values:

**Example Placeholders to Replace:**
- `<<HostGroup>>` : Replace with the host group name, `use any name` as it is used just for reference.
- `<<Host01-Hostname>>` : Replace with the hostname of Host01, `use any name` as it is used just for reference.
- `<<Host01-IPAddr>>` : Replace with the IP address of Host01.
- `<<Host01-Username>>` : Replace with the username to connect to Host01, usual value is `root`.
- `<<Host01-DefaultSSHPort>>` : Replace with the SSH port number for Host01, usual value is `22` if not a nested proxmox inside another proxmox, or the default port is changed.

### Step 3: Run the Playbook
Use one of the following commands to run the Ansible playbook:

**Option 1: Using a Python Script (`playbook_runner.py`)**
```bash
clear && sudo python playbook_runner.py
```

**Option 2: Using `ansible-playbook` Command**
```bash
clear && sudo ansible-playbook -i inventory.yml playbook.yml --ask-pass
```

#!/usr/bin/env python3
import os
import re
import shutil
import ansible_runner
from getpass import getpass

playbook_on_task_start=None

def event_handler(event):
    global playbook_on_task_start
    if event['event'] in ['playbook_on_task_start']:
        playbook_on_task_start = event['stdout']
    if event['event'] in ['playbook_on_play_start', 'playbook_on_stats']:
        print(event['stdout'])
        if event['event'] == 'playbook_on_stats':
            print()
    elif event['event'] in ['runner_on_ok'] and event['stdout'] == "":
        pass
    elif event['event'] in ['runner_on_skipped', 'runner_item_on_skipped']:
        pass
    elif event['event'] in ['playbook_on_task_start'] and event['event_data']['task_action'] == 'include_tasks':
        pass
    elif event['event'] in ['runner_on_failed', 'runner_item_on_failed']:
        print(playbook_on_task_start) if playbook_on_task_start is not None else None
        print(event['stdout'])
    elif event['event'] in ['runner_on_ok', 'runner_item_on_ok']:
        task_name = event['event_data']['task']
        if not re.match(r'^\d{2}-Task_Condition:', task_name) and not re.match(r'^Variable initialization: \d{3},', task_name):
            print(playbook_on_task_start) if playbook_on_task_start is not None else None
            print(event['stdout'])
    else: # 'runner_on_start',
        print(event['stdout'])
        # pass

def run_playbook(playbook_path, inventory_path, ssh_password, extra_vars):
    r = ansible_runner.run_async(
        private_data_dir='.',
        inventory=inventory_path,
        playbook=playbook_path,
        quiet=True,
        event_handler=event_handler,
        artifact_dir=None,
        rotate_artifacts=1,
        passwords={'conn_pass': ssh_password},
        extravars=extra_vars,  # Pass extra vars here
    )
    return r

if __name__ == "__main__":
    playbook_path = 'playbook.yml'
    inventory_path = os.path.abspath('inventory.yml')
    ssh_password = getpass(prompt='Enter SSH password: ')
    
    # Prompt user for input in Python and pass it to Ansible
    public_server_input = input("Is it a public hosted rented server from a 3rd party? (yes/no): ").strip().lower()
    
    # Ensure valid input
    while public_server_input not in ["yes", "no"]:
        print("Invalid input. Please enter 'yes' or 'no'.")
        public_server_input = input("Is it a public hosted rented server from a 3rd party? (yes/no): ").strip().lower()

    # Prompt user for input in Python and pass it to Ansible
    proxmox_accessed_directly_input = input("Is proxmox accessed directly(yes) or via port forwarding/nested proxmox vm(no)?: ").strip().lower()
    
    # Ensure valid input
    while proxmox_accessed_directly_input not in ["yes", "no"]:
        print("Invalid input. Please enter 'yes' or 'no'.")
        proxmox_accessed_directly_input = input("Is proxmox accessed directly(yes) or via port forwarding/nested proxmox vm(no)?: ").strip().lower()

    extra_vars = {'is_public_server_from_3rd_party': public_server_input, 'is_proxmox_accessed_directly': proxmox_accessed_directly_input}
    
    runner = run_playbook(playbook_path, inventory_path, ssh_password, extra_vars)
    runner[0].join()  # Ensure the thread finishes

    # Cleanup artifacts directory
    artifacts_dir = os.path.join('.', 'artifacts')
    if os.path.exists(artifacts_dir):
        shutil.rmtree(artifacts_dir)

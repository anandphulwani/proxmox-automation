#!/usr/bin/env python3
import os
import re
import shutil
import ansible_runner
from getpass import getpass

def event_handler(event):
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
    elif event['event'] in [
                            'runner_on_ok', 'runner_item_on_ok', 
                            'runner_on_failed', 'runner_item_on_failed', 
                            'playbook_on_task_start'
                            ]:
        task_name = event['event_data']['task']
        if not re.match(r'^\d{2}-Task_Condition:', task_name):
            print(event['stdout'])
    else: # 'runner_on_start',
        print(event['stdout'])
        # pass

def run_playbook(playbook_path, inventory_path, ssh_password):
    r = ansible_runner.run_async(
        private_data_dir='.',
        inventory=inventory_path,
        playbook=playbook_path,
        quiet=True,
        event_handler=event_handler,
        artifact_dir=None,
        rotate_artifacts=1,
        passwords={'conn_pass': ssh_password},
    )
    return r

if __name__ == "__main__":
    playbook_path = 'playbook.yml'
    inventory_path = os.path.abspath('inventory.yml')
    ssh_password = getpass(prompt='Enter SSH password: ')
    runner = run_playbook(playbook_path, inventory_path, ssh_password)
    runner[0].join()  # Ensure the thread finishes

    # Cleanup artifacts directory
    artifacts_dir = os.path.join('.', 'artifacts')
    if os.path.exists(artifacts_dir):
        shutil.rmtree(artifacts_dir)

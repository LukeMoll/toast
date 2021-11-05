import ansible_runner

from .config import get_toastfile

def run_slice(s : dict):
    playbook = get_toastfile(s['path'])
    r = ansible_runner.run(
        playbook=playbook,
        inventory=[],
        roles_path=[],
        extravars={},
    )
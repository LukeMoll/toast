import ansible_runner

from .config import get_toastfile, config

import os

ROLES_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), os.pardir, "roles")
)


def run_slice(s: dict):
    playbook = get_toastfile(s["path"])

    s_clone = dict(s)
    try:
        del s_clone["secret"]
    except KeyError:
        pass

    vars_dict = {"toast": {"slice": s_clone, "vars": config["toast"]["vars"]}}

    r = ansible_runner.run(
        playbook=playbook,
        inventory=[],
        roles_path=[ROLES_DIR],
        extravars=vars_dict,
    )

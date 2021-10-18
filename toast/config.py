from typing import Union
import toml
import os

if "TOAST_CONFIG" not in os.environ:
    print("Environment variable TOAST_CONFIG not set")
    exit(1)

_config_fn = os.environ["TOAST_CONFIG"]
if not os.path.isabs(_config_fn):
    print(f"Warning: {_config_fn} is relative")
    _config_fn = os.path.abspath(_config_fn)
    print(f"Canonicalizing to {_config_fn}")

if not os.path.exists(_config_fn):
    print(f"Toast config {_config_fn} does not exist")
    exit(2)

with open(_config_fn) as fd:
    config = toml.load(fd)

if "slice" not in config:
    print("Warning: no slices configured")

def get_slice(repo_fullname : str) -> Union[dict,None]:
    repo_fullname = repo_fullname.lower()
    for s in config["slice"]:
        if s.get("upstream", None) == repo_fullname:
            return s
    return None
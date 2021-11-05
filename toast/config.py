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


def apply_defaults():
    if "toast" not in config:
        config["toast"] = dict()

    if "port" not in config["toast"]:
        config["toast"]["port"] = 12345


def validate_config():
    allowed_sections = {"toast", "slice"}
    keys = set(config.keys())
    if len(keys - allowed_sections) > 0:
        print("Warning: unrecognised sections: " + ",".join(keys - allowed_sections))

    if "slice" not in config:
        print("Warning: no slices configured")

    slice_required_keys = {"upstream", "path"}
    slice_allowed_keys = {*slice_required_keys, "secret", "remote-name", "branch"}
    for s in config["slice"]:
        slice_keys = set(s.keys())
        if len(slice_required_keys - slice_keys) > 0:
            print(
                "Missing required keys in slice:",
                ",".join(slice_required_keys - slice_keys),
            )
            exit(3)

        if len(slice_keys - slice_allowed_keys) > 0:
            print(
                f"Warning: unrecognised keys in slice '{s['upstream']}':",
                ",".join(slice_keys - slice_allowed_keys),
            )

        if not os.path.exists(s["path"]):
            print(f"Warning: file not found: {s['path']}.")

        if not os.path.exists(os.path.join(s["path"], ".git")):
            print(f"Warning: {s['path']} is not a Git repository.")


validate_config()
apply_defaults()


def get_slice(repo_fullname: str) -> Union[dict, None]:
    repo_fullname = repo_fullname.lower()
    for s in config["slice"]:
        if s.get("upstream", None) == repo_fullname:
            return s
    return None


def get_toastfile(path: str) -> str:
    filenames = [
        "toastfile.yml",
        "toastfile.yaml",
        ".toastfile.yml",
        ".toastfile.yaml",
        ".toastfile",
        os.path.join(".toast", "toastfile.yml"),
        os.path.join(".toast", "toastfile.yaml"),
    ]

    if not os.path.exists(path) or not os.path.isdir(path):
        raise NotADirectoryError(path)

    for fn in filenames:
        if os.path.exists(os.path.join(path, fn)):
            return os.path.join(path, fn)

    raise FileNotFoundError(f"No toastfile found under {path}")

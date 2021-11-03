import os

import pygit2


def clone_repository(s: dict):
    pygit2.clone_repository(f"https://github.com/{s['upstream']}.git", s['path'], )

def get_remote(repo : pygit2.Repository, s: dict) -> pygit2.Remote:
    remote_name = s.get("remote-name", "origin")

    try:
        return repo.remotes[remote_name]
    except KeyError:
        raise Exception(f"Repository {s['path']} has no remote {remote_name}")

def get_remote_branch(repo : pygit2.Repository, s: dict, remote: pygit2.Remote) -> pygit2._pygit2.Branch:
    if "branch" in s:
        refspec = f"{remote.name}/{s['branch']}"
        if refspec not in repo.branches:
            raise Exception(f"Repository {s['path']} has no branch {refspec}")
    else:
        default_branches = ["main", "master"]
        for b in default_branches:
            refspec = f"{remote.name}/{b}"
            if refspec in repo.branches:
                break
        else:
            raise Exception(f"No branch defined for repository {s['path']} and could not find a default one")
    
    return repo.branches.get(refspec)

def update_repository(s: dict):
    if not os.path.exists(s['path']):
        print(f"No git repository at {s['path']}, cloning now...")
        clone_repository(s)

    repo = pygit2.Repository(s['path'])
    remote = get_remote(repo, s)

    # will FAIL if it needs authentication (eg SSH, private repo with HTTPS)
    remote.fetch()

    branch = get_remote_branch(repo, s, remote)

    # could fail if working tree isn't clean
    repo.checkout(branch)



import os

import pygit2


def clone_repository(s: dict):
    pass

def get_remote(repo : pygit2.Repository, s: dict):
    remote_name = s.get("remote-name", "origin")

    try:
        return repo.remotes[remote_name]
    except KeyError:
        raise Exception(f"Repository {s['path']} has no remote {remote_name}")


def update_repository(s: dict):
    if not os.path.exists(s['path']):
        raise FileNotFoundError(s['path'])
        # TODO: handle this...
        clone_repository(s)

    repo = pygit2.Repository(s['path'])
    remote = get_remote(repo, s)

    # will FAIL if it needs authentication (eg SSH, private repo with HTTPS)
    remote.fetch()

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
    
    repo.checkout(refspec)
    # this doesn't work, can't fathom why
    # porcelain time



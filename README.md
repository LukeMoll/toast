Toast
===

*A tool to manage continuous deployments of web apps using Ansible*

## Installation
```
pip install shiv
git clone git@github.com:LukeMoll/toast
shiv -c toast -o ./toast.shiv ./toast
```

## Components
 - [ ] Core:
   - [x] Config parser: TOML
   - [x] Webhook server, decode GitHub payload, and validate against GitHub secret
     - [x] Flask and some Python production server; fully encapsulated by entry point
   - [ ] Ansible-runner
     - [x] Allow templating vars:
       - [x] {Name, Wpath} of Slice
       - [x] Basically everything from Toast Slice section
     - [ ] Ansible roles
       - [x] Pass to -runner
       - [ ] Nginx sub{path,domain}
         - [ ] Webroot or proxy
         - [ ] Path or domain
     - [ ] Mutex/lock per-Slice
       - [x] Queue operations from route handler for another thread to work through?
       - [ ] De-duplicate slice operations
   - [ ] Git(Hub) wrangler
     - [ ] Handle SSH remotes (ooer)
     - [ ] Handle private repos
 - [ ] Docs/etc:
   - [ ] Systemd unit (example)
   - [ ] Nginx config (example)
 - [ ] Extended:
   - [ ] Status datastructure
   - [ ] CLI client
   - [ ] Web dashboard client

## toast.conf
 - TOML file with sections per Slice
 - Each section:
   - A (GitHub) repository identifier (`<org>/<name>`) to:
     - Match against `push` payload
     - Poll for changes
   - A path to the cloned repository root
     - Trailing slash removed by `os.normpath`
   - Name of the deployed branch
   - (optional) a GitHub Secret
   - (optional) GitHub Deploy key for private repository polling
   - Deployment options:
     - `vars` section to be interpreted by playbooks
 - Toast section:
   - Port number
 - Ansible globals (`toast.vars`)
   - Passed to each invocation

## CLI
Commands: 
 - `status`:
   - is toastd running
   - For each slice:
     - Does it exist on disk?
     - Is is up-to-date with the local remote?
     - (?) how long since the last `fetch`?¹
     - Did the last ansible run without error?¹
     - ¹ This would be best kept in some kind of log...
 - `fetch`:
   - Force-fetch on slice(s)
 - `run`:
   - Force-run slice

IPC endpoint drops anything not from 127.0.0.1

## Installation
Possibly `shiv`
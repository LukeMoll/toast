Toast
===

*A tool to manage continuous deployments of web apps using Ansible*

## Components
 - [ ] Core:
   - [x] Config parser: TOML
   - [x] Webhook server, decode GitHub payload, and validate against GitHub secret
     - [x] Flask and some Python production server; fully encapsulated by entry point
   - [ ] Ansible-runner
     - [ ] Allow templating vars:
       - x] {Name, Wpath} of Slice
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

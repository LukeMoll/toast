Toast
===

*A tool to manage continuous deployments of web apps using Ansible*

## Components
 - Core:
   - Config parser: TOML
   - Webhook server, decode GitHub payload, and validate against GitHub secret
     - Flask and some Python production server; fully encapsulated by entry point
   - Ansible-runner
     - Allow templating vars:
       - {Name, path} of *Repo*
       - Basically everything from Toast *Repo* section
     - Ansible roles
       - Pass to -runner
       - Nginx sub{path,domain}
         - Webroot or proxy
         - Path or domain
   - Git(Hub) wrangler
 - Docs/etc:
   - Systemd unit (example)
   - Nginx config (example)
 - Extended:
   - Status datastructure
   - CLI client
   - Web dashboard client

## toast.conf
 - TOML file with sections per *Repo* (better terminology needed; "Slice"?)
 - Each section:
   - A (GitHub) repository identifier (`<org>/<name>`) to:
     - Match against `push` payload
     - Poll for changes
   - A path to the cloned repository root
     - Wisdom on trailing slash convention? 
     - Will **always** be a directory so can probably be ignored
   - Name of the deployed branch
   - (optional) a GitHub Secret
   - (optional) GitHub Deploy key for private repository polling
   - Deployment options:
     - Port number
 - Toast section:
   - Port number
 - Ansible globals
   - Passed to each invocation

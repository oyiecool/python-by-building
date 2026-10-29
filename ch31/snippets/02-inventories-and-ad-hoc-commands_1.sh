ansible -i hosts.ini all -m ansible.builtin.ping           # can I reach everything?
ansible -i hosts.ini web -m ansible.builtin.command -a "uptime"
ansible -i hosts.ini db -b -m ansible.builtin.apt -a "name=postgresql state=present"   # -b = sudo

from pathlib import Path
import ansible_runner

here = Path(".").resolve()
r = ansible_runner.run(private_data_dir=str(here / "adhoc"), inventory=str(here / "inventory.py"),
                       host_pattern="web", module="ansible.builtin.command",
                       module_args="uptime", quiet=True)
print(r.status, r.rc)
for e in r.events:
    if e["event"] == "runner_on_ok":
        d = e["event_data"]
        print(d["host"], d["res"]["stdout"][:50])

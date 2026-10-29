#!/usr/bin/python
"""disk_guard - a custom Ansible module that checks free space on a filesystem."""
import os

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
module: disk_guard
short_description: Fail when a filesystem has less free space than allowed
options:
  path:    {description: Mount point or directory to check, type: str, default: /}
  min_free_pct: {description: Lowest acceptable free space in percent, type: int, default: 15}
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(path=dict(type="str", default="/"),
                           min_free_pct=dict(type="int", default=15)),
        supports_check_mode=True,                      # only reads, so safe in --check runs
    )
    path = module.params["path"]
    try:
        st = os.statvfs(path)
    except OSError as e:
        module.fail_json(msg=f"cannot read {path}: {e}")
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    pct = round(100 * free / total, 1) if total else 0.0
    result = dict(changed=False, path=path, total_gb=round(total / 1e9, 1),
                  free_gb=round(free / 1e9, 1), free_pct=pct)
    if pct < module.params["min_free_pct"]:
        module.fail_json(msg=f"{path} has only {pct}% free", **result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()

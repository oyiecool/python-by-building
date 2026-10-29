$ sudo systemctl daemon-reload
$ sudo systemctl enable --now expense-api
$ systemctl status expense-api
$ journalctl -u expense-api -f          # follow its logs

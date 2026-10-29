$ docker build -t expense-api .
$ docker run -d --name expenses -p 8000:8000 -v expense-data:/data expense-api
$ curl http://localhost:8000/summary/2026-10

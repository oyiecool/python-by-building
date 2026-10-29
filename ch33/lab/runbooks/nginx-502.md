# Nginx returns 502 Bad Gateway
Symptoms: 502 errors, "connect() failed (111: Connection refused) while connecting to upstream".
1. Check the app service is listening on its port (8000).
2. Restart the app service, not nginx, if the port is closed.

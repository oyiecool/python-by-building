import os, sys
print(os.environ.get("PATH")[:60])
print(os.getenv("API_KEY", "not set"))
print(sys.platform, sys.version_info[:2], sys.argv)

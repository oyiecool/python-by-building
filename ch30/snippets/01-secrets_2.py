import secrets
reset_token = secrets.token_urlsafe(32)      # unguessable, suitable for links
pin = f"{secrets.randbelow(10**6):06d}"      # a 6-digit code

from datetime import datetime
import secrets


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_secret_key():
    return secrets.token_hex(16)
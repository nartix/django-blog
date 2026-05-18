#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import dotenv_values


DEFAULT_ENV_FILE = "/vault/secrets/app.env"
DEFAULT_ENV_TIMEOUT_SECONDS = 120
START_APP_MODES = {"prod", "celery", "kafka", "dev"}
TRUE_VALUES = {"1", "true", "yes", "on"}


def log(message):
    print(f"[entrypoint] {message}", flush=True)


def load_vault_env():
    env_file = Path(os.environ.get("VAULT_ENV_FILE", DEFAULT_ENV_FILE))
    timeout = int(os.environ.get("VAULT_ENV_TIMEOUT", DEFAULT_ENV_TIMEOUT_SECONDS))
    deadline = time.monotonic() + timeout

    while not env_file.is_file() or env_file.stat().st_size == 0:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Timed out waiting for Vault env file: {env_file}")
        log(f"Waiting for Vault env file at {env_file}")
        time.sleep(2)

    values = dotenv_values(env_file, interpolate=False)
    loaded = 0
    for key, value in values.items():
        if key and value is not None:
            os.environ[key] = value
            loaded += 1

    log(f"Loaded {loaded} values from {env_file}")


def should_collectstatic(mode):
    if mode != "prod":
        return False
    return os.environ.get("DJANGO_COLLECTSTATIC", "true").lower() in TRUE_VALUES


def collectstatic():
    log("Collecting static files")
    subprocess.check_call(
        [sys.executable, "ferozfaiz/manage.py", "collectstatic", "--noinput"]
    )


def resolve_command(argv):
    if not argv:
        return "prod", ["/app/start_app.sh", "prod"]

    if len(argv) == 1 and argv[0] in START_APP_MODES:
        return argv[0], ["/app/start_app.sh", argv[0]]

    return None, argv


def main():
    load_vault_env()

    mode, command = resolve_command(sys.argv[1:])
    if should_collectstatic(mode):
        collectstatic()

    log(f"Starting command: {' '.join(command)}")
    os.execvp(command[0], command)


if __name__ == "__main__":
    main()

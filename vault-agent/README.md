# Vault Agent Docker Compose

This deployment keeps Vault access out of the Django image. Vault Agent renders
secrets into the shared `vault-secrets` tmpfs volume, and the app containers read
`/vault/secrets/app.env` at startup.

## Local token file

Vault Agent reads the Vault address from `VAULT_ADDR`; it is not hardcoded in
the Compose file or agent config.

Set the Vault address and create a local token file before starting Compose:

```sh
export VAULT_ADDR='<vault-address>'
printf '%s' '<vault-token>' > vault-agent/.vault-token
chmod 600 vault-agent/.vault-token
```

The token file is ignored by git and excluded from the Docker build context. You
can also put `VAULT_ADDR=<vault-address>` in a local `.env` file because Docker
Compose reads it automatically.

Example `.env`:

```sh
VAULT_ADDR=https://vault.example.com
```

To use a token file in another location:

```sh
VAULT_ADDR='<vault-address>' VAULT_TOKEN_FILE=/path/to/token docker compose -f docker-compose.prod.yml up -d
```

## Build and run

Build the local production image:

```sh
docker compose -f docker-compose.prod.yml build
```

Start the deployment:

```sh
docker compose -f docker-compose.prod.yml up -d
```

The local production image is tagged as `django-blog:local`.

## Verify

Check that Vault Agent is healthy and rendered the secret files:

```sh
docker compose -f docker-compose.prod.yml ps vault-agent
docker compose -f docker-compose.prod.yml logs --tail=50 vault-agent
```

The app containers read:

```text
/vault/secrets/app.env
/vault/secrets/postgresql-ca.crt
```

pid_file = "/tmp/vault-agent.pid"

auto_auth {
  method "token_file" {
    config = {
      token_file_path = "/run/secrets/vault-token"
    }
  }
}

template_config {
  exit_on_retry_failure = true
}

template {
  source               = "/vault/templates/app.env.ctmpl"
  destination          = "/vault/secrets/app.env"
  perms                = "0600"
  error_on_missing_key = true
}

template {
  source               = "/vault/templates/postgresql-ca.crt.ctmpl"
  destination          = "/vault/secrets/postgresql-ca.crt"
  perms                = "0600"
  error_on_missing_key = true
}

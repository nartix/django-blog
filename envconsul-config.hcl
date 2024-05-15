secret {
  path = "kv/data/POSTGRESQL"
  no_prefix = true
  key {
    name = "POSTGRESQL_CRT"
  }
  key {
    name = "POSTGRESQL_USERNAME"
    format = "PG_MASTER_USER"
  }
  key {
    name = "POSTGRESQL_PASSWORD"
    format = "PG_MASTER_PASSWORD"
  }
  key {
    name = "POSTGRESQL_MASTER_HOST"
    format = "PG_MASTER_HOST"
  }
  key {
    name = "POSTGRESQL_MASTER_PORT"
    format = "PG_MASTER_PORT"
  }
  key {
    name = "POSTGRESQL_REPLICA_HOST_1"
    format = "PG_REPLICA_HOST_1"
  }
  key {
    name = "POSTGRESQL_SSL_ROOT_CERT_DJANGO"
    format = "PG_SSL_ROOT_CERT"
  }
  key {
    name = "POSTGRESQL_SSL_ROOT_CERT_DJANGO_DEV"
  }
}

secret {
  path = "kv/data/DJANGO"
  no_prefix = true
}

secret {
  path = "kv/data/AWS_SES"
  no_prefix = true
  key {
    name = "AWS_SES_EMAIL_PORT"
    format = "EMAIL_PORT"
  }
  key {
    name = "AWS_SES_EMAIL_HOST"
    format = "EMAIL_HOST"
  }
  key {
    name = "AWS_SES_EMAIL_USE_TLS"
    format = "EMAIL_USE_TLS"
  }
  key {
    name = "AWS_SES_EMAIL_HOST_USER"
    format = "EMAIL_HOST_USER"
  }
  key {
    name = "AWS_SES_EMAIL_HOST_PASSWORD"
    format = "EMAIL_HOST_PASSWORD"
  }
  key {
    name = "AWS_SES_EMAIL_USE_SSL"
    format = "EMAIL_USE_SSL"
  }
  key {
    name = "AWS_SES_EMAIL_SENDER_ADDRESS"
    format = "EMAIL_SENDER_ADDRESS"
  }
}

secret {
  path = "kv/data/CELERY"
  no_prefix = true
}

secret {
  path = "kv/data/REDIS"
  no_prefix = true
}

secret {
  path = "kv/data/KAFKA"
  no_prefix = true
}

secret {
  path = "kv/data/ELASTICSEARCH"
  no_prefix = true
}

// Secret configurations for Cloudflare used in Elasticsearch configuration
secret {
  path = "kv/data/CLOUDFLARE"
  no_prefix = true
  key {
    name = "CF_ACCESS_CLIENT_ID"
    format = "ELASTICSEARCH_CLIENT_ID"
  }
  key {
    name = "CF_ACCESS_CLIENT_SECRET"
    format = "ELASTICSEARCH_CLIENT_SECRET"
  }
}

secret {
  path = "kv/data/GOOGLE_OAUTH"
  no_prefix = true
}

secret {
  path = "kv/data/MICROSOFT_OAUTH"
  no_prefix = true
}

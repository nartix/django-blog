## About the project

I developed ferozfaiz.com using Django, focusing on a fully server-side rendered architecture. To enhance interactivity and reactivity, I integrated HTMX and AlpineJS. Additionally, I implemented OAuth 2.0 authentication, supporting both Google and Microsoft. I used RabbitMQ/Celery to send emails. Kafka was used to ship logs to ElasticSearch/Grafana. I also used Hashicorp Vault to store secrets. The current deployment uses Docker Compose with a Vault Agent; the Kubernetes manifests are retained from the earlier deployment.

Live Demo: <a href='https://ferozfaiz.com/'>ferozfaiz.com</a>

### Tech Stack:

- Django
- PostgreSQL
- Redis
- Rabbitmq/Celery
- Kafka
- ElasticSearch
- TailwindCSS
- HTMX
- AlpineJS
- Docker
- Docker Compose
- ViteJS
- Tiptap
- Hashicorp Vault
- Google & Microsoft OAuth 2.0
- Amazon SES
- AWS ECR

## Current production deployment

`docker-compose.prod.yml` runs Django/Gunicorn, Celery, the Kafka consumer, and a Vault Agent. The agent renders configuration and the PostgreSQL CA certificate into a shared in-memory volume. Application containers mount that volume read-only, and the web service binds only to `127.0.0.1:8000` behind the existing public routing.

Build and recreate the web service using the production Compose file and the operator's existing Vault configuration. Keep the Vault token outside source control. The GitHub Actions workflow builds and pushes images to ECR; it does not roll out the running Compose services. See [Vault Agent setup](vault-agent/README.md) for the production inputs.

## Screenshots

<br>
<h3 align='center'>Home Page</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-0.png'/>
</div>
<br>
<h3 align='center'>Blog</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-3.png'/>
</div>
<br>
<h3 align='center'>Blog Post</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-4.png'/>
</div>
<br>
<h3 align='center'>Edit Blog Post</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-13.png'/>
</div>
<br>
<h3 align='center'>User Profile</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-7.png'/>
</div>
<br>
<h3 align='center'>About</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-1.png'/>
</div>
<br>
<h3 align='center'>Sign Up</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-5.png'/>
</div>
<br>
<h3 align='center'>Login</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-6.png'/>
</div>
<br>
<h3 align='center'>Forgot Password</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-8.png'/>
</div>
<br>
<h3 align='center'>Edit Profile</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-9.png'/>
</div>
<br>
<h3 align='center'>Change Password</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-10.png'/>
</div>
<br>
<h3 align='center'>Sign Up Validation Email</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-11.png'/>
</div>
<br>
<h3 align='center'>Change Email</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-12.png'/>
</div>
<br>
<h3 align='center'>Project Page</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-30.png'/>
</div>
<br>
<h3 align='center'>Django Kafka Consumer</h3>
<div align='center'>
<img src='ferozfaiz/static/img/kafka_consumer_for_django_logs.png'/>
</div>
<br>
<h3 align='center'>Mobile Blog View</h3>
<div align='center'>
<img src='ferozfaiz/static/img/django-2.png'/>
</div>
<br>
<h3 align='center'>Kubernetes</h3>
<div align='center'>
<img src='ferozfaiz/static/img/kubernetes_pods.png'/>
</div>
<br>
<h3 align='center'>Grafana with ElasticSearch Data</h3>
<div align='center'>
<img src='ferozfaiz/static/img/grafana.png'/>
</div>

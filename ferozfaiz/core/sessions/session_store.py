from django.contrib.sessions.backends.db import SessionStore as DBStore
import core.models as session


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        # avoids circular import
        return session.Session

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)

        obj.user_agent = data.get('user_agent')
        obj.ip_address = data.get('ip_address')
        obj.location = data.get('location')
        obj.url_visited = data.get('url_visited')
        obj.user_id = data.get('user_id')

        return obj

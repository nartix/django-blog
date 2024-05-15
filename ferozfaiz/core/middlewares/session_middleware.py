from django.utils.deprecation import MiddlewareMixin

class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Retrieve the necessary information
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)
        location = 'Some location'  # Replace with actual location retrieval code
        url_visited = request.path
        user_id = request.user.id if request.user.is_authenticated else None

        # Update the session data
        request.session['user_agent'] = user_agent
        request.session['ip_address'] = ip_address
        request.session['location'] = location
        request.session['url_visited'] = url_visited
        request.session['user_id'] = user_id

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
from django.utils.deprecation import MiddlewareMixin

class OMSCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path == '/' or getattr(request, 'csrf_processing_done', False):
            response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin')
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'

        return response

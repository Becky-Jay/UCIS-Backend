import logging
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

_failed_attempts: dict = defaultdict(lambda: {'count': 0, 'last_attempt': None, 'blocked_until': None})
MAX_ATTEMPTS = 5
BLOCK_MINUTES = 15


class SuspiciousActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.endswith('/login/') and request.method == 'POST':
            ip = self._get_ip(request)
            record = _failed_attempts[ip]

            if record['blocked_until'] and datetime.utcnow() < record['blocked_until']:
                from django.http import JsonResponse
                return JsonResponse(
                    {'message': f'Too many failed attempts. Try again after {BLOCK_MINUTES} minutes.'},
                    status=429,
                )

            request._suspicious_ip = ip

        response = self.get_response(request)

        if request.path.endswith('/login/') and request.method == 'POST' and response.status_code == 401:
            ip = getattr(request, '_suspicious_ip', self._get_ip(request))
            record = _failed_attempts[ip]
            record['count'] += 1
            record['last_attempt'] = datetime.utcnow()

            if record['count'] >= MAX_ATTEMPTS:
                record['blocked_until'] = datetime.utcnow() + timedelta(minutes=BLOCK_MINUTES)
                logger.warning(f'IP {ip} blocked after {MAX_ATTEMPTS} failed login attempts')

        return response

    @staticmethod
    def _get_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')

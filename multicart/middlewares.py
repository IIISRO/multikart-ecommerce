from django.utils.deprecation import MiddlewareMixin
from core.models import BlockedIp
from django.http import Http404, HttpResponseForbidden

class BlockedIpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        blocked_ips_qs = BlockedIp.objects.all()
        blocked_ips = [i.ip for i in blocked_ips_qs]
        if request.META['REMOTE_ADDR'] in blocked_ips:  
            return HttpResponseForbidden(f'<h1>Your ip address {request.META["REMOTE_ADDR"]} blocked. Contact multikart00@gmail.com')



class CheckAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if '/admin/' in request.path and not request.user.is_staff:
            raise Http404()



import logging
class LoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger(__name__)
        logger.info('')
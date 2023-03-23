import re

from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class IPMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        ip = request.META['REMOTE_ADDR']
        print(ip)
        ip_re = re.match('^/test.*$',request.path_info)
        ip_count = int(request.session.get(ip,'1'))
        print(ip_count)
        if ip_re:
            if ip_count > 5:
                return HttpResponse('访问超限')
            ip_count += 1
            request.session[ip] = str(ip_count)
            return
        return


    def process_response(self,request,response):
        return response
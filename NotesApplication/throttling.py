from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class DynamicAnonRateThrottle(AnonRateThrottle):
    scope = 'dynamic_anon'
    
    def allow_request(self, request, view):
        method = request.method.lower()

        RATES = {
            'get': '30/minute',
            'post': '1/minute',
            'put': '1/minute',
            'delete': '1/minute',
        }

        rate = RATES.get(method, '1/minute')
        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)

        return super().allow_request(request, view)
    

class DynamicUserRateThrottle(UserRateThrottle):
    scope = 'dynamic_user'
    
    def allow_request(self, request, view):
        method = request.method.lower()

        RATES = {
            'get': '120/minute',
            'post': '20/minute',
            'put': '20/minute',
            'delete': '30/minute',
        }

        rate = RATES.get(method, '1/minute')
        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)

        return super().allow_request(request, view)

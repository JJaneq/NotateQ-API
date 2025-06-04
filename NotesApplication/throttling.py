from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class DynamicAnonRateThrottle(AnonRateThrottle):
    scope = 'dynamic_anon'
    
    def allow_request(self, request, view):
        method = request.method.lower()

        RATES = {
            'get': '10/second',
            'post': '1/second',
            'put': '1/second',
            'delete': '1/second',
        }

        rate = RATES.get(method, '1/second')
        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)

        return super().allow_request(request, view)
    

class DynamicUserRateThrottle(UserRateThrottle):
    scope = 'dynamic_user'
    
    def allow_request(self, request, view):
        method = request.method.lower()

        RATES = {
            'get': '50/second',
            'post': '10/second',
            'put': '10/second',
            'delete': '10/second',
        }

        rate = RATES.get(method, '1/second')
        self.rate = rate
        self.num_requests, self.duration = self.parse_rate(rate)

        return super().allow_request(request, view)

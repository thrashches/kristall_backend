from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class JWTTokenFromCookieUserAuthentication(JWTTokenUserAuthentication):
    def get_token(self, request):
        return request.COOKIES.get('access_token')

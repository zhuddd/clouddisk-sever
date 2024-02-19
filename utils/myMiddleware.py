from django.utils.deprecation import MiddlewareMixin

from utils.MyResponse import MyResponse
from utils.account import get_user_by_session


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path in ["/account/login", "/account/register", "/file/stream_video"]\
                or request.path.startswith("/admin/"):
            return None
        session = request.COOKIES.get("session", "")
        user_id = get_user_by_session(session)
        if user_id is None:
            print(request.path)
            return MyResponse.ERROR({"error": "请先登录"})
        else:
            request.user_id = user_id
            return None

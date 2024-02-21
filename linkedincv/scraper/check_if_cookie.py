from scraper.models import UserCookie
from scraper.Infrastructure import Linkedin
from scraper.models import UserCookie


def check_if_cookie(user, only_check: bool = False, just_li: bool = False) -> UserCookie:
    try:
        cookie = UserCookie.objects.get(user=user)
    except UserCookie.DoesNotExist:
        return None

    validate = Linkedin.get_profile_data(cookie.cookie, user, only_check, just_li)

    if type(validate) == tuple:
        if not validate[0]:
            UserCookie.objects.filter(user=user).delete()
            return None

    return cookie

from django.contrib.auth import get_user_model

from ...core.api.tokens import JWTAccessToken


def get_user_from_access_token(access_token_str):
    access_token_obj = JWTAccessToken(access_token_str, verify=True)
    user_id = access_token_obj["user_id"]
    user = get_user_model().objects.get(id=user_id)
    return user

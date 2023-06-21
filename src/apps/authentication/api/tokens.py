from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin, RefreshToken

from . import exceptions


class JWTAccessToken(AccessToken):
    """Extended AccessToken class for overriding token validation errors"""

    def verify(self):
        """
        Performs additional validation steps which were not performed when this
        token was decoded.  This method is part of the "public" API to indicate
        the intention that it may be overridden in subclasses.
        """
        self.check_exp()

        # If the defaults are not None then we should enforce the
        # requirement of these settings.As above, the spec labels
        # these as optional.
        if api_settings.JTI_CLAIM is not None and api_settings.JTI_CLAIM not in self.payload:
            raise exceptions.JWTAccessTokenHasNoId()

        if api_settings.TOKEN_TYPE_CLAIM is not None:
            self.verify_token_type()

    def verify_token_type(self):
        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[api_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise exceptions.JWTAccessTokenHasNoType()

        if self.token_type != token_type:
            raise exceptions.JWTAccessTokenHasWrongType()


class CustomRefreshToken(RefreshToken):
    """Extended RefreshToken class for overriding token validation errors"""

    def verify(self):
        """
        Performs additional validation steps which were not performed when this
        token was decoded.  This method is part of the "public" API to indicate
        the intention that it may be overridden in subclasses.
        """
        # Check black list before verifying
        self.check_blacklist()

        self.check_exp()

        # If the defaults are not None then we should enforce the
        # requirement of these settings.As above, the spec labels
        # these as optional.
        if api_settings.JTI_CLAIM is not None and api_settings.JTI_CLAIM not in self.payload:
            raise exceptions.JWTRefreshTokenHasNoId()

        if api_settings.TOKEN_TYPE_CLAIM is not None:
            self.verify_token_type()

    def verify_token_type(self):
        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[api_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise exceptions.JWTRefreshTokenHasNoType()

        if self.token_type != token_type:
            raise exceptions.JWTRefreshTokenHasWrongType()

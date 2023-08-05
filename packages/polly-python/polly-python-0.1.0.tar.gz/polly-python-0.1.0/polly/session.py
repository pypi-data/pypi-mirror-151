from requests import Session
import os
import base64


class PollySession(Session):
    """
    This class contain function to create session for
    polly.

    ``Args:``
        |  ``token (str):`` token copy from polly.

    ``Returns:``
        |  None

    To use this function


    .. code::


            from polly.session import PollySession
            session = PollySession(token)

    """

    def __init__(self, TOKEN, env="polly"):
        Session.__init__(self)
        try:
            # for python version >= python3.8
            from importlib.metadata import version

            version = version("polly-python")
        except ImportError:
            # for python version < python3.8
            import pkg_resources

            version = pkg_resources.get_distribution("polly-python").version
        client = os.getenv("POLLY_SERVICE")
        if client is not None:
            version = version + "/" + client
        else:
            version = version + "/local"

        # check for API Auth key or refresh token
        # generate appropirate headers based on token type
        try:
            # checking if the token string is base64 or not
            # decoding and encoding the token string and
            # comparing with original token that was passed
            # decoding and encoding the token again gives bytes
            # representation of token string
            TOKEN_BYTES = bytes(TOKEN, "ascii")
            if base64.b64encode(base64.b64decode(TOKEN)) == TOKEN_BYTES:
                self.headers = {
                    "Content-Type": "application/vnd.api+json",
                    "x-api-key": f"{TOKEN}",
                    "User-Agent": "polly-python/" + version,
                }
        except Exception:
            self.headers = {
                "Content-Type": "application/vnd.api+json",
                "Cookie": f"refreshToken={TOKEN}",
                "User-Agent": "polly-python/" + version,
            }
        self.env = env

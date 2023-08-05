from polly.session import PollySession
from requests.adapters import HTTPAdapter, Retry
from polly.help import example, doc

link_doc = "https://docs.elucidata.io/OmixAtlas/Polly%20Python.html"
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])


class UnauthorizedException(Exception):
    """

    :meta private:
    """

    def __str__(self):
        return f"Authorization failed as credentials not found. Please use Polly.auth(token) as shown here  ---- {link_doc}"


class Polly:
    """
    This class for authorization to use Polly on any local or cloud platform. To authenticate usage of Polly, \
the following function can be used.
    """

    default_session = None
    example = classmethod(example)
    doc = classmethod(doc)

    @classmethod
    def auth(cls, token, env="polly"):
        """
        Function for authorize usage of Polly on terminal or notebook.

        ``Args:``
            |  ``token (str):`` token copy from Polly front-end.


        ``Returns:``
            |  If token is not correct, it will give an error, else it will clear the authentication for user to\
 get started with polly-python.

        ``Error:``
            |  ``UnauthorizedException:`` when the token is expired.

        To use auth function import class Polly.

        .. code::


                from polly.auth import Polly
                Polly.auth(token)
        """
        cls.default_session = PollySession(token, env=env)
        cls.default_session.mount(
            "https://",
            HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries),
        )

    @classmethod
    def get_session(cls, token=None, env="polly"):
        """
        Function to get session from polly.

        ``Args:``
            |  ``token (str):`` token copy from polly.

        ``Returns:``
            |  if token is not satisfied it will throw UnauthorizedException.
            |  else it will return a polly.session object.

        ``Error:``
            |  ``UnauthorizedException:`` when the token is expired.

        To use get_sesion function import class Polly.


        .. code::


                from polly.auth import Polly
                session = Polly.get_session(token)

        """
        if not token:
            if not cls.default_session:
                raise UnauthorizedException
            else:
                return cls.default_session
        else:
            cls.auth(token, env=env)
            return cls.default_session

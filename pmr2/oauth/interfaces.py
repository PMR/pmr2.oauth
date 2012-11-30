import zope.interface
import zope.schema

from pmr2.oauth import MessageFactory as _


class BaseInvalidError(KeyError):
    __doc__ = "base invalid error."


class TokenInvalidError(BaseInvalidError):
    __doc__ = "invalid token."


class ConsumerInvalidError(BaseInvalidError):
    __doc__ = "invalid consumer."


class RequestInvalidError(BaseInvalidError):
    __doc__ = "invalid request."


class BaseValueError(ValueError):
    __doc__ = "basic value error"


class NotRequestTokenError(TokenInvalidError):
    __doc__ = "Not request token"


class NotAccessTokenError(TokenInvalidError):
    __doc__ = "Not access token"


class ExpiredTokenError(TokenInvalidError):
    __doc__ = "Expired token"


class CallbackValueError(BaseValueError):
    __doc__ = "callback value error"


class NonceValueError(BaseValueError):
    __doc__ = "nonce value error"


class IOAuthAdapter(zope.interface.Interface):
    """
    Interface for the OAuth adapter.
    """

    def __call__():
        """
        Return a boolean value to determine whether access was granted.
        """


class IOAuthPlugin(zope.interface.Interface):
    """\
    The OAuth plugin.
    """

    def extractOAuthCredentials(request):
        """\
        Extract the OAuth credentials from the request, for processing
        by Plone PAS.
        """


class IConsumer(zope.interface.Interface):
    """\
    An OAuth consumer.
    """

    key = zope.schema.ASCIILine(
        title=_(u'Consumer Key'),
        description=_(u'The key that identifies this consumer.  This usually '
                     'is the domain name of the consumer'),
        required=True,
    )

    secret = zope.schema.ASCIILine(
        title=_(u'Consumer Secret'),
        description=_(u'Consumer secret'),
        required=True,
    )

    def validate():
        """
        Self validation.
        """


class IConsumerManager(zope.interface.Interface):
    """\
    Consumer utility
    """

    def add(consumer):
        """\
        Add a consumer.
        """

    def check(consumer):
        """\
        Check for validity of input consumer.
        """

    def get(consumer_key, default=None):
        """\
        Return consumer, identified by consumer_key.
        """

    def getAllKeys():
        """\
        Return all consumer keys tracked by this consumer.
        """

    def getValidated(consumer_key, default=None):
        """\
        Return consumer only if it is a validated one.
        """

    def remove(consumer):
        """\
        Remove consumer.
        """


class IScopeManager(zope.interface.Interface):
    """\
    Scope Manager

    A manager that simplifies the handling of scopes, which place limits
    on what an authenticated token can access.
    """

    # individual scope manager should deal with how/what the meaning of
    # the scope value within each token.

    def validate(context, client_key, access_key):
        """\
        Validate the scope against the given context with the given
        client and owner.

        context
            the object to access.

        client
            the client (consumer) key.

        access_key
            the access key identifying a given token granted by a
            resource owner.
        """


class IDefaultScopeManager(zope.interface.Interface):
    """\
    Fields for the default scope manager.
    """

    permitted = zope.schema.ASCII(
        title=_(u'Permitted URIs'),
        description=_(u'List of regular expressions of URIs that are permitted '
                     'to be accessible via OAuth.'),
        required=True,
    )


class IToken(zope.interface.Interface):
    """\
    An OAuth token.
    """

    key = zope.schema.ASCIILine(
        title=_(u'Key'),
        description=_(u'Consumer key'),
        required=True,
    )

    secret = zope.schema.ASCIILine(
        title=_(u'Secret'),
        description=_(u'Consumer secret'),
        required=True,
    )

    callback = zope.schema.TextLine(
        title=_(u'Callback'),
        required=True,
    )

    callback_confirmed = zope.schema.ASCIILine(
        title=_(u'Callback Confirmed'),
        required=True,
    )

    verifier = zope.schema.ASCIILine(
        title=_(u'Verifier'),
        required=True,
    )

    # other requirements

    access = zope.schema.Bool(
        title=_(u'Access Permitted'),
        description=_(u'Determines if this can be used to access content.'),
        default=False,
        required=True,
    )

    user = zope.schema.ASCIILine(
        title=_(u'User ID'),
        description=_(u'The user id associated with this token.'),
        required=False,
        default=None,
    )

    consumer_key = zope.schema.ASCIILine(
        title=_(u'Consumer Key'),
        description=_(u'The consumer key associated with this token'),
        required=False,
        default=None,
    )

    timestamp = zope.schema.Int(
        title=_(u'Timestamp'),
        description=_(u'Creation timestamp of this token'),
    )

    expiry = zope.schema.Int(
        title=_(u'Expiry'),
        description=_(u'Expiry timestamp for this token'),
    )

    scope = zope.schema.Text(
        title=_(u'Scope'),
        description=_(u'The scope associated with this token'),
        required=False,
    )

    def validate():
        """
        Self validation.
        """


class ITokenManager(zope.interface.Interface):
    """\
    Token manager utility
    """

    def add(token):
        """\
        Add a token.
        """

    def generateRequestToken(consumer, request):
        """\
        Generate a request token, using consumer and request.
        """

    def generateAccessToken(consumer, request):
        """\
        Generate an access token.
        """

    def claimRequestToken(token, user):
        """\
        Token claimed by user.
        """

    def get(token, default=None):
        """\
        Get a token by token.

        Input could be a token, or a key.  Returns the same token 
        identified by the key of the input token or the input key.
        """

    def getRequestToken(token, default=False):
        """\
        Return request token identified by token.

        Raises NotRequestTokenError when token is not an access token.
        Raises InvalidTokenError if internal consistency (invariants)
        are violated.
        If token is not found and default value is false, 
        InvalidTokenError should be raised also.
        """

    def getAccessToken(token, default=False):
        """\
        Return access token identified by token.

        Raises NotAccessTokenError when token is not an access token.
        Raises InvalidTokenError if internal consistency (invariants)
        are violated.
        If token is not found and default value is false, 
        InvalidTokenError should be raised also.
        """

    def getTokensForUser(user):
        """\
        Return a list of token keys for a user.
        """

    def remove(token):
        """\
        Remove token.
        """


# Other management interfaces

class ICallbackManager(zope.interface.Interface):
    """\
    Callback manager.

    Can be used by token managers to check whether a callback is
    acceptable.
    """

    def check(callback):
        """\
        Check that this callback is valid.
        """


class INonceManager(zope.interface.Interface):
    """\
    Nonce manager.

    If nonce must be checked specifically, implement this manager.
    """

    def check(timestamp, nonce):
        """\
        Check that this nonce can be used.
        """

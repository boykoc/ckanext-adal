# CKAN related imports
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model
from ckan.common import request
from ckan.common import config as ckan_config
from flask import Blueprint
from flask import render_template_string

# Extension specific related imports
import adal_config as config # Extension configuration
from adal import AuthenticationContext # ADAL
import flask # TODO: Refactor?
import random # TODO: Refactor?
import string # TODO: Refactor?
# JWT Verification
import jwt
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import requests # TODO: Refactor?


AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = ckan_config['ckan.site_url'].rstrip('/') + '/getAToken'
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}' +
                      '/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')

log = logging.getLogger(__name__)


def adal_login():
    '''Make call to authorization_url to authenticate user and get
    authorization code.
    '''
    # TODO: handle state better.
    auth_state = (''.join(random.SystemRandom()
                  .choice(string.ascii_uppercase + string.digits)
                  for _ in range(48)))
    authorizaction_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    resp = flask.Response(status=307)
    resp.headers['location'] = authorizaction_url

    return resp


def get_a_token():
    '''Handle Azure AD callback.
    Get authorization code from Azure AD response. Use code to get access
    token and validate. If all is good, log user in.
    '''
    try:
        token_response = _aquire_token()
        auth_context = AuthenticationContext(AUTHORITY_URL)
        token_response = auth_context.acquire_token_with_refresh_token(
            token_response['refreshToken'],
            config.CLIENT_ID,
            config.RESOURCE,
            config.CLIENT_SECRET)
        decoded = _validate_access_token(token_response['accessToken'])
        if not _validate_email_domains(decoded['unique_name']):
            raise
        if not _validate_user_exists_in_ckan(
            decoded['unique_name']
            .lower()
            .replace('.', '_')
            .split('@')[0],
            decoded['unique_name']):
            raise

        resp = _ckan_authenticate(
            decoded['unique_name']
            .lower()
            .replace('.', '_')
            .split('@')[0])
    except Exception as e:
        log.error('Exception raised. Unable to authenticate. {}'
                  .format(repr(e)))
        toolkit.abort(403, _('Not authorized.'))

    return resp


def _aquire_token():
    code = flask.request.args['code']
    state = flask.request.args['state']
    # Main ADAL logic starts.
    auth_context = AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(
        code,
        REDIRECT_URI,
        config.RESOURCE,
        config.CLIENT_ID,
        config.CLIENT_SECRET)

    return token_response
    # Main ADAL logic ends.


def _ckan_authenticate(user_name):
    # Log the user in programatically.
    # Reference: ckan/views/user.py
    # By this point we either have a user or created one and they're good to
    # login.
    resp = toolkit.h.redirect_to(u'user.logged_in')

    '''Set the repoze.who cookie to match a given user_id'''
    if u'repoze.who.plugins' in request.environ:
        rememberer = request.environ[u'repoze.who.plugins'][u'friendlyform']
        identity = {u'repoze.who.userid': user_name}
        resp.headers.extend(rememberer.remember(request.environ, identity))

    return resp


def _validate_access_token(access_token):
    # Get the token header to find cert related info.
    token_header = jwt.get_unverified_header(access_token)

    # Get certs and find match from header.
    res = requests.get('https://login.windows.net/common/discovery/keys')
    jwk_keys = res.json()
    x5c = None

    for key in jwk_keys['keys']:
        if key['kid'] == token_header['kid']:
            x5c = key['x5c']

    # Now that a cert match is found, get it's public key.
    cert = ''.join([
        '-----BEGIN CERTIFICATE-----\n',
        x5c[0],
        '\n-----END CERTIFICATE-----\n'])
    public_key = load_pem_x509_certificate(cert.encode(),
                                           default_backend()).public_key()
    try:
        # exp, nbf and and iat claims are automatically validated if present
        # in the JWt. Audience and issuer are additional checks passed in when
        # decoding.
        decoded = jwt.decode(
            access_token,
            public_key,
            algorithms=['RS256'],
            audience=config.RESOURCE,
            issuer=config.ISSUER)
    except Exception as e:
        log.error('Exception raised while decoding JWT. {}'.format(repr(e)))
        # TODO: abort and redirect with error message.
        toolkit.abort(403, _('Not authorized.'))

    return decoded


def _validate_email_domains(user_email):
    ''' Validate email domains.
    '''
    # TODO: Do something with return value or abort here.
    # TODO: Validate matching email, username, etc and login proper user.
    try:
        if not user_email.split('@')[1] in config.EMAIL_DOMAINS:
            raise
    except Exception as e:
        log.error('Exception raised. Improper email domain. {}'
                  .format(repr(e)))
        return False
    return True


def _validate_user_exists_in_ckan(username, email):
    # Validate user is registered and active.
    """
    Return the CKAN user with the given user name, or None.
    Check state, state: deleted can still login but gets a blank page because
    CKAN is handling authorization later as well.
    """
    try:
        # Get the user via the model as accessing it via get_action
        # ('show_user') will be blocked. I anticipate having
        # ckan.auth.public_user_details = false in the conig.
        user = model.User.get(username)
        if user.state == 'active' and user.email == email.lower():
            return user
        else:
            raise toolkit.ObjectNotFound
    except toolkit.ObjectNotFound as e:
        log.error('Exception raised. Invalid user. {}'
                  .format(repr(e)))
        return None


class AdalPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'adal')

    # IAuthenticator

    def identify(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass

    def abort(self, status_code, detail, headers, comment):
        pass

    # IBlueprints

    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        rules = [
            ('/adal/login', 'adal_login', adal_login),
            ('/getAToken', 'get_a_token', get_a_token)
        ]

        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

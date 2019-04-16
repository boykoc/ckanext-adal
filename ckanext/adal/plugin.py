# TODO:
#
# [X] Create and import config file with Azure details.
# [ ] Setup adal_login() to handle build auth url and call it.
# [ ] Setup get_a_token() to handle callback, get token with returned code, validate token, log user in.
# [ ] Add button or something to let users trigger login via ADAL.
#
#


import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint
from flask import render_template_string

import config
import flask
import random
import string

AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://52.237.34.255:{}/getAToken'.format('5000')
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')

def adal_login():
    '''Make call to authorization_url to authenticate user and get
    authorization code.
    '''
    print("here 1")
    auth_state = (''.join(random.SystemRandom()
                    .choice(string.ascii_uppercase + string.digits)
                    for _ in range(48)))
    print('here 2')
    authorizaction_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    print("here 3")
    resp = flask.Response(status=307)
    resp.headers['location'] = authorizaction_url
    return resp

def get_a_token():
    html = u'''<!DOCTYPE html>
<html>
    <head>
        <title>getAToken</title>
    </head>
    <body>
        Token.
    </body>
</html>'''

    return render_template_string(html)

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

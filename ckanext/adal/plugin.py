import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint
from flask import render_template_string

def adal_login():
    html = u'''<!DOCTYPE html>
<html>
    <head>
        <title>ADAL Login</title>
    </head>
    <body>
        Login.
    </body>
</html>'''

    return render_template_string(html)

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
            ('/adal/login/getAToken/', 'get_a_token', get_a_token)
        ]

        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

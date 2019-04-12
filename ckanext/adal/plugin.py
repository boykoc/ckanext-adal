import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


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

    def get_blueprints(self):
        pass


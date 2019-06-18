"""Tests for plugin.py."""
import ckanext.adal.plugin as plugin
import ckanext.adal.adal_config as adal_config
from nose.tools import assert_equals, ok_, assert_raises
from ckan.tests import factories, helpers
import ckan.model as model
import ckan.plugins as plugins

# Reference: https://docs.microsoft.com/en-us/azure/active-directory/
#                    develop/id-tokens#claims-in-an-id_token
ACCESS_TOKEN_STUB = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjdfWnVmMX \
R2a3dMeFlhSFMzcTZsVWpVWUlHdyIsImtpZCI6IjdfWnVmMXR2a3dMeFlhSFMzcTZsVWpVWUlHd \
yJ9.eyJhdWQiOiJiMTRhNzUwNS05NmU5LTQ5MjctOTFlOC0wNjAxZDBmYzljYWEiLCJpc3MiOiJ \
odHRwczovL3N0cy53aW5kb3dzLm5ldC9mYTE1ZDY5Mi1lOWM3LTQ0NjAtYTc0My0yOWYyOTU2Zm \
Q0MjkvIiwiaWF0IjoxNTM2Mjc1MTI0LCJuYmYiOjE1MzYyNzUxMjQsImV4cCI6MTUzNjI3OTAyN \
CwiYWlvIjoiQVhRQWkvOElBQUFBcXhzdUIrUjREMnJGUXFPRVRPNFlkWGJMRDlrWjh4ZlhhZGVB \
TTBRMk5rTlQ1aXpmZzN1d2JXU1hodVNTajZVVDVoeTJENldxQXBCNWpLQTZaZ1o5ay9TVTI3dVY \
5Y2V0WGZMT3RwTnR0Z2s1RGNCdGsrTExzdHovSmcrZ1lSbXY5YlVVNFhscGhUYzZDODZKbWoxRk \
N3PT0iLCJhbXIiOlsicnNhIl0sImVtYWlsIjoiYWJlbGlAbWljcm9zb2Z0LmNvbSIsImZhbWlse \
V9uYW1lIjoiTGluY29sbiIsImdpdmVuX25hbWUiOiJBYmUiLCJpZHAiOiJodHRwczovL3N0cy53 \
aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaXBhZGR \
yIjoiMTMxLjEwNy4yMjIuMjIiLCJuYW1lIjoiYWJlbGkiLCJub25jZSI6IjEyMzUyMyIsIm9pZC \
I6IjA1ODMzYjZiLWFhMWQtNDJkNC05ZWMwLTFiMmJiOTE5NDQzOCIsInJoIjoiSSIsInN1YiI6I \
jVfSjlyU3NzOC1qdnRfSWN1NnVlUk5MOHhYYjhMRjRGc2dfS29vQzJSSlEiLCJ0aWQiOiJmYTE1 \
ZDY5Mi1lOWM3LTQ0NjAtYTc0My0yOWYyOTU2ZmQ0MjkiLCJ1bmlxdWVfbmFtZSI6IkFiZUxpQG1 \
pY3Jvc29mdC5jb20iLCJ1dGkiOiJMeGVfNDZHcVRrT3BHU2ZUbG40RUFBIiwidmVyIjoiMS4wIn \
0=.UJQrCA6qn2bXq57qzGX_-D3HcPHqBMOKDPx4su1yKRLNErVD8xkxJLNLVRdASHqEcpyDctbd \
Hccu6DPpkq5f0ibcaQFhejQNcABidJCTz0Bb2AbdUCTqAzdt9pdgQvMBnVH1xk3SCM6d4BbT4Bk \
LLj10ZLasX7vRknaSjE_C5DI7Fg4WrZPwOhII1dB0HEZ_qpNaYXEiy-o94UJ94zCr07GgrqMsfY \
QqFR7kn-mn68AjvLcgwSfZvyR_yIK75S_K37vC3QryQ7cNoafDe9upql_6pB2ybMVlgWPs_DmbJ \
8g0om-sPlwyn74Cc1tW3ze-Xptw_2uVdPgWyqfuWAfq6Q'


class TestAdal(object):
    def setup(self):
        self.app = helpers._get_test_app()

        if not plugins.plugin_loaded(u'adal'):
            plugins.load(u'adal')
            plugin = plugins.get_plugin(u'adal')
            self.app.flask_app.register_extension_blueprint(
                plugin.get_blueprint())

    def teardown(self):
        '''Nose runs this method after each test method in our test class.'''
        # Rebuild CKAN's database after each test method, so that each test
        # method runs with a clean slate.
        model.repo.rebuild_db()

    def test_adal_login(self):
        '''Test response is returned with a 307 status and location is fired
        to Azure authentication page.
        '''
        res = self.app.get(u'/adal/login')
        ok_(adal_config.AUTHORITY_HOST_URL in res.headers['location'])
        assert_equals('307 TEMPORARY REDIRECT', res.status)

    def test_get_a_token(self):
        '''This needs to make calls to a real Azure AD app that has a callback
        setup. This would be different for each CKAN instance.
        I've thought about stubbing out but for now I'm skipping as this seems
        very cumbersome. Possibly better to refactor the function to extract
        some complexity and make it easier to test.
        '''
        pass

    def test_aquire_token(self):
        '''This is mostly just implementing ADAL which handles it's own
        testing.
        '''
        pass

    def test_ckan_athenticate(self):
        # TODO: look into this more:
        # https://github.com/ckan/ckan/wiki/
        #         Migration-from-Pylons-to-Flask#routes
        # user = factories.User()
        # res = plugin._ckan_authenticate(user['name'])
        # ok_('Dashboard' in res)
        pass

    def test_validate_access_token(self):
        '''This expects an Azure AD access_token and gets the rotating public
        keys from microsoft.
        '''
        pass

    def test_invalide_validate_access_token(self):
        '''Test exception is raised if invalid access_token give.
        This raises based on the x5c lookup fail, not on the decode portion
        I could extract the jwt.decode to it's own function and test it with a
        "fake" key and token and create it for each test pass but this
        functionality is also tested by the pyjwt library.
        '''
        assert_raises(Exception,
                      plugin._validate_access_token,
                      ACCESS_TOKEN_STUB)

    def test_validate_email_domains(self):
        '''Only those email domains from config should validate.
        '''
        email = 'Luke.Skywalker@' + adal_config.EMAIL_DOMAINS[0]
        assert_equals(plugin._validate_email_domains(email), True)
        assert_equals(plugin._validate_email_domains('Darth.Vader@gmail.com'),
                      False)

    def test_validate_user_exists_in_ckan(self):
        user = factories.User()

        valid_user = plugin._validate_user_exists_in_ckan(
            user['name'],
            user['email'])
        is_not_valid_user = plugin._validate_user_exists_in_ckan(
            'darth_vader',
            'darth.vader@workplace.com')
        assert_equals(valid_user.id, user['id'])
        assert_equals(is_not_valid_user, None)

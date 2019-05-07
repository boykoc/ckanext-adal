"""Tests for plugin.py."""
import ckanext.adal.plugin as plugin
import ckanext.adal.adal_config as adal_config
from nose.tools import assert_equals
from ckan.tests import factories
import ckan.model as model

def test_plugin():
    pass

class TestAdal(object):
  def teardown(self):
    '''Nose runs this method after each test method in our test class.'''
    # Rebuild CKAN's database after each test method, so that each test
    # method runs with a clean slate.
    model.repo.rebuild_db()

  def test_adal_login(self):
    pass

  def test_get_a_token(self):
    pass

  def test_aquire_token(self):
    pass

  def test_ckan_athenticate(self):
    pass

  def test_validated_access_token(self):
    pass

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


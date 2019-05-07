"""Tests for plugin.py."""
import ckanext.adal.plugin as plugin
import ckanext.adal.adal_config as adal_config
from nose.tools import assert_equals

def test_plugin():
    pass

class TestAdal(object):
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
    pass


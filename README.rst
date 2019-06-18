=============
ckanext-adal
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

This extension relies on [ADAL](https://github.com/AzureAD/azure-activedirectory-library-for-python).


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-adal:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-adal Python package into your virtual environment::

     git clone https://github.com/boykoc/ckanext-adal.git
     cd ckanext-adal
     python setup.py develop
     pip install -r requirements.txt

3. Add ``adal`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Edit the configuration file for the plugin at ``ckanext/adal/adal_config.py``.

Add a Redirect URI in Azure AD. Go to Azure Active Directory in Azure. Look
for Authentication to set the URI of type Web to ``https://[YOUR_DOMAIN_HERE]/getAToken``


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.adal --cover-inclusive --cover-erase --cover-tests


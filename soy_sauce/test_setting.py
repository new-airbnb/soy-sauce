from soy_sauce.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': True,
        'NAME': conf['test_database_name'],
        'HOST': conf['test_database_uri'],
        'TEST': {
            'NAME': conf['test_database_name']
        }
    }
}

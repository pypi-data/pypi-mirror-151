'''
Classes representing Audit Log plans.
'''
import json
import logging
from http import HTTPStatus
import tempfile
from os import unlink
import requests
from sap.audit_logging.loggers import ConsoleLogger, HttpLogger

CLIENT_CREDENTIALS_TOKEN_PATH = '/oauth/token?grant_type=client_credentials'
MTLS_CREDENTIALS_TOKEN_PATH = '/oauth/token'
AUDIT_SERVICE_URL_PATH = 'audit-log/v2'
AUDIT_SERVICE_OAUTH_URL_PATH = 'audit-log/oauth2/v2'


def _create_pem_files(file_content):
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    with tmp_file:
        tmp_file.write(file_content)
        tmp_file.close()
    return tmp_file.name


def _delete_pem_files(filename):
    if filename:
        unlink(filename)


def create(credentials):
    ''' creating plan '''
    if credentials is None:
        return Missing()
    if 'uaa' in credentials:
        return Oauth2(credentials)
    return Standard(credentials)


class Missing:
    ''' When credentials are missing'''

    def __init__(self):
        self._credentials = None

    def create_logger(self):  # pylint: disable=no-self-use
        ''' creates a logger for this plan'''
        logging.basicConfig()
        logging.getLogger(__name__).warning(
            'Audit log service not found. Using console logger.')
        return ConsoleLogger()

    def set_security_context(self, ctx):  # pylint: disable=no-self-use
        ''' setting the security context '''


class Oauth2:
    ''' Oauth2 Plan '''

    def __init__(self, credentials):
        self._credentials = credentials
        self._ctx = None

    def create_logger(self):
        ''' creates a logger for this plan'''
        return HttpLogger(self)

    def set_security_context(self, ctx):
        ''' setting the security context '''
        self._ctx = ctx

    def url(self):
        ''' return url with plan-specific path prefix'''
        return '{0}/{1}'.format(self._credentials['url'], AUDIT_SERVICE_OAUTH_URL_PATH)

    def auth(self):
        ''' return auth-realated properties for making requests '''
        uaa = self._credentials['uaa']
        # checking token type
        if self._ctx is not None and self._ctx.get_grant_type() != 'client_credentials':
            token = self._ctx.request_token_for_client(uaa, None)
            return {'headers': {'Authorization': 'Bearer ' + token}}
        use_mtls = False
        # checking mTls
        if {'clientx509enabled', 'certurl', 'certificate', 'key'}.issubset(uaa):
            use_mtls = True
        target_url = uaa['url'] + CLIENT_CREDENTIALS_TOKEN_PATH
        cert_file_name, key_file_name = None, None
        try:
            if use_mtls: # pylint: disable=no-self-use
                cert_file_name = _create_pem_files(uaa['certificate'])
                key_file_name = _create_pem_files(uaa['key'])
                target_url = uaa['certurl'] + MTLS_CREDENTIALS_TOKEN_PATH
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': uaa['clientid']
                }
                response = requests.post(target_url, data=data,
                                         cert=(cert_file_name, key_file_name))
            else:
                response = requests.post(target_url, auth=(uaa['clientid'], uaa['clientsecret']))
            if response.status_code != HTTPStatus.OK:
                message = 'Could not fetch client_credentials token, status: %d' \
                          % response.status_code
                raise RuntimeError(message)
            token = json.loads(response.text)['access_token']
            return {'headers': {'Authorization': 'Bearer ' + token}}
        finally:
            _delete_pem_files(cert_file_name)
            _delete_pem_files(key_file_name)


class Standard:
    ''' Standard Plan '''

    def __init__(self, credentials):
        self._credentials = credentials

    def create_logger(self):
        ''' creates a logger for this plan'''
        return HttpLogger(self)

    def set_security_context(self, ctx):  # pylint: disable=no-self-use
        ''' setting the security context '''
        raise RuntimeError('Cannot set Security Context if plan is Standard.')

    def url(self):
        ''' return url with plan-specific path prefix'''
        return '{0}/{1}'.format(self._credentials['url'], AUDIT_SERVICE_URL_PATH)

    def auth(self):
        ''' return auth-realated properties for making requests'''
        return {'auth': (self._credentials['user'], self._credentials['password'])}

'''
Audit logger message factory.
'''
from cfenv import AppEnv
from sap.audit_logging.messages.configuration_change_message import ConfigurationChangeMessage
from sap.audit_logging.messages.data_access_message import DataAccessMessage
from sap.audit_logging.messages.data_modification_message import DataModificationMessage
from sap.audit_logging.messages.security_event_message import SecurityEventMessage
from sap.audit_logging import plans

AUDIT_LOG_LABEL = 'auditlog'

class AuditLogger:
    ''' AuditLogger '''

    def __init__(self, service_instance_name=None, credentials=None):
        if service_instance_name is not None and credentials is not None:
            raise TypeError('Service instance name and credentials cannot be both provided')
        creds = _resolve_credentials(service_instance_name, credentials)
        self._plan = plans.create(creds)
        self._logger = self._plan.create_logger()

    def with_security_context(self, ctx):
        ''' returns a new audit logger object with security context set '''
        # pylint: disable=protected-access
        audit_logger = AuditLogger(credentials=self._plan._credentials)
        audit_logger._plan.set_security_context(ctx)
        return audit_logger

    def create_data_access_msg(self):
        ''' create data access message '''
        return DataAccessMessage(self._logger)

    def create_data_modification_msg(self):
        ''' create data modification message '''
        return DataModificationMessage(self._logger)

    def create_configuration_change_msg(self):
        ''' create configuration change message '''
        return ConfigurationChangeMessage(self._logger)

    def create_security_event_msg(self):
        ''' create security event message '''
        return SecurityEventMessage(self._logger)


def _resolve_credentials(service_instance_name, credentials):
    if credentials is not None:
        return credentials

    app_env = AppEnv()
    audit_log_service = None
    if service_instance_name is not None:
        audit_log_service = app_env.get_service(name=service_instance_name)
        if not audit_log_service:
            raise ValueError(
                'Could not find service with name={0}'.format(service_instance_name))
    else:
        audit_log_service = app_env.get_service(label=AUDIT_LOG_LABEL)

    return None if audit_log_service is None else audit_log_service.credentials

import logging

logger = logging.getLogger(__name__)


def log_admin_action(admin, action, target_resource, target_id, details=None, ip_address=None):
    """
    Create an AuditLog entry. Called from views whenever an admin takes an action.
    Returns the created log instance or None on failure.
    """
    from apps.audit_logs.models import AuditLog
    try:
        log = AuditLog.objects.create(
            action=action,
            performed_by=admin,
            role=admin.role,
            target_resource=target_resource,
            target_id=str(target_id),
            details=str(details) if details else '',
            ip_address=ip_address or '',
        )
        return log
    except Exception as e:
        logger.error(f'Failed to create audit log: {e}')
        return None

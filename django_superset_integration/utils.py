# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class LogChanges:
    """
    Must be extended in admin model classes
    Log modifications made to objects from django dmin site
    """

    def log_addition(self, request, object, message=None):
        """
        Log an object creation
        """
        log_str = str(type(object))
        log_str += ": "
        log_str += object.__str__()
        log_str += " ; created by: "
        log_str += request.user.__str__()
        log_str += " from admin site."
        logger.warning(log_str)

    def log_change(self, request, object, message=None):
        """
        Log an object modification
        """
        log_str = str(type(object))
        log_str += ": "
        log_str += object.__str__()
        log_str += " ; modified by: "
        log_str += request.user.__str__()
        log_str += " from admin site."
        logger.warning(log_str)

    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted
        Nota: must be called before object deletion
        """
        log_entry = super().log_deletion(request, object, object_repr)
        logger.info(log_entry)

        log_str = str(type(object))
        log_str += ": "
        log_str += object.__str__()
        log_str += " ; deleted by: "
        log_str += request.user.__str__()
        log_str += " from admin site."
        logger.warning(log_str)

        return log_entry

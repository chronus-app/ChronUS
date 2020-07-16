from rest_framework.exceptions import APIException


class ResourcePermissionException(APIException):
    status_code = 403
    default_detail = 'You don´t have permissions to perform this action'
    default_code = 'resource_perm_exception'
from rest_framework.exceptions import APIException

class MissingParams(APIException):
    status_code = 422
    default_detail = 'There are missing required query params to handle request.'
    default_code = 'missing_params'
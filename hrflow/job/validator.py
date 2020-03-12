def validate_job_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("job_id must be string")
    return value


def validate_job_reference(value, acceptnone=True):
    if value is None:
        if acceptnone is False:
            raise TypeError("job_reference must not be None")
        else:
            return value


def validate_timestamp(value, var_name="timestamp"):
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    if not isinstance(value, str) and value is not None:
        raise TypeError("{} must be string or a int".format(var_name))
    return value
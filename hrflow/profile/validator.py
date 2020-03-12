import magic
import os


SERNIORITY_VALUES = ["all", "senior", "junior"]
STAGE_VALUES = [None, "new", "yes", "later", "no"]
SORT_BY_VALUES = ["date_reception", "date_creation", "location", "location_experience", "location_education",
                  "score_semantic", "score_predictive"]
ORDER_BY_VALUES = [None, "desc", "asc"]
VALID_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.doc', '.docx', '.rtf', '.dotx', '.odt', '.odp', '.ppt',
                    '.pptx', '.rtf', '.msg']
INVALID_FILENAME = ['.', '..']
TRAINING_METADATA_MANDATORY_FIELD = {'job_reference': lambda x: validate_job_reference(x, False),
                                     'stage': lambda x: validate_stage(x),
                                     'stage_timestamp': lambda x: validate_timestamp(x, 'stage_timestamp'),
                                     'rating': lambda x: validate_rating(x),
                                     'rating_timestamp': lambda x: validate_rating(x)}


def validate_dict(value, var_name="profile_data"):
    if not isinstance(value, dict):
        raise TypeError("{} should be a dict dict not a {}".format(var_name, value.__class__.__name__))
    return value


def get_file_metadata(file_path, profile_reference):
    try:
        return (
            os.path.basename(file_path) + profile_reference,  # file_name
            None,
            magic.Magic(True).from_file(file_path)
        )
    except Exception as e:
        raise Exception(repr(e))


def validate_source_id(value):
    if not isinstance(value, str):
        raise TypeError("source_id must be a string")
    return value


def validate_source_ids(value):
    if not value or not all(isinstance(elt, str) for elt in value):
        raise TypeError("source_ids must contain list of strings")
    return value


def validate_training_metadata(value):
    if not isinstance(value, list):
        raise TypeError("training_metadata must be a list of dict")
    if len(value) == 0:
        return value
    if not isinstance(value[0], dict):
        raise TypeError("training_metadata must be a list of dict")
    for metadata in value:
        for mandat_field, field_validator in TRAINING_METADATA_MANDATORY_FIELD.items():
            if mandat_field not in metadata:
                raise ValueError("Trainig metadata '{}' must have {} field.".format(metadata, mandat_field))
            field_validator(metadata[mandat_field])
    return value





def validate_seniority(value):
    if value not in SERNIORITY_VALUES:
        raise ValueError("seniority value must be in {}".format(str(SERNIORITY_VALUES)))

    return value


def validate_stage(value):
    if value is None:
        return value
    if value not in STAGE_VALUES:
        raise ValueError("stage value must be in {} not {}".format(str(STAGE_VALUES), value))

    return value


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

    if not isinstance(value, str) and value is not None:
        raise TypeError("job_reference must be string")

    return value


def validate_profile_reference(value):
    if value is None:
        return value
    if not isinstance(value, str) and value is not None:
        raise TypeError("profile_reference must be string not {}".format(value))

    return value


def validate_page(value):
    if not isinstance(value, int):
        raise TypeError("page must be 'int'")

    return value


def validate_limit(value):
    if not isinstance(value, int):
        raise TypeError("limit must be 'int'")

    return value


def validate_rating(value):
    if not isinstance(value, int):
        raise TypeError("rating must be 'int'")

    return value


def validate_order_by(value):
    if value not in ORDER_BY_VALUES:
        raise ValueError("order_by value must be in {}".format(str(ORDER_BY_VALUES)))

    return value


def validate_sort_by(value):
    if value not in SORT_BY_VALUES:
        raise ValueError("sort_by value must be in {}".format(str(SORT_BY_VALUES)))

    return value


def validate_timestamp(value, var_name="timestamp"):
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    if not isinstance(value, str) and value is not None:
        raise TypeError("{} must be string or a int".format(var_name))
    return value


def is_valid_extension(file_path):
    ext = os.path.splitext(file_path)[1]
    if not ext:
        return False
    return (ext in VALID_EXTENSIONS or ext.lower() in VALID_EXTENSIONS)


def is_valid_filename(file_path):
    name = os.path.basename(file_path)
    return name not in INVALID_FILENAME


def get_files_from_dir(dir_path, is_recurcive):
    file_res = []
    files_path = os.listdir(dir_path)

    for file_path in files_path:
        true_path = os.path.join(dir_path, file_path)
        if os.path.isdir(true_path) and is_recurcive:
            if is_valid_filename(true_path):
                file_res += get_files_from_dir(true_path, is_recurcive)
            continue
        if is_valid_extension(true_path):
            file_res.append(true_path)
    return file_res


def validate_id(self, value, field_name=''):
    if not isinstance(value, str) and value is not None:
        raise TypeError("{} must be string".format(field_name))

    return value


def format_fields(fields):
    return {k: 1 for k in fields}


def validate_profile_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("profile_id must be string")

    return value
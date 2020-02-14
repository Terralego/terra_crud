import base64
import mimetypes

from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class

from terra_geocrud import settings as app_settings


def get_info_content(value):
    if value:
        return value.split(';base64,')
    else:
        return None, None


def get_storage():
    StorageClass = get_storage_class(import_path=app_settings.TERRA_GEOCRUD['DATA_FILE_STORAGE_CLASS'])
    return StorageClass()


def generate_storage_file_path(prop, value, feature):
    file_info, file_content = get_info_content(value)

    if file_info:
        # guess filename and extension
        infos = file_info.split(';') if file_info else ''
        try:
            # get name
            file_name = infos[1].split('=')[1]
        except IndexError:
            extension = mimetypes.guess_extension(infos[0].split(':')[1])
            file_name = f"{prop}{extension}"

        # build name in storage
        return f'terra_geocrud/features/{feature.pk}/data_file/{prop}/{file_name}'


def store_data_file(storage, storage_file_path, file_content):
    storage.save(storage_file_path, ContentFile(base64.b64decode(file_content)))


def get_storage_file_url(storage_file_path):
    # check if there is file in storage, else store it
    if storage_file_path:
        storage = get_storage()
        return storage.url(storage_file_path)


def get_storage_path_from_infos(infos):
    """ path is stored behind name= """
    file_infos = infos.split(';')
    return file_infos[1].split('name=')[-1]


def get_storage_path_from_value(value):
    infos, content = get_info_content(value)
    return get_storage_path_from_infos(infos)

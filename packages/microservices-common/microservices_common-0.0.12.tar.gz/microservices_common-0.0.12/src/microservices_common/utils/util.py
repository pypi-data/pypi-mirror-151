import os
import logging
import json
import random
import time
from datetime import datetime
import copy


class Util:

    @classmethod
    def check_if_integer(cls, key, value):
        try:
            convert_to_int = int(value)
        except:
            logging.error(
                u"Key: {0}, does not contain a valid integer value. Value is: {1}".format(key, value))
            return False
        return True

    @classmethod
    def check_if_float(cls, key, value):
        try:
            convert_to_float = float(value)
        except:
            logging.error(
                u"Key: {0}, does not contain a valid float value. Value is: {1}".format(key, value))
            return False
        return True

    @classmethod
    def check_if_json(cls, key, value):
        try:
            convert_to_json = json.loads(value)
        except:
            logging.error(
                u"Key: {0}, does not contain a valid JSON value. Value is: {1}".format(key, value))
            return False
        return True

    @classmethod
    def check_if_string(cls, key, value):
        try:
            convert_to_string = str(value)
        except:
            logging.error(
                u"Key: {0}, does not contain a valid string value. Value is: {1}".format(key, value))
            return False
        return True

    @classmethod
    def check_if_true(cls, key, value):
        new_value = None
        if isinstance(value, bool):
            new_value = str(value).lower()
        elif isinstance(value, bytes):
            new_value = value.lower()
        elif isinstance(value, str):
            new_value = value.lower()

        if new_value and new_value == 'true':
            return True
        else:
            logging.info(
                u"Key: {0}, does not contain a valid TRUE boolean value. Value is: {1}".format(key, value))
            return False

    @classmethod
    def check_if_false(cls, key, value):
        new_value = None
        if isinstance(value, bool):
            new_value = str(value).lower()
        elif isinstance(value, bytes):
            new_value = value.lower()
        elif isinstance(value, str):
            new_value = value.lower()

        if new_value and new_value == 'false':
            return True
        else:
            logging.info(
                u"Key: {0}, does not contain a valid FALSE boolean value. Value is: {1}".format(key, value))
            return False

    @classmethod
    def check_attribute_type(cls, key, value):
        if isinstance(value, bytes):
            logging.info(u"Key: {0}, contains a string object".format(key))
            return 'string'
        elif isinstance(value, str):
            logging.info(u"Key: {0}, contains a unicode object".format(key))
            return 'string'
        elif isinstance(value, dict):
            logging.info(u"Key: {0}, contains a dict object".format(key))
            return 'dict'
        elif isinstance(value, list):
            logging.info(u"Key: {0}, contains a list object".format(key))
            return 'list'

    @classmethod
    def generate_random_string(cls):
        import uuid
        return str(uuid.uuid4())

    @classmethod
    def upload_file_to_bucket(cls, payload, company_id, unique_id, unique_key):
        from google.cloud import storage
        if not company_id:
            company_id = 9999999999999999
        try:
            GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
            GCS_ROUTE_OPTIMIZATION_RESULT_PATH_PREFIX = os.getenv(
                'GCS_ROUTE_OPTIMIZATION_RESULT_PATH_PREFIX')

            bucket_name = GCS_BUCKET_NAME
            destination_blob_name = GCS_ROUTE_OPTIMIZATION_RESULT_PATH_PREFIX.format(
                company_id=company_id,
                optimization_id=unique_id)

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob('{}_{}'.format(
                destination_blob_name, unique_key))

            # blob.upload_from_string(data=json.dumps({'payload': payload}), content_type='application/json')
            print(u'file path is : {} '.format(payload))
            with open(payload, "rb") as my_file:
                blob.upload_from_file(my_file, num_retries=10)
            blob.make_public()
            print(u"Blob {} is publicly accessible at {}".format(
                blob.name, blob.public_url))
            return blob.public_url
        except Exception as file_upload_exception:
            print('error uploading data to bucket, optimization will not be initiated')
            print(file_upload_exception)
            return None

    @classmethod
    def save_and_upload_file_to_bucket(cls, filename, company_id, unique_id, unique_key, data=None, file_to_save=None, file_path_to_save=None):
        if data is not None:
            file_path_to_save = os.path.join('/', filename)
            file_to_save = open(file_path_to_save, "w")
            file_to_save.writelines([json.dumps(data)])
            file_to_save.close()
        elif not file_to_save or not file_path_to_save:
            return None
        print('file_path_to_save: {}'.format(file_path_to_save))
        return cls.upload_file_to_bucket(payload=file_path_to_save, company_id=company_id, unique_id=unique_id, unique_key=unique_key)

    @classmethod
    def download_file(cls, path, name=None):
        import requests
        try:
            file_download_request = requests.get(path)
            if file_download_request.status_code != 200:
                return None
        except Exception as e:
            print(e)
            return None
        return file_download_request.content

    @classmethod
    def get_request_content(cls, request):
        request_content = None
        if request.method == 'POST':
            if request.headers.get('Content-Type') == 'x-www-form-urlencoded':
                request_content = request.form.to_dict()
            else:
                request_content = request.get_json()
        elif request.method == 'GET':
            request_content = request.args.to_dict()

        query_params = request.args.to_dict()

        print('query_params : ', query_params)
        print('request_content : ', request_content)

        return request_content, query_params

    @classmethod
    def log(cls, msg):
        print('{} {}'.format(datetime.now(), msg))

    @classmethod
    def get_owner_from_auth(cls, auth_info):
        from microservices_common.exceptions import OwnerNotFound

        owner = auth_info.get('user', dict()).get('company_id', None)
        if not owner:
            raise OwnerNotFound()
        return owner

    @classmethod
    def is_valid_uuid(cls, uuid_to_test, version=4):
        from uuid import UUID
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    @classmethod
    def generate_headers_for_arrivy_from_request(cls, request):
        headers = dict(request.headers)
        if headers.get('Host'):
            del headers['Host']
        if headers.get('Content-Length'):
            del headers['Content-Length']
        if headers.get('Re-Cookie'):
            headers['Cookie'] = headers.get('Re-Cookie')

        return headers

    @classmethod
    def load_dict(cls, _json):
        _json = _json if _json else dict()
        if _json and Util.check_attribute_type('_json', _json) != 'dict':
            return json.loads(_json)
        return _json

    @classmethod
    def is_admin(cls, request):
        import os
        return request.headers.get('Admin-Key') and request.headers.get('Admin-Key') == os.getenv('ADMIN_KEY')

    @classmethod
    def print_traceback(cls):
        import traceback
        print(traceback.format_exc())

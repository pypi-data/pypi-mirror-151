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
    def submit_request_for_geo_coding(cls, here_payload):
        import requests
        from xml.etree import ElementTree

        print('going to call here geocoding API')
        url = "https://batch.geocoder.ls.hereapi.com/6.2/jobs?gen=8&app_id={}&app_code={}&action=run&mailto=omega@getnada.com&header=true&indelim=%7C&outdelim=%7C&outcols=displayLatitude,displayLongitude,locationLabel,houseNumber,street,district,city,postalCode,county,state,country&outputCombined=true&apiKey={}".format(
            os.getenv('APP_ID'), os.getenv('APP_CODE'), os.getenv('API_KEY'))

        print('here geocoding API final url is : ', url)

        headers = {
            'Content-Type': 'text/plain'
        }

        try:
            response = requests.request(
                "POST", url, headers=headers, data=here_payload)
            print(response)
            print(response.text)
            if response.status_code == 200:
                root = ElementTree.fromstring(response.content)
                try:
                    status, request_id = None, None
                    if root[0][1].tag == 'Status':
                        status = root[0][1].text
                    if root[0][0][0].tag == 'RequestId':
                        request_id = root[0][0][0].text
                    print(status, request_id)
                    if status == 'accepted' and request_id:
                        # update results with request id
                        print(
                            'here geocoding api request accepted, should start polling for results')
                        return 'success', dict(here_geocoding_request_id=request_id, status=status)
                    else:
                        print('here geocoding api request not accepted')
                        return 'error', dict(results={'error_info': {'message': 'here geocoding api request not accepted'}})
                except IndexError as index_error:
                    print(index_error)
                    # update optimization with error
                    return 'error', dict(results={'error_info': {'message': 'error parsing geocoding input request response'}})
            else:
                # update optimization with error
                return 'error', dict(results={'error_info': {'message': 'error sending geocoding input request'}})

        except Exception as e:
            print('exception in here api')
            print(e)
            return 'error', dict(results={'error_info': {'message': 'exception in here api {}'.format(e.message)}})

    @classmethod
    def start_polling_for_geocoding_results(cls, here_geocoding_request_id):
        import requests
        from xml.etree import ElementTree
        url = "https://batch.geocoder.ls.hereapi.com/6.2/jobs/{}?&app_id={}&app_code={}&action=status&apiKey={}".format(
            here_geocoding_request_id, os.getenv('APP_ID'), os.getenv('APP_CODE'), os.getenv('API_KEY'))

        poll_count = 0
        sleep_time = 5
        max_poll_tries = 30
        while poll_count < max_poll_tries:
            print('polling for here geocoding results for geocoding_request_id : {}, poll_count : {}'.format(
                here_geocoding_request_id, poll_count))
            try:
                response = requests.request("GET", url)
                print(response)
                print(response.text)
                if response.status_code == 200:
                    root = ElementTree.fromstring(response.content)
                    try:
                        status, request_id = None, None
                        if root[0][1].tag == 'Status':
                            status = root[0][1].text
                        if root[0][0][0].tag == 'RequestId':
                            request_id = root[0][0][0].text
                        print(status, request_id)
                        if status == 'completed' and request_id:
                            # update results with request id
                            return 'success', dict(here_geocoding_request_status=status)
                        elif status in ['cancelled', 'deleted', 'failed']:
                            print(
                                'here geocoding api request status is {}'.format(status))
                            return 'error', dict(results={'error_info': {'message': 'here geocoding api request status is {}'.format(status)},
                                                          'here_geocoding_request_status': status})
                    except IndexError as index_error:
                        print(index_error)
                        # update optimization with error
                        return 'error', dict(results={'error_info': {'message': 'error parsing polling response'}})
                else:
                    print(
                        'here geocoding polling api request returned non 200 status code')
                    return 'error', dict(results={'error_info': {'message': 'here geocoding polling api request returned non 200 status code'}})
            except Exception as e:
                print('exception in here polling api')
                print(e)
                return 'error', dict(results={'error_info': {'message': 'exception in here polling api {}'.format(e.message)}})

            poll_count += 1
            time.sleep(sleep_time)
            sleep_time += 3

        print('here geocoding polling api request timed out')
        return 'error', dict(results={'error_info': {'message': 'here geocoding polling api request timed out'}})

    @classmethod
    def dowload_and_save_here_geocoded_file(cls, here_geocoding_request_id, serialized_optimization):
        import requests
        import zipfile
        import io
        zip_file_extracted_name, zip_file_extracted_path = None, None
        url = "https://batch.geocoder.ls.hereapi.com/6.2/jobs/{}/result?app_id={}&app_code={}&apiKey={}".format(
            here_geocoding_request_id, os.getenv('APP_ID'), os.getenv('APP_CODE'), os.getenv('API_KEY'))

        payload = {}
        headers = {
            'Content-Type': 'application/octet-stream'
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload)

            if response.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(response.content))
                extracted = z.namelist()
                zip_file_extracted_name = extracted[0] if extracted else None
                if zip_file_extracted_name:
                    zip_file_extracted_path = cls.generate_random_string()
                    z.extractall(os.path.join(
                        '/', zip_file_extracted_path))
                    zip_file_extracted_path = os.path.join(
                        '/', zip_file_extracted_path, zip_file_extracted_name)
                    # upload geocoded file to bucket and save its info in result
                    geo_coded_file_bucket_url = cls.upload_file_to_bucket(payload=zip_file_extracted_path,
                                                                          company_id=cls.get_company_id(
                                                                              serialized_optimization=serialized_optimization),
                                                                          unique_id=serialized_optimization.get(
                                                                              'id'),
                                                                          unique_key=zip_file_extracted_name)
                    if geo_coded_file_bucket_url:
                        return 'success', dict(geo_coded_file_info=dict(
                            geo_coded_file_bucket_url=geo_coded_file_bucket_url,
                            geo_coded_file_name=zip_file_extracted_name,
                            geo_coded_file_path=zip_file_extracted_path
                        ))

                else:
                    return 'error', dict(results={'error_info': {'message': 'here geocoding api request completed, but no results file'}})
            else:
                return 'error', dict(results={'error_info': {'message': 'here geocoded zip file download api request returned non 200 status code'}})

        except Exception as e:
            print(e)
            print('exception in here geocoded zip file download api')
            return 'error', dict(results={'error_info': {'message': 'exception in here geocoded zip file download api'}})

    @classmethod
    def generate_lat_lng_dict_from_file(cls, file_path):
        lat_lng_dict = dict()

        with open(file_path) as fp:
            for i, line in enumerate(fp):
                if i > 0:
                    address = line.strip()
                    address_components = address.split('|')
                    if address_components and len(address_components) > 4:
                        recId = address_components[0]
                        lat = address_components[3]
                        lng = address_components[4]
                        location_label = address_components[5]
                        country = address_components[13]
                        state = address_components[12]
                        zip_code = address_components[10]
                        county = address_components[11]
                        city = address_components[9]
                        district = address_components[8]
                        houseNumber = address_components[6]
                        address_components = dict()
                        address_components.update({
                            'lat': lat,
                            'lng': lng,
                            'location_label': location_label,
                            'country': country,
                            'state': state,
                            'zip_code': zip_code,
                            'county': county,
                            'city': city,
                            'district': district,
                            'houseNumber': houseNumber})
                        if lat and lng and not lat_lng_dict.get(recId):
                            lat_lng_dict[str(recId)] = {
                                'lat': lat, 'lng': lng, 'location_label': location_label, 'address_components': address_components}
        return lat_lng_dict

    @classmethod
    def genrate_payload_for_matrix_API(cls, depot, task_start_addresses, task_end_addresses, depot_str,
                                       task_start_complete_addresses, task_end_complete_addresses,
                                       travel_mode='car'):

        all_origins = [depot]
        all_destinations = [depot]
        all_destinations_str = [depot_str]
        for task_address in task_end_addresses:
            all_origins.append(task_address)

        for (task_address, task_address_str) in zip(task_start_addresses, task_start_complete_addresses):
            all_destinations.append(task_address)
            all_destinations_str.append(task_address_str)

        profile = 'carFast'
        if travel_mode and travel_mode in ['car', 'truck']:
            if travel_mode == 'truck':
                profile = 'truckFast'
        payload = {
            'origins': [],
            'destinations': [],
            'profile': profile,
            'matrixAttributes': ['travelTimes', 'distances'],
            'regionDefinition': {
                'type': 'world'
            }
        }

        threshhold = int(os.getenv('MATRIX_CHUNK_SIZE'))
        payloads = []
        payload_info = dict(origins=all_origins, destinations=all_destinations)
        contains_chuck = False
        origin_batch = 0

        if len(all_origins) > threshhold:
            contains_chuck = True

            print(
                'origins are greater than threshold, need to divide matrix generation into chunks')
            origin_start = 0
            origin_end = threshhold
            destination_start = 0
            destination_end = threshhold

            while True:
                origins = all_origins[origin_start:origin_end]
                destinations = all_destinations[destination_start:destination_end]

                _payload = copy.deepcopy(payload)
                _payload.update(
                    dict(destinations=destinations, origins=origins))

                payloads.append(dict(payload=_payload, additional_info=dict(origin_count=len(
                    origins), destination_count=len(destinations), origin_batch=origin_batch)))

                if destination_end < len(all_destinations):
                    # there are more destinations left
                    print(
                        'there are more destinations left, increasing destination_start and destination_end')
                    destination_start += threshhold
                    destination_end += threshhold
                elif origin_end < len(all_origins):
                    # there are more origins left
                    origin_batch += 1
                    print(
                        'there are more origins left, increasing origin_start and origin_end and resetting destination_start and destination_end')
                    origin_start += threshhold
                    origin_end += threshhold
                    destination_start = 0
                    destination_end = threshhold
                else:
                    print('no more origins or destinations left, breaking loop')
                    break

        else:
            payload.update(
                {'origins': all_origins, 'destinations': all_destinations})
            payloads = [dict(payload=payload, additional_info=dict(origin_count=len(
                all_origins), destination_count=len(all_destinations), origin_batch=0))]

        payload_info.update(
            dict(contains_chuck=contains_chuck, payloads=payloads, max_origin_batch=origin_batch))
        return payload_info

    @classmethod
    def submit_request_for_time_distance_matrix_calculation(cls, payload):
        import requests
        here_maps_api_key = os.getenv('API_KEY')
        URL = 'https://matrix.router.hereapi.com/v8/matrix'
        token_uri = URL + "?apiKey=" + here_maps_api_key
        headers = {"Content-type": "application/json"}
        try:
            response = requests.post(
                token_uri, data=json.dumps(payload), headers=headers)
            res = response.json()
            print('Here maps time and distance matrix request response is')
            print(u'{}'.format(res))

            if res.get('status') == 'accepted':
                return 'success', dict(status=res.get('status'), matrix_id=res.get('matrixId'), matrix_status_url=res.get('statusUrl'))
            else:
                return 'error', dict(results={'error_info':
                                              {'message': 'here maps matrix request not accepted, status is {}'.format(res.get('status')),
                                               'complete_error': res}})

        except Exception as ex:
            print(ex)
            return 'error', dict(results={'error_info': {'message': 'here maps matrix request exception'}})

    @classmethod
    def start_polling_for_time_distance_matrix_results(cls, here_matrix_api_info):
        import requests

        poll_count = 0
        sleep_time = 5
        max_poll_tries = 30
        job_completed = False
        final_response = None
        resultant_matrix_id_for_polling = here_matrix_api_info.get(
            'matrix_id')
        resultant_status_url = here_matrix_api_info.get(
            'matrix_status_url')
        print('resultant_matrix_id_for_polling:{}'.format(
            resultant_matrix_id_for_polling))
        print('resultant_status_url:{}'.format(resultant_status_url))
        api_key = os.getenv('API_KEY')

        url = resultant_status_url + "?apiKey=" + api_key

        while poll_count < max_poll_tries:
            print('polling for time distance matrix results for matrix_id : {}, poll_count : {}'.format(
                resultant_matrix_id_for_polling, poll_count))
            try:
                final_response = requests.get(
                    url, timeout=60, allow_redirects=False).json()
                status = final_response.get('status')
                if status in ['cancelled', 'deleted', 'failed']:
                    print('here geocoding api request status is {}'.format(status))
                    return 'error', dict(
                        results={'error_info': {'message': 'here geocoding api request status is {}'.format(status)},
                                 'here_geocoding_request_status': status})
                elif status == 'completed':
                    job_completed = True
                    break

            except Exception as e:
                print(e)
                return 'error', dict(results={'error_info': {'message': 'here maps matrix fetch call exception'}})

            poll_count += 1
            time.sleep(sleep_time)
            sleep_time += 3

        if job_completed:
            print(final_response)
            status = final_response.get("status")

            final_result_url = final_response.get(
                "resultUrl") + "?apiKey=" + api_key
            final_result = requests.get(final_result_url, timeout=60).json()

            if final_result.get('matrix') is None:
                # update result status to failed with error_info
                return 'error', dict(results={
                    'error_info': {'message': 'matrix not found in response', 'complete_error': final_result}})

            return 'success', dict(matrix=final_result.get('matrix'))
        else:
            print('here matrix polling api request timed out')
            return 'error', dict(results={'error_info': {'message': 'here matrix polling api request timed out'}})

    @classmethod
    def is_matrix_valid(cls, matrix):
        errorCodes = matrix.get('errorCodes')
        if errorCodes:
            for errorCode in errorCodes:
                if errorCode not in [0, 3]:
                    return False
        return True

    @classmethod
    def populate_distance_and_time_data_from_matrix(cls, locations, distances, travel_times):
        time_distance_data = {}
        index = 0
        for i in range(len(locations)):
            origin_key = str('{},{}'.format(locations[i].get(
                'lat'),  locations[i].get('lng'))).replace(" ", "")

            for j in range(len(locations)):
                destination_key = str('{},{}'.format(locations[j].get(
                    'lat'), locations[j].get('lng'))).replace(" ", "")

                if origin_key != destination_key:
                    if origin_key not in time_distance_data:
                        time_distance_data.update({origin_key: {}})
                        # time_distance_data[origin_key].update(
                        #     {'selfAddress': locations[i]})

                    if destination_key not in time_distance_data[origin_key]:
                        time_distance_data[origin_key].update(
                            {destination_key: {}})

                    time_distance_data[origin_key][destination_key].update({
                        # 'address': locations[j],
                        'd': distances[index],
                        't': travel_times[index],
                        # 'duration_in_traffic': travel_times[index],
                    })
                index = index + 1

        return time_distance_data

    @classmethod
    def populate_minimum_distance_and_time_data_from_matrix(cls, all_origins, all_destinations, travel_times, distances, routes,
                                                            all_task_ids):
        task_to_location_dict = dict({'key': "__", 'index': 0})
        all_origins_len = len(all_origins)

        for i in range(len(all_origins) - 1):
            # commenting out old key structure, to reduce file size and keep key structure consistent with maximum_distance_and_time_data
            # origin_key = str({"lat": all_origins[
            #     i + 1].get('lat'), "lng": all_origins[i + 1].get('lng')}).replace(" ", "")
            origin_key = str('{},{}'.format(all_origins[i].get(
                'lat'),  all_origins[i].get('lng'))).replace(" ", "")
            task_to_location_dict.update(
                {all_task_ids[i]: {'key': origin_key, 'index': i + 1}})

        time_distance_data = {}

        for routeIndex in range(len(routes)):
            if len(routes[routeIndex]) == 1:
                continue
            for taskIndex in range(len(routes[routeIndex]) - 1):
                from_key = task_to_location_dict[routes[routeIndex][taskIndex]].get(
                    'key')
                from_index = task_to_location_dict[routes[routeIndex][taskIndex]].get(
                    'index')

                to_key = task_to_location_dict[routes[routeIndex]
                                               [taskIndex + 1]].get('key')
                to_index = task_to_location_dict[routes[routeIndex]
                                                 [taskIndex + 1]].get('index')

                time_distance_data = cls.get_time_and_distance_for_pair(
                    from_key, from_index, to_key, to_index, time_distance_data, all_origins, all_destinations, travel_times,
                    distances, all_origins_len)

        return time_distance_data

    @classmethod
    def get_time_and_distance_for_pair(cls, from_key, from_index, to_key, to_index, time_distance_data, all_origins,
                                       all_destinations, travel_times,
                                       distances, all_origins_len):
        index = (from_index * all_origins_len) + to_index

        origin = all_origins[from_index]
        destination = all_destinations[to_index]

        # commenting out old key structure, to reduce file size and keep key structure consistent with maximum_distance_and_time_data
        # origin_key = str({"lat": origin.get(
        #     'lat'), "lng": origin.get('lng')}).replace(" ", "")

        origin_key = str('{},{}'.format(origin.get(
            'lat'),  origin.get('lng'))).replace(" ", "")

        if origin_key not in time_distance_data:
            time_distance_data.update({origin_key: {}})
            # time_distance_data[origin_key].update(
            #     {"selfAddress": origin})

        # commenting out old key structure, to reduce file size and keep key structure consistent with maximum_distance_and_time_data
        # destination_key = str({"lat": destination.get(
        #     'lat'), "lng": destination.get('lng')}).replace(" ", "")

        destination_key = str('{},{}'.format(destination.get(
            'lat'), destination.get('lng'))).replace(" ", "")

        if destination_key not in time_distance_data[origin_key]:
            time_distance_data[origin_key].update(
                {destination_key: {}})

        time_distance_data[origin_key][destination_key].update({
            # "address": destination,
            "d": distances[index],
            "t": travel_times[index]
        })

        return time_distance_data

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
    def combine_matrixes(cls, chunks_info, matrixes, max_origin_batch):
        print('in combine_matrixes')
        final_matrix = []
        final_distance_matrix = []
        final_duration_matrix = []
        index = 0
        matrix_read_dict = dict()  # origin_batch_matrix_number : read_count
        completed_batch = []
        while len(completed_batch) <= max_origin_batch:

            for index, (payload, matrix) in enumerate(zip(chunks_info, matrixes)):
                origin_batch = payload.get('origin_batch')
                if origin_batch in completed_batch:
                    continue
                if origin_batch > 0 and (origin_batch - 1) not in completed_batch:
                    break

                destination_count = payload.get('destination_count')

                read_start = matrix_read_dict.get(
                    '{}_{}'.format(origin_batch, index), 0)
                temp_distance_matrix = matrix.get(
                    'distances')[read_start:(destination_count+read_start)]
                temp_duration_matrix = matrix.get(
                    'travelTimes')[read_start:(destination_count+read_start)]
                if not temp_distance_matrix or not temp_duration_matrix:
                    completed_batch.append(origin_batch)
                    break
                final_distance_matrix += temp_distance_matrix
                final_duration_matrix += temp_duration_matrix
                matrix_read_dict.update(
                    {'{}_{}'.format(origin_batch, index): (read_start + destination_count)})

        return final_distance_matrix, final_duration_matrix

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
        from exceptions import OwnerNotFound

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
    def remove_invalid_fields(cls, document, errors_tree):
        from collections import Mapping
        if errors_tree is None:
            return document
        filtered = {}
        for field, value in document.items():
            if field in errors_tree.descendants:
                continue
            if isinstance(value, Mapping):
                value = cls.remove_invalid_fields(value, errors_tree[field])
            filtered[field] = value
        return filtered

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

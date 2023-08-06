import os
import io
import numpy as np
import pandas as pd
import tarfile
from .logger import Logger
from .script_generator import ScriptGenerator
import yaml
import subprocess  # for deploy_to_kyma
import re  # for deploy_to_kyma
import stat
import shutil
import requests
import json
from google.cloud import storage
from googleapiclient import discovery
from googleapiclient import errors
from google.cloud import bigquery
from google.api_core.client_options import ClientOptions


class DwcGCP:
    def __init__(self,
                 project_name=None,
                 bucket_name=None):
        self.logger = Logger.get_instance()
        if project_name:
            self.project_name = project_name
        else:
            raise ValueError(
                'Error: Please iniate class with GCP project name')
        if bucket_name:
            self.bucket_name = bucket_name
        else:
            raise ValueError(
                'Error: Please iniate class with GCP Cloud Storage bucket name')

    def create_folder(self, bucket_name, destination_folder_name):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_folder_name)

        blob.upload_from_string('')

        self.logger.info('Created {} .'.format(
            destination_folder_name))

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        self.logger.info(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        self.logger.info(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )

    def create_bucket_class_location(self, bucket_name):
        """Create a new bucket in specific location with storage class"""
        # bucket_name = "your-new-bucket-name"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = storage_client.create_bucket(bucket, location="us")

        self.logger.info(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket

    def make_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def make_tar_bundle(self, output_filename='training.tar.gz', source_dir='training', destination='train/training.tar.gz'):

        self.make_tarfile(output_filename, source_dir)
        self.upload_blob(self.bucket_name, output_filename, destination)

    def train_model(self, jobId,
                    training_inputs):

        job_spec = {'jobId': jobId, 'trainingInput': training_inputs}
        project_id = 'projects/{}'.format(self.project_name)
        cloudml = discovery.build('ml', 'v1')
        request = cloudml.projects().jobs().create(body=job_spec,
                                                   parent=project_id)

        try:
            response = request.execute()
            self.logger.info('Training Job Submitted Succesfully')
            self.logger.info('Job status for {}.{}:'.format(
                self.project_name, jobId))
            self.logger.info('    state : {}'.format(response['state']))
#             self.logger.info('    consumedMLUnits : {}'.format(
#             response['trainingOutput']['consumedMLUnits']))

            # You can put your code for handling success (if any) here.

        # except errors.HttpError as err:
        except errors.HttpError as err:
            # Do whatever error response is appropriate for your application.
            # For this example, just send some text to the logs.
            # You need to import logging for this to work.
            self.logger.info('There was an error creating the training job.'
                             ' Check the details:')
            self.logger.info(err._get_reason())

    def deploy(self, model_name, model_location,  version, region, prediction_location='', custom_predict=None, module_name=None, onlinePredictionLogging=False, onlinePredictionConsoleLogging=False):

        project_id = 'projects/{}'.format(self.project_name)

        model_request_dict = {'name': model_name, "regions": [
            region], "onlinePredictionLogging": onlinePredictionLogging, "onlinePredictionConsoleLogging": onlinePredictionConsoleLogging}
#         model_request_dict = {'name': model_name}

        ml = discovery.build('ml', 'v1')

        endpoint_id = region

        model_request = ml.projects().models().create(
            parent=project_id, body=model_request_dict)

        try:
            response = model_request.execute()
            self.logger.info(response)
        except errors.HttpError as err:
            # Something went wrong, print out some information.
            self.logger.info(
                'There was an error creating the model. Check the details:')
            self.logger.info(err._get_reason())

        model_path = self.project_name + '/models/' + model_name
        model_id = 'projects/{}'.format(model_path)

        deployment_uri = 'gs://' + self.bucket_name + model_location

        version_create_request = {
            "name": 'version',
            "description": '',
            "isDefault": False,
            "deploymentUri": deployment_uri,
            "framework": 'SCIKIT_LEARN',
            'runtimeVersion': '2.5'
        }

        if custom_predict and module_name:
            package_uri = 'gs://' + self.bucket_name + \
                '/' + prediction_location + custom_predict

            version_create_request = {
                "name": 'version',
                "description": '',
                "isDefault": False,
                "deploymentUri": deployment_uri,
                "packageUris": [package_uri],
                #                 "framework": 'SCIKIT_LEARN',
                'runtimeVersion': '2.5',
                "predictionClass": module_name
            }

        version_request = ml.projects().models().versions().create(
            parent=model_id, body=version_create_request)

        try:
            response = version_request.execute()
            self.logger.info(response)
        except errors.HttpError as err:
            # Something went wrong, print out some information.
            self.logger.info(
                'There was an error creating the model. Check the details:')
            self.logger.info(err._get_reason())

    def enable_logging(self, model_name, version, samplingPercentage, datasetName, tableName, createDataset=False, createTable=False):

        model_id = 'projects/' + self.project_name + \
            '/models/' + model_name + '/versions/' + version

        ml = discovery.build('ml', 'v1')

        if createTable:
            client = bigquery.Client()

            if createDataset:
                dataset_id = self.project_name + "." + datasetName
                dataset = bigquery.Dataset(dataset_id)
                dataset.location = "US"
                dataset = client.create_dataset(dataset, timeout=30)
                self.logger.info("Created dataset {}.{}".format(
                    client.project, dataset.dataset_id))

            table_id = self.project_name + "." + datasetName + "." + tableName

            schema = [
                bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
                bigquery.SchemaField(
                    "model_version", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("time", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("raw_data", "STRING", mode="REQUIRED"),
                bigquery.SchemaField(
                    "raw_prediction", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("groundtruth", "STRING", mode="NULLABLE")

            ]

            table = bigquery.Table(table_id, schema=schema)
            table = client.create_table(table)  # Make an API request.
            self.logger.info(
                "Created table {}.{}.{}".format(
                    table.project, table.dataset_id, table.table_id)
            )

        logging = {
            "samplingPercentage": samplingPercentage,
            "bigqueryTableName": tableName
        }

        version_patch_request = {

            "requestLoggingConfig": logging
        }

        version_request = ml.projects().models().versions().patch(
            name=model_id, updateMask=version_patch_request)

        try:
            response = version_request.execute()
            self.logger.info(response)
        except errors.HttpError as err:
            # Something went wrong, print out some information.
            self.logger.info(
                'There was an error creating the model. Check the details:')
            self.logger.info(err._get_reason())

    def predict(self, data, model_name):
        endpoint = 'https://ml.googleapis.com'
        client_options = ClientOptions(api_endpoint=endpoint)
        ml = discovery.build('ml', 'v1', client_options=client_options)

        request_body = {
            'instances': data.values.tolist()
        }
        request = ml.projects().predict(
            # name='projects/PROJECT_ID/models/MODEL_NAME/VERSION_NAME',
            # name='projects/sap-ti-ci-sce/models/linear_reg_final_deploy',
            name='projects/' + self.project_name + '/models/' + model_name,
            body=request_body)

        response = request.execute()
        self.logger.info(response)
        return response

    def deploy_to_kyma(self, profile_name, key_file, image_name,  custom_predictor=None, download_model=True, model_location=None, initial_instance_count=1):

        if custom_predictor:
            self.logger.info('Copying Predictor File...')
            shutil.copyfile('/home/jupyter/' +
                            custom_predictor, 'predictor.py')
#             process = subprocess.Popen(
#             ['sh', 'cp', '/home/jupyter/' + custom_predictor + ' predictory.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             com = process.communicate()
#             self.logger.info(com[0])
            self.logger.info('Checking for Predictor File...')
            if os.path.exists("predictor.py") == False:
                self.logger.info('Predictor file not found...')
                self.logger.info(
                    'Please check if this is the correct path /home/jupyter/' + custom_predictor)

            else:
                self.logger.info('Succesfully copied Predictor File...')
        if download_model:
            self.logger.info('Downloading Model File...')
            self.download_blob(self.bucket_name, model_location, 'model.pkl')

        self.logger.info('Checking for Model File...')
        if os.path.exists("model.pkl") == True:
            self.logger.info('Model file found...')

        self.logger.info('checking if user has a requirements.txt...')
        has_requirements = False
        if os.path.exists("requirements.txt") == True:
            self.logger.info(' user has a requirements.txt.')
            has_requirements = True
        self.logger.info(' user does not have a requirements.txt.')

        sg = ScriptGenerator()

        sg.write_flaskapp('api.py', custom_predictor)

        self.logger.info('....\t\t api.py created')

        self.logger.info('....\t Checking kubeconfig.yml')
        if os.path.exists("kubeconfig.yml") == False:
            self.logger.info(
                "Ensure you have downloaded the kubeconfig.yml from the Kyma Console UI. This is found in the user menu.")
        self.logger.info('User has a kubeconfig.yml.')

        stream = open('kubeconfig.yml', 'r')
        data = yaml.load(stream,  yaml.BaseLoader)
        items = data.get('clusters')
        host_name = items[0]['name']

        sg.write_dockerfile('Dockerfile', has_requirements,
                            predictor=custom_predictor)

        self.logger.info('....\t Dockerfile created')

        sg.write_deployment('deployment.yaml',
                            initial_instance_count, image_name, self.project_name)
        self.logger.info('....\t deployment.yaml created')

        self.logger.info('Installing kubectl...')

        process = subprocess.Popen(
            ['install_kubectl.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        com = process.communicate()
        self.logger.info(com[0])
        self.logger.info(com[1])

        self.logger.info(
            'Building, pushing, and deploying container and creating endpoint....')
        for path in self._run_build_and_push_script(project_name=self.project_name, image=image_name,  profile_name=profile_name, KEY_FILE=key_file):
            self.logger.info(path)

        endpoint = 'https://'+image_name+'.'+host_name
        self.logger.info('Your endpoint is '+endpoint)

        self.logger.info("\tTo invoke: "+endpoint+'/predict')

        self.logger.info('Done.')

    def _run_build_and_push_script(self, project_name, image, profile_name, KEY_FILE):
        # changed for packaging
        # st = os.stat(image+'/build_and_push.sh')
        # os.chmod(image+'/build_and_push.sh', st.st_mode | stat.S_IEXEC)
        try:
            args = [project_name, image, profile_name, KEY_FILE]
            # changed for packaging
            # process = subprocess.Popen([image+'/build_and_push.sh']+ args, stdout=subprocess.PIPE, shell=False)
            process = subprocess.Popen(
                ['build_and_push.sh'] + args, stdout=subprocess.PIPE, shell=False)
            while True:
                line = process.stdout.readline().rstrip().decode()
                if not line:
                    break
                yield line
            streamdata = process.communicate()[0]
            if process.returncode == 1:
                raise Exception('Error in build_and_push.sh')
        except Exception as e:
            self.logger.error(e)
#             self._delete_folder(image)
            raise

    def invoke_kyma_endpoint(self, api, payload_path=None):
        try:
            with open(payload_path, 'r') as j:
                contents = json.loads(j.read())

            r = requests.post(
                api, data=json.dumps(contents))
            # print(json.loads(r.get_data().decode("utf-8")))
            # print(r.json())

            # if payload_path is not None:
            #     # payload = open(payload_path)
            #     with open(payload_path, 'r') as j:
            #         payload = json.loads(j.read())

            #     self.logger.info(type(payload))
            #     r = requests.post(
            #         api, data=payload)
            # else:
            #     if payload is None:
            #         raise Exception(
            #             'You must provide a path to your payload, or the payload itself.')
            #     r = requests.post(
            #         api, data=payload)
            # # headers = {'Content-Type': content_type, 'Accept': accept}
            # r = requests.post(api, data=payload, headers=headers)

            return r.json()
        except Exception as e:
            self.logger.info(e)
            raise

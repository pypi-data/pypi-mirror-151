import os
import io
import numpy as np
import pandas as pd
# from dbconnection import DbConnection
# from hdbcli import dbapi
import shutil
import datetime
import subprocess # for deploy_to_kyma
import re # for deploy_to_kyma
import stat
import yaml # for deploy_to_kyma
import requests # for invoke_kyma_endpoint
from .script_generator import ScriptGenerator # for deploy_to_kyma #changed for packaging
from .logger import Logger #for logging
from pkg_resources import resource_filename # for bash popne
try:
    import boto3
    import botocore
    import sagemaker
    from botocore.client import ClientError
    from sagemaker import get_execution_role
    from sagemaker.sklearn.estimator import SKLearn
except:
    pass

class DwcSagemaker:
    def __init__(self,  
                 prefix='model-data', 
                 bucket_name=None):

        self.logger = Logger.get_instance()
        self.region = boto3.session.Session().region_name
        if self.region is None:
            self.logger.info('region is none...Did you set your AWS environment credentials?')
        else:
            self.logger.info('Got region %s ', self.region)
        try:
            self.role = get_execution_role()
            self.prefix = prefix
            bucket_name = self._get_bucket_name(bucket_name)
            self.bucket_name = bucket_name
            s3 = boto3.resource('s3')
            
            
            
            # try:
            #     s3.meta.client.head_bucket(Bucket=bucket_name)
            # except:
            try:
                if self.region == 'us-east-1':
                    s3.create_bucket(Bucket=bucket_name)
                else:
                    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})
                self.logger.info('Bucket created in %s', self.region)
            except Exception as e:
                if 'BucketAlreadyOwnedByYou' in str(e):
                    self.logger.info('Using existing bucket')
                else:
                    self.logger.error('S3 error: %s', e)
                    raise
        except Exception as e:
            pass

    def _get_bucket_name(self, bucket_name):
        if bucket_name:
            return bucket_name
        else:
            return 'federatedml-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


    # def load_dwc_dataset(self, table, size=1):
    #     db = DbConnection()
    #     res, column_headers = db.get_data_with_headers(table, size)
    #     return pd.DataFrame(res, columns=column_headers)
    
    # def execute_query(self, query):
    #     db = DbConnection()
    #     res, column_headers = db.execute_query(query)
    #     return pd.DataFrame(res, columns=column_headers)

#     def load_sagemaker_model(self, algorithm):
#         return sagemaker.image_uris.retrieve(algorithm, self.region, "latest"

    def _upload_dataframe(self, data, content_type='csv', which='train', s3distributionType=None):
        data.to_csv(which+'.csv', index=False, header=False)
        boto3.Session().resource('s3').Bucket(self.bucket_name).Object(os.path.join(self.prefix, '{}/{}.csv'.format(which, which))).upload_file(which+'.csv')     
        s3_input = sagemaker.inputs.TrainingInput(s3_data='s3://{}/{}/{}'.format(self.bucket_name, self.prefix, which), content_type=content_type, distribution=s3distributionType)
        return s3_input
    
    def _upload_protobuf(self, data, which='train', s3distributionType=None):
        boto3.Session().resource('s3').Bucket(self.bucket_name).Object(os.path.join(self.prefix, '{}/{}.protobuf'.format(which, which))).upload_fileobj(data)
        s3_input_path = sagemaker.inputs.TrainingInput(s3_data='s3://{}/{}/{}'.format(self.bucket_name, self.prefix, which), distribution=s3distributionType)
        #'s3://{}/{}/{}'.format(self.bucket_name, self.prefix, which)
        return s3_input_path
    
    def _upload_file(self, data_file, which='train', s3distributionType=None):
        boto3.Session().resource('s3').Bucket(self.bucket_name).Object(os.path.join(self.prefix, '{}/{}'.format(which, data_file))).upload_file(data_file)
        s3_input_path = sagemaker.inputs.TrainingInput(s3_data='s3://{}/{}/{}'.format(self.bucket_name, self.prefix, which), distribution=s3distributionType)
        # s3_input_path = 's3://{}/{}/{}'.format(self.bucket_name, self.prefix, which)
        return s3_input_path
    
    def _upload_data(self, data, content_type=None, which='train', s3distributionType=None):
        if isinstance(data, pd.core.frame.DataFrame):
            s3_input_path = self._upload_dataframe(data, content_type=content_type, which=which, s3distributionType=s3distributionType)
            
        elif isinstance(data, io.BytesIO):
            s3_input_path = self._upload_protobuf(data, which=which, s3distributionType=s3distributionType)
            
        elif isinstance(data, str) and (data.endswith(('.json', '.json.gz', '.csv', '.txt'))):
            s3_input_path = self._upload_file(data, which=which)
            
        return s3_input_path

    def train_sagemaker_model(self, 
                              train_data,
                              framework,
                              framework_version='latest',
                              train_content_type='csv',
                              test_content_type='csv',
                              instance_count=1,
                              instance_type=None,
                              base_job_name=None,
                              hyperparameters=None,
                              test_data=None,
                              s3distributionTypeTrain=None,
                              s3distributionTypeTest=None):
        
        model_container = sagemaker.image_uris.retrieve(framework, self.region, framework_version)
        
        self.logger.info('{} framework loaded'.format(framework))
        
        s3_input_train = self._upload_data(train_data, train_content_type,s3distributionType=s3distributionTypeTrain)
        
        self.logger.info('Training data uploaded')
        
        if test_data is not None:
            s3_input_test = self._upload_data(test_data, test_content_type, which='test', s3distributionType=s3distributionTypeTest)
                
            self.logger.info('Test data uploaded')

        sess = sagemaker.Session()
        clf = sagemaker.estimator.Estimator(model_container, 
                                            self.role, 
                                            instance_count=instance_count, 
                                            instance_type=instance_type, 
                                            output_path='s3://{}/{}/output'.format(self.bucket_name, self.prefix),
                                            base_job_name=base_job_name,
                                            sagemaker_session=sess)

        clf.set_hyperparameters(**hyperparameters)
        
        if test_data is not None:
            clf.fit({'train': s3_input_train, 'test': s3_input_test})            
        else:
            clf.fit({'train': s3_input_train})
        
        return clf
    
    def train_sklearn_model(self, 
                            train_data=None, 
                            test_data=None, 
                            content_type=None,
                            train_script=None, 
                            source_dir=None,
                            instance_count=1,
                            instance_type=None, 
                            base_job_name=None,
                            hyperparameters=None,
                            wait=False,
                            logs='All',
                            download_output=False):
        
        FRAMEWORK_VERSION = "0.23-1"

        s3_input_train = self._upload_data(train_data, content_type)
        self.logger.info('Training data uploaded')
    
        if test_data is not None:
            s3_input_test = self._upload_data(test_data, content_type, which='test')
            self.logger.info('Test data uploaded')
    
        
        sklearn_estimator = SKLearn(entry_point=train_script,
                                    source_dir=source_dir,
                                    role=self.role,
                                    instance_count=instance_count,
                                    instance_type=instance_type,
                                    framework_version=FRAMEWORK_VERSION,
                                    base_job_name=base_job_name,
                                    hyperparameters=hyperparameters)
        
        if test_data is not None:
            sklearn_estimator.fit({'train': s3_input_train, 'test': s3_input_test}, 
                wait=wait,
                logs=logs)
        else:
            sklearn_estimator.fit({'train': s3_input_train},
                wait=wait,
                logs=logs)

        if download_output:
            sklearn_estimator.latest_training_job.wait(logs='None')
            return_code = self._download_artifacts(artifact_type='Output', clf=sklearn_estimator)
            if return_code == -1:
                self.logger.info('Did you upload anything to the output folder in S3?')

        return sklearn_estimator
    
    def _cleanup_resources(self):
        bucket_to_delete = boto3.resource('s3').Bucket(self.bucket_name)
        bucket_to_delete.objects.filter(Prefix=self.prefix).delete()

    def deploy(self, clf, initial_instance_count, instance_type, endpoint_name=None, cleanup_resources=True):
        predictor = clf.deploy(initial_instance_count=initial_instance_count, endpoint_name=endpoint_name, instance_type=instance_type)
        if cleanup_resources == True:
            self._cleanup_resources()
        return predictor.endpoint_name
            
            
    def predict(self, endpoint_name, body, content_type='', accept=''):
        client = boto3.client('sagemaker-runtime', region_name=self.region)
        response = client.invoke_endpoint(EndpointName=endpoint_name,
                                          Body=body,
                                          ContentType=content_type,
                                          Accept=accept)
        return response['Body'].read().decode()
    
    def _download_artifacts(self, artifact_type, clf):
        sm_boto3 = boto3.client('sagemaker')
        if isinstance(clf, sagemaker.sklearn.estimator.SKLearn):
            artifact = sm_boto3.describe_training_job(TrainingJobName=clf.latest_training_job.name)
        elif type(clf) == str:
            artifact = sm_boto3.describe_training_job(TrainingJobName=clf)
        model_bucket = artifact['OutputDataConfig']['S3OutputPath'].rsplit('//')[-1][:-1]
        if artifact_type == 'Output':
            output_file = os.path.join(artifact['TrainingJobName'], 'output/output.tar.gz')
            local_output_dir =  artifact['TrainingJobName'] + '/output/'
        elif artifact_type == 'Model':
            output_file = artifact['ModelArtifacts']['S3ModelArtifacts']
            output_file = output_file.rsplit('/')
            output_file = '/'.join(output_file[3:])
            local_output_dir =  artifact['TrainingJobName'] + '/model/'
        elif artifact_type == 'Source':
            output_file = artifact['HyperParameters']['sagemaker_submit_directory']
            output_file = output_file.rsplit('/')
            output_file = '/'.join(output_file[3:])
            output_file = output_file[:-1]
            local_output_dir =  artifact['TrainingJobName'] + '/source/'
        try:
            boto3.Session().resource('s3').Bucket(model_bucket).download_file(output_file, os.path.basename(output_file))
            shutil.unpack_archive(os.path.basename(output_file), local_output_dir)
            self.logger.info(artifact_type + ' files saved in ' + local_output_dir)
            return local_output_dir
        except botocore.exceptions.ClientError as e:
            self.logger.error(artifact_type + ' files could not be downloaded')
            return -1

    
    def deploy_to_kyma(self, clf, profile_name, initial_instance_count=1, endpoint_name=None, cleanup_resources=True):
        try:
            sm_boto3 = boto3.client('sagemaker')
            if isinstance(clf, sagemaker.sklearn.estimator.SKLearn):
                job_name =  clf.latest_training_job.name
            elif type(clf) == str:
                job_name=clf
            result = re.search(r'(-[0-9]{2,4})+', job_name)
            parsed_job_name = job_name[:result.start()]
            if endpoint_name == None:
                folder_name = parsed_job_name + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            else:
                folder_name = endpoint_name + '-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            if isinstance(re.fullmatch(r'(?:[a-z0-9]+(?:[._-][a-z0-9]+)*/)*[a-z0-9]+(?:[._-][a-z0-9]+)*', folder_name), type(None)):
                raise Exception('Your training job name cannot be used as an endpoint name. Please pass an endpoint_name to the function to resolve this issue.')

            self.logger.info(' Creating container files...')

            #create all folders first
            self._create_folder(folder_name)
            self.logger.info('....\t '+folder_name+' folder created')

            self._create_folder(folder_name+'/SKLearn')
            self.logger.info('....\t SKLearn folder created')

            self._create_folder(folder_name+'/ml')
            self.logger.info('....\t ml folder created')

            #create files next
            #get ml folder set up
            self.logger.info('....\t\t Downloading the model from S3...')
            local_model_dir = self._download_artifacts(artifact_type='Model', clf=clf)
            if local_model_dir == -1:
                raise Exception("ERROR: Couldn't download model artifact from S3")
            self.logger.info('....\t\t Copying model to ml/model')
            shutil.copytree(local_model_dir, folder_name+'/ml/model/')

            self.logger.info('....\t\t Downloading the source from S3...')
            local_source_dir = self._download_artifacts(artifact_type='Source', clf=clf)
            if local_source_dir == -1:
                raise Exception("ERROR: Couldn't download source artifact from S3")
            self.logger.info('....\t\t Copying source to SKLearn/source/')
            shutil.copytree(local_source_dir, folder_name+ '/SKLearn/source/')

            # implement pip as a subprocess to get requirement.txt of training script for predictor.py
            self.logger.info(' checking if user has a requirements.txt...')
            has_requirements=False
            if os.path.exists(os.path.join(local_source_dir, "requirements.txt")) == True:
                self.logger.info(' user has a requirements.txt.')
                has_requirements=True
            self.logger.info(' user does not have a requirements.txt.')
                        
            #then get sklearn folder set up
            sg = ScriptGenerator()

            sg.write_nginx(folder_name+'/SKLearn/nginx.conf')
            self.logger.info('....\t\t nginx.conf created')

            sg.write_serve(folder_name+'/SKLearn/serve')
            self.logger.info('....\t\t serve created')

            sg.write_wsgi(folder_name+'/SKLearn/wsgi.py')
            self.logger.info('....\t\t wsgi.py created')
            artifact = sm_boto3.describe_training_job(TrainingJobName=job_name)
            entry_point = artifact['HyperParameters']['sagemaker_program'].replace('"', '')
            sg.write_flaskapp(folder_name+'/SKLearn/flaskapp.py', entry_point)
            
            self.logger.info('....\t\t flaskapp.py created')
            
            # changed for packaging
            # # need to look into how it will be copied when predictor is packaged into the library
            # self.logger.info('....\t\t Copying predictor to /SKLearn/predictor.py')
            # shutil.copy('predictor.py', folder_name+'/SKLearn/')

            #finally get the container folder set up 
            self.logger.info('....\t Copying kubeconfig.yml')
            try:
                shutil.copy('kubeconfig.yml', folder_name)
            except FileNotFoundError as e:
                raise FileNotFoundError("Ensure you have downloaded the kubeconfig.yml from the Kyma Console UI. This is found in the user menu.")

            stream = open(folder_name+'/kubeconfig.yml', 'r')
            data = yaml.load(stream,  yaml.BaseLoader)
            items = data.get('clusters')
            host_name = items[0]['name']

            training_image = artifact['AlgorithmSpecification']['TrainingImage']
            sg.write_dockerfile(folder_name+'/Dockerfile', training_image, has_requirements)
            self.logger.info('....\t Dockerfile created')

            account_id = boto3.client('sts').get_caller_identity().get('Account')
            container_image = account_id +'.dkr.ecr.'+self.region+'.amazonaws.com/'+folder_name+':latest'
            sg.write_deployment(folder_name+'/deployment.yaml', folder_name, initial_instance_count, container_image, profile_name)
            self.logger.info('....\t deployment.yaml created')

            # changed for packaging
            # # need to look into how it will be copied when build_and_push.sh is packaged into the library
            # self.logger.info('....\t Copying build_and_push.sh')
            # shutil.copy('build_and_push.sh', folder_name)
            # self.logger.info('....\t build_and_push.sh copied')
            
            link = '.amazonaws.com'
            if self.region == 'cn-north-1' or self.region == 'cn-northwest-1':
                link = '.amazonaws.com.cn'
            account_id=re.split('.dkr', training_image)[0]
            full_link=account_id+'.dkr.ecr.'+self.region+link

            #deleting downloaded folder that contains the model and source
            self._delete_folder(local_model_dir)
            self._delete_folder(local_source_dir)
            parent_path = os.path.join(local_source_dir, os.pardir)
            os_parent_path = os.path.abspath(parent_path)
            if len(os.listdir(os_parent_path)) ==0:
                self._delete_folder(os_parent_path)

            # changed for packaging
            self.logger.info('Installing kubectl...')
            # st = os.stat('./install_kubectl.sh')
            # os.chmod('./install_kubectl.sh', st.st_mode | stat.S_IEXEC)
            # process = subprocess.Popen(['./install_kubectl.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            kubectl_install = resource_filename(__name__,'install_kubectl.sh')
            process = subprocess.Popen(['sh', kubectl_install], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            com = process.communicate()
            self.logger.info(com[0])
            self.logger.info(com[1])
            
            # TODO : Comment out for PIP INSTALL
            # self._create_folder(folder_name+'/pack')
            # self.logger.info('....\t pack folder created')
            # self.logger.info('....\t Copying package')
            # shutil.copy('fedml_aws-2.0.0-py3-none-any.whl', folder_name+'/pack')
            # self.logger.info('....\t fedml_aws-2.0.0-py3-none-any.whl copied')
            
            self.logger.info('Building, pushing, and deploying container and creating endpoint....')
            for path in self._run_build_and_push_script(image=folder_name, full_link=full_link, profile_name=profile_name):
                self.logger.info(path)

            
            endpoint = 'https://'+folder_name+'.'+host_name
            self.logger.info('Your endpoint is '+endpoint)
            self.logger.info("\tTo ping: "+endpoint+'/ping')
            self.logger.info("\tTo invoke: "+endpoint+'/invocations')

            self.logger.info('Deleting folder...')
            self._delete_folder(folder_name)
            self.logger.info('Done.')

            if cleanup_resources == True:
                self._cleanup_resources()
        except Exception as e:
            self._delete_folder(folder_name)
            self.logger.info(e)
            raise

    def _run_build_and_push_script(self, image, full_link, profile_name):
        # changed for packaging
        # st = os.stat(image+'/build_and_push.sh')
        # os.chmod(image+'/build_and_push.sh', st.st_mode | stat.S_IEXEC)
        try:
            args = [image, full_link, profile_name]
            # changed for packaging
            #process = subprocess.Popen([image+'/build_and_push.sh']+ args, stdout=subprocess.PIPE, shell=False)
            build_and_push_script = resource_filename(__name__,'build_and_push.sh')
            process = subprocess.Popen(['sh', build_and_push_script]+ args, stdout=subprocess.PIPE, shell=False)
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
            self._delete_folder(image)
            raise

    def _create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                raise FileExistsError('Folder already exists')
        except FileExistsError as e:
            self.logger.info("File Exists Error: %s", e)
        except Exception as e:
            self.logger.info(e)
            raise
            
    def _delete_folder(self, path):
        if os.path.exists(path):
            os.system("rm -rf "+path)
            
    def invoke_kyma_endpoint(self, api, content_type, payload_path=None, payload=None, accept='application/json'):
        try:
            if payload_path is not None:
                payload = open(payload_path)
                print(type(payload))
            else:
                if payload is None:
                    raise Exception('You must provide a path to your payload, or the payload itself.')
            headers = {'Content-Type': content_type, 'Accept':accept}
            r = requests.post(api, data=payload, headers=headers)
            return r
        except Exception as e:
            self.logger.info(e)
            raise
        
    
        
    
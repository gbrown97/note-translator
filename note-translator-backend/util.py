import boto3
import botocore
import io
import logging
from botocore.exceptions import ClientError 
class S3Storage:

  def __init__(self, userName) -> None:
    #read access key and secret access key from a json file.
    self.s3 = boto3.resource('s3',aws_access_key_id='AKIAUN7YZP4UUMN4EPUN', aws_secret_access_key='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', region_name= "us-east-2")
    self.bucketName = 'note-translator-data'
    self.bucket = self.s3.Bucket(self.bucketName)
    self.s3Client = boto3.client('s3', aws_access_key_id='AKIAUN7YZP4UUMN4EPUN', aws_secret_access_key='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', region_name= "us-east-2")
    self.user = userName
    result = self.s3Client.list_objects_v2(Bucket=self.bucketName, Prefix= userName +'/')
    if 'Contents' in result:
      print("Key exists in the bucket.")
    else:
      print("Key doesn't exist in the bucket.")
      folder_name = self.s3Client.put_object(Bucket=self.bucketName, Key= userName+'/')

  # LIST S3 FILES.   
  def listFiles(self):
    try :
      prefix_objs = self.bucket.objects.filter(Prefix=self.user)
      s3_files=[obj.key for obj in prefix_objs.all()]
      return s3_files
    except Exception as e:
      print(e)

  # LOAD TEXT FILE FROM S3.
  def loadTxt(self,fileKey):
    filename = str(fileKey).split('/')[-1]
    key = self.user + '/' + fileKey
    response = self.bucket.Object(key = key).get()
    status = response.get('ResponseMetadata',{}).get('HTTPStatusCode')
    if status == 200:
      print(f"Text File Loaded Successfully - {status}")
      txtData = response.get("Body")
      return txtData,filename
    else:
      print(f"Text File Not Loaded - {status}")

  # UPLOAD TEXT FILE TO S3.
  def uploadTxt(self,textData, fileKey):
    key = self.user + '/' + fileKey
    object = self.s3.Object(self.bucketName, key)
    result = object.put(Body=textData)
    status = result.get('ResponseMetadata',{}).get('HTTPStatusCode')
    if status == 200:
      print(f"Text File Uploaded Successfully - {status}")
    else:
      print(f"Text File Not Uploaded - {status}")

  # DELETE A FILE FROM S3.     
  def deleteFile(self,key):
    key = self.user + "/" + key
    self.s3.Object(self.bucketName, key).delete()

  # RENAME FILE IN S3.
  def renameFile(self,oldKey,newKey):
    oldKey = self.user + '/' + oldKey
    newKey = self.user + '/' + newKey
    self.s3.Object(self.bucketName,newKey).copy_from(CopySource=self.bucketName +"/"+ oldKey)
    self.s3.Object(self.bucketName,oldKey).delete()
  
  # DOWNLOAD FILE FROM S3 TO LOCAL.
  def downloadFile(self,key,filename):
    self.s3Client.download_file(self.bucketName, key, filename)
  
  # Generate a presigned URL to share an S3 object  -preview
  def create_presigned_url(self,key):
    """Generate a presigned URL to share an S3 object

    :param object_name/key: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    key = self.user + '/' + key
    try:
      url = self.s3Client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params={'Bucket': self.bucketName,
                'Key': key },
        ExpiresIn=3600,

      )
    except ClientError as e:
      print(e)
      return None
    
    return url
  

  def create_presigned_post(self,object_name,fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    try:
        response = self.s3Client.generate_presigned_post(self.bucketName,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response
  
  def create_presigned_url_expanded(self,client_method_name, method_parameters=None,
                                  expiration=3600, http_method=None):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    
    try:
        response = self.s3Client.generate_presigned_url(ClientMethod=client_method_name,
                                                    Params=method_parameters,
                                                    ExpiresIn=expiration,
                                                    HttpMethod=http_method)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
  
   
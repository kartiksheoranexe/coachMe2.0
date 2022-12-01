import boto3
import pandas
import botocore
from botocore.exceptions import ClientError


client = boto3.client(
    's3',
    aws_access_key_id = 'AKIA2BX3HUAUQF2E5N5L',
    aws_secret_access_key = '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',
    region_name = 'ap-southeast-1'
)

resource = boto3.resource(
    's3',
    aws_access_key_id = 'AKIA2BX3HUAUQF2E5N5L',
    aws_secret_access_key = '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',
    region_name = 'ap-southeast-1'
)

Bucket='coachme-demo-1'
resource.Bucket(Bucket).upload_file("Rushabhonboard.xlsx", "clientfile")

location = {'LocationConstraint': 'ap-southeast-1'}
client.create_bucket(
    Bucket='coachme-demo-2',
    CreateBucketConfiguration=location
)


clientResponse = client.list_buckets()
print(clientResponse)
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')

  
    my_bucket = resource.Bucket(bucket["Name"])

    for file in my_bucket.objects.all():
        print(file.key)



try:
    obj = client.get_object(Bucket='coachme-demo-1',Key='Clientonboard.csv')
    data = pandas.read_csv(obj['Body'])
    print('Printing the data frame...')
    print(data)
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidObjectState':
        print(e.response['Error'])




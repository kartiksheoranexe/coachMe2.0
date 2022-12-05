import boto3
import pandas
import botocore
from botocore.exceptions import ClientError
from boto3.session import Session


ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
region = 'ap-southeast-1'


client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=region
)

resource = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=region
)

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
while True:
    print("Printing Options....")
    print("Press 1 - To get list of Bucket and its components")
    print("Press 2 - To create a new bucket")
    print("Press 3 - To upload a file to a bucket")
    print("Press 4 - To download a file from a bucket")
    print("Print 5 - To read a file from bucket")
    user_input = int(input())

    if user_input == 1:
        clientResponse = client.list_buckets()
        print('Printing bucket names...')
        for bucket in clientResponse['Buckets']:
            print(f'Bucket Name: {bucket["Name"]}')
            my_bucket = resource.Bucket(bucket["Name"])
            for file in my_bucket.objects.all():
                print(file.key)
            continue
    elif user_input == 2:
        print("Enter the name of the bucket you want to create : ")
        new_bucket_name = input()
        location = {'LocationConstraint': 'ap-southeast-1'}
        client.create_bucket(
            Bucket=new_bucket_name,
            CreateBucketConfiguration=location
        )
        continue
    elif user_input == 3:
        print("Enter the bucket name where you want to upload your file : ")
        bucket_name = input()
        print("Enter file : ")
        file = input()
        print("Enter name you want to save your file with : ")
        file_name = input()
        resource.Bucket(bucket_name).upload_file(file, file_name)
        continue
    elif user_input == 4:
        print("Enter the bucket name from where you want to download your file : ")
        bucket_name = input()
        bucket_obj = resource.Bucket(bucket_name)
        print("List of files : ")
        for f in bucket_obj.objects.all():
            print(f.key)
        print("Enter file : ")
        file = input()
        session.resource('s3').Bucket(bucket_name).download_file(
            file, f'D:\s3filedownloads\{file}')
        continue
    elif user_input == 5:
        print("Enter the name of the bucket you want to access : ")
        bucket_name = input()
        print("Enter the name of the file you want to access : ")
        file_name = input()
        try:
            obj = client.get_object(Bucket=bucket_name, Key=file_name)
            data = pandas.read_csv(obj['Body'])
            print('Printing the data frame...')
            print(data)
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidObjectState':
                print(e.response['Error'])
        continue
    else:
        print("Wrong input!!")
        continue

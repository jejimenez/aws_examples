from argparse import ArgumentParser
import props
import boto3


# The calls to AWS STS AssumeRole must be signed with the access key ID
# and secret access key of an existing IAM user or by using existing temporary 
# credentials such as those from antoher role. (You cannot call AssumeRole 
# with the access key for the root account.) The credentials can be in 
# environment variables or in a configuration file and will be discovered 
# automatically by the boto3.client() function. For more information, see the 
# Python SDK documentation: 
# http://boto3.readthedocs.io/en/latest/reference/services/sts.html#client


def get_client():
    # create an STS client object that represents a live connection to the 
    # STS service
    sts_client = boto3.client('sts')
    
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    # RoleARN is in IAM console ->  Roles -> {Role Name} -> Summary [Role ARN]
    
    assumedRoleObject = sts_client.assume_role(
        RoleArn=props.rolearn,#"RoleArn="arn:aws:iam::{Account_id}:role/{rolename}",
        RoleSessionName="AssumeRoleSession1"
    )
    
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']
    
    # Use the temporary credentials that AssumeRole returns to make a 
    # connection to Amazon S3  
    client = boto3.client(
        'rekognition',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
    )
    return client

def get_args():
    parser = ArgumentParser(description='Call index faces')
    parser.add_argument('-i', '--image')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.image is None:
        args.image = '/Users/jaimeenrrique/Documents/workspace/py_aws_boto_sts1/DSC_0238_37.jpg'
    client = get_client()
    with open(args.image, 'rb') as image:
        #response = client.index_faces(Image={'Bytes': image.read()}, CollectionId=args.collection)
        response   = client.detect_labels(Image={'Bytes':image.read()})
        print response
    print "help"

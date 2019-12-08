import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json

dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
audio_table = dynamodb.Table('audio_identifiers')
text_table = dynamodb.Table('text_version_audio')
mapping_table = dynamodb.Table('mapping')

#rpId = rasberrypi id {1,2,3,4} for now
def putId(id, rpId, lst, fileName):
    fileNameStr = str(fileName)
    jsonObj = json.dumps(lst)
    audio_table.put_item(
        Item={
            'audioId': id,
            'rpId' : rpId,
            'questionsArray' : jsonObj,
            'fileName' : fileNameStr,
        }
    )

def getId(id):
    res = None
    try:
        response = audio_table.scan(
            FilterExpression = Attr('audioId').eq(id)
            )
        res = response['Items'][0]
    except ClientError as e:
        print(e.response['Error']['Message'])
    return res

#for collections by fixed variables {1,2,3,4}
def getIdByRp(id):
    res = []
    try:
        response = audio_table.scan(
            FilterExpression = Attr('rpId').eq(id)
            )
        for i in response['Items']:
            res.append((i['audioId'], json.loads(i['questionsArray']), i['fileName'], i['rpId']))
    except ClientError as e:
        print(e.response['Error']['Message'])
    return res

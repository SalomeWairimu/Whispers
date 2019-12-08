import boto3

# s3 = boto3.resource('s3')

s3 = boto3.resource(
    's3')

def test():
    for bucket in s3.buckets.all():
        print(bucket.name)

b = s3.Bucket('firstbucketluke')
#b.upload_file("1.JPG", "file")

def uploadFileToAws(file, fileNameinS3):
    #s3.Object('firstbucketluke', file).put(Body='body', Metadata={'typeOfAudio': 'filler'})
    s3.meta.client.upload_file(file, 'firstbucketluke', fileNameinS3)

def getAudioFileByKey(key, filePath = "/home/pi/Documents/WhisperDemo/audios/"):
    b.download_file(key, filePath + 'answer.wav')

"""
for key in b.objects.all():
    k = key.load()
    print(key.e_tag)
    print(type(k))
"""

#for obj in b.objects.all():
 #   print(obj.key)

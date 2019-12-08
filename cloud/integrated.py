import cloud.main as buckets
import cloud.dynamo as db
import json

b = buckets.b

#for obj in b.objects.all():
#    print(obj.key)
#db.putId('asdf', '1', 'sample speech to text')

#a = db.getIdByRp(1)

def postToCloud(file, id, rpId, lst, fileNameinS3):
    # file = .wav
    # id = unique ID from server
    # rpId = which rasberrypi {1,2,3,4} for now
    # txt = the speech to text
    print("Uploading to cloud")
    buckets.uploadFileToAws(file, fileNameinS3)
    db.putId(id,rpId,lst,fileNameinS3)
    return

def retrieveByRasberryPiId(id):
    lst = db.getIdByRp(id)
    audio_ids = []
    audio_qsts = []
    for audio in lst:
        for i in range(len(audio[1])):
            audio_ids.append(audio[0])
            audio_qsts.append(audio[1][i])
        
    return audio_ids, audio_qsts

def retrieveAudioFileByAudioId(id):
    f = db.getId(id)['fileName']
    return f
def downloadFile(fileName):
    buckets.getAudioFileByKey(fileName)

# SAMPLE method use
#listOfQuestions = ["question1", "question2"]
#postToCloud('sample.wav', '125122', '123', listOfQuestions , "fileNameInS3.wav")

#res = retrieveByRasberryPiId('123')
#print(res[0][0]) --> audioId
#print(res[0][1]) --> type(list)
#print(res[0][1][0]) --> first question from array
#print(res[1][0]) --> next audioId .. and so on

#downloadFile("fileNameInS3.wav")
#or
#downloadFile("fileNameInS3.wav", "../../audios/randomfolder") to specify path for file download
#downloadFile("newTest.wav")

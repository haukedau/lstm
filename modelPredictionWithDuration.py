#Diese Datei kümmert sich um die Generierung
#neuer Noten und die Erstellung der Midi-Datei
#aus den generierten Noten


import numpy as numpy
import requestTests
import os

from keras.models import load_model

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def makePrediction(model,model_duration,actualTrain):
    print(str(actualTrain.ndim))
    if(actualTrain.ndim == 1):
        actualTrain = numpy.array([actualTrain])
    print(str(actualTrain.ndim))
    result = numpy.empty([1, 129])
    for x in range(0,500):
        if x > 0:
            actualTrain = actualTrain[1:actualTrain.shape[0]]
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult = numpy.append(partResult[0], duration)
            partResult = newresult
            #print("partResult" + str(partResult.shape))
            actualTrain = numpy.append(actualTrain, [partResult],axis=0)
            result = numpy.append(result,[partResult],axis=0)
        else:
            partResult = (model.predict(numpy.array([actualTrain]), batch_size=32))
            #print(partResult)
            duration = model_duration.predict(numpy.array([actualTrain]), batch_size=32)
            newresult= numpy.append(partResult[0], duration)
            partResult=newresult
            #print("partResult" + str(partResult.shape))
            actualTrain =  numpy.append(actualTrain,[partResult],axis=0)
            #print("actualTrain" + str(actualTrain.shape))
            result[0] = partResult[0]

    print("finsied saves now")
    i = 0
    for element in result:
        j = 0
        maxProb = 0
        maxElement = -1
        for prob in element:
            resultBin = 0
            if (prob > maxProb and j < 128):
                    print(str(prob))
                    maxElement = j
                    maxProb = prob
            if (j < 128):
                result[i][j] = resultBin
            j = j + 1

        if(maxElement > 0):
            result[i][maxElement] = 1
        i = i + 1
    numpy.savetxt("./log/output2.txt",result,fmt='%.3f')

    return requestTests.covertArrayToJSON(result.tolist())

def getFolderContent():
    newArray = os.listdir("./models/")
    newDictionary ={}
    for folder in newArray:
        newDictionary[""+folder] =  os.listdir("./models/"+str(folder))
    return newDictionary

#http://127.0.0.1:5000/getPrediction?folder=bachOneChannel&channel=73
@app.route('/getPrediction')
def getPrediction():
    folder = request.args.get('folder')
    channel = request.args.get('channel')
    model = load_model('./models/' +str(folder)+'/'+ str(channel) + '_noteModel.h5')
    model_duration = load_model('./models/' +str(folder)+'/'+ str(channel) + '_durationsModel.h5')
    print("got request")
    starttrain = numpy.loadtxt('./models/' +str(folder)+'/'+  str(channel) + "_x2Train.txt")
    midiFileName = makePrediction(model,model_duration,starttrain)
    return "<a href='http://localhost/"+midiFileName+".mid' >"+midiFileName+"</a>"

#127.0.0.1:5000/getModels
@app.route('/getModels')
def getModels():
    print("got getModels request")
    return jsonify(getFolderContent())


if __name__ == '__main__':
    app.run()

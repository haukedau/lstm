# -*- coding: utf-8 -*-
import numpy as numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop

import json
import midiConverter

inputArray = midiConverter.getMidiFromFile("midi_songs_bach/fp-1all.mid")
inputArray = numpy.append(inputArray, midiConverter.getMidiFromFile("midi_songs_bach/fp-2cou.mid"),axis=0)
inputArray = numpy.append(inputArray, midiConverter.getMidiFromFile("midi_songs_bach/fp-3sar.mid"),axis=0)
inputArray = numpy.append(inputArray, midiConverter.getMidiFromFile("midi_songs_bach/fp-4bou.mid"),axis=0)

print("inputArrayComple:" + str(inputArray.shape))
sequence_length = 100
#print all
startAsString = midiConverter.convertToMidiTrack(inputArray)
numpy.savetxt("inputArray.txt",inputArray,fmt='%i')
uploadResult = midiConverter.getMidiFromText(startAsString,"inputArray")

print("ARRAY"+str(inputArray.shape))

def shapeData(sequence_length):
    input_data = []
    output_data = []

    for i in range(0, (inputArray.shape[0] - sequence_length), 1):
        input_sequence = inputArray[i:i + sequence_length]
        output_sequence = inputArray[i + sequence_length]
        input_data.append(input_sequence)
        output_data.append(output_sequence)

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)

    return (input_data, output_data)

data,target = shapeData(sequence_length)
print("DATA"+str(data.shape))
print("TARGET"+str(target.shape))

print("inputArray",inputArray.shape)
print("target shape " +str(target.shape))
print(target)


print(data.shape)
model = Sequential()
model.add(LSTM(88, return_sequences=True, input_shape=(sequence_length,88)))
model.add(LSTM(128))
model.add(Dense(88, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

x_train = data
y_train = numpy.asarray(target)
print("x_train"+str(x_train.shape))
print("y_train"+str(y_train.shape))

numpy.savetxt("xTrain.txt",x_train[0])
<<<<<<< HEAD
model.fit(x_train, y_train, batch_size=32, epochs=50)
=======
model.fit(x_train, y_train, batch_size=32, epochs=100)
>>>>>>> aa7bff312fb5692f81cbcda1315b07e6083e9663
score = model.evaluate(x_train, y_train, batch_size=32)

model.save('my_modelDoubleLstm.h5')
###########
# IMPORTS #
###########
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import MaxPooling2D
import math
import numpy

################
# PREPARATIONS #
################
# fix random seed for reproducibility
numpy.random.seed(7)
# load data set and test set (they have to have same dimensions)
dataset = numpy.loadtxt("IsingValues.txt", delimiter=",")
testset = numpy.loadtxt("IsingTest.txt", delimiter=",")
# note shape of indata
size_y = dataset.shape[0]
size_x = dataset.shape[1]
border = size_x - 2
# split into input (X) and output (Y) variables
X = dataset[:,0:border]
Y = dataset[:,border:size_x]
# do the same for test data
Xt = testset[:,0:border]
Yt = testset[:,border:size_x]
# convert input to matrices
length = int(math.sqrt(size_x))
X_i = numpy.empty([size_y, length, length, 1])
X_it = numpy.empty([size_y, length, length, 1])
for i in range(size_y):
	for j in range(length):
		X_it[i,j,:,0] = Xt[i,j*length:(j+1)*length]
		X_i[i,j,:,0] = X[i,j*length:(j+1)*length]

#########
# MODEL #
#########
# Define model
model = Sequential()
model.add(Conv2D(length,kernel_size=[2,2],input_shape=[length,length,1],strides=[2,2],padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))
model.add(Flatten())
model.add(Dense(2,activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

###################
# BACKPROPAGATION #
###################
# Fit the model
model.fit(X_i, Y, epochs=500, batch_size=10)

##############
# EVALUATION #
##############
# evaluate test data
scores = model.evaluate(X_it, Yt)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

###########
# PREDICT #
###########
# calculate predictions
predictions = model.predict(X_it)
# check accuracy
diff = numpy.rint(predictions) - Yt
res = numpy.empty([size_y, 1], dtype='str')
for i in range(size_y):
    res[i] = 'i'
    if diff[i,0] == 0 and diff[i,1] == 0:
        res[i] = 'c'
# print predictions
print(numpy.concatenate([predictions, Yt, res],axis=1))

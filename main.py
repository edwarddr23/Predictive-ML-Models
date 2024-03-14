import sys

from pyspark.sql.types import DoubleType
from pyspark.mllib.regression import LabeledPoint

from pyspark import SparkContext, SparkConf
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.linalg import Vectors
from sklearn.preprocessing import LabelEncoder

def convert(input):
    if input == "M":
        input = 1
    elif input == "B":
        input = 0
    else:
        input = float(input)
    return float(input)

def parsePoint(line):
	values = [convert(x) for x in line.split(",")]
    # The first value is the result value and the second value is the features that are factors that result in the result value.
	return LabeledPoint (values[1], values[2:32])
	
sc = SparkContext("local", "pyspark MLrandomforest")
data = sc.textFile ("input/input.txt")

parsedData = data.map(parsePoint)
model = RandomForest.trainClassifier(parsedData, 2, {}, numTrees = 5, impurity = 'gini', maxDepth = 5, maxBins = 32)

testData = ([20.6,29.33,140.1,1265,0.1178,0.277,0.3514,0.152,0.2397,0.07016,0.726,1.595,5.772,86.22,0.006522,0.06158,0.07117,0.01664,0.02324,0.006185,25.74,39.42,184.6,1821,0.165,0.8681,0.9387,0.265,0.4087,0.124])
prediction = model.predict(testData)
f = open("OUTPUT", "w+")
f.write("PREDICTION:" + str(prediction) + "\n")
f.close()
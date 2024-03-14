import sys

from pyspark.sql.types import DoubleType
from pyspark.mllib.regression import LabeledPoint

from pyspark import SparkContext, SparkConf
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.linalg import Vectors
from sklearn.preprocessing import LabelEncoder

def convert(input):
    if input == "Y":
        input = 1
    elif input == "N":
        input = 0
    elif input == "BS":
        input = 2
    elif input == "PhD":
        input = 3
    elif input == "MS":
        input = 4
    else:
        input = float(input)
    return float(input)

def parsePoint(line):
	values = [convert(x) for x in line.split(",")]
	return LabeledPoint (values[6], values[0:5])
	
sc = SparkContext("local", "pyspark MLrandomforest")
data = sc.textFile ("input/input.txt")
header = data.first()
data = data.filter(lambda line: line != header)

parsedData = data.map(parsePoint)
model = RandomForest.trainClassifier(parsedData,
                                     2,
                                     {},
                                     numTrees = 5,
                                     impurity = 'gini',
                                     maxDepth = 5,
                                     maxBins = 7)

testData = ([0,convert('N'),0,convert('PhD'),convert('Y'),convert('N')])
prediction = model.predict(testData)
f = open("OUTPUT", "w+")
f.write("PREDICTION:" + str(prediction) + "\n")
f.close()
import pandas as pd
import os
import shutil
import random

class data2pkl :

    DEFAULT_OUTPUT_FILE_PATH = "mydata/"

    def __init__(self, datasetFilePath, outputFileName, outputFileRootPath=DEFAULT_OUTPUT_FILE_PATH):
        self.datasetFilePath = datasetFilePath
        self.checkExists()
        self.outputFileRootPath = outputFileRootPath
        self.outputFileName = self.outputFileRootPath + outputFileName
        self.data = []

    def checkOrCreate(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def checkExists(self):
        if not os.path.exists(self.datasetFilePath):
            raise FileNotFoundError

    def generate(self, questionCount, cloneCount):
        self.checkOrCreate(self.outputFileRootPath)
        index = 0
        datasetQuestionAmount = len([dirname for dirname in os.listdir(self.datasetFilePath)])
        if questionCount > datasetQuestionAmount:
            questionCount = datasetQuestionAmount
        neededDatas = random.sample(range(1, datasetQuestionAmount + 1), questionCount)
        for questionIndex in neededDatas:
            path = self.datasetFilePath + os.sep + str(questionIndex)
            allFile = os.listdir(path)
            random.shuffle(allFile)
            picked = allFile[0:cloneCount]
            for cloneIndex in picked:
                file = path + os.sep + str(cloneIndex)
                print(file)
                with open(file, encoding="utf8") as f:
                    sourceCode = "".join(f.readlines())
                    currentData = [index, sourceCode, questionIndex]
                    self.data.append(currentData)
                    index+=1

        dataframe = pd.DataFrame(self.data)
        dataframe.to_pickle(self.outputFileName)

def analizeSampleData(file):
    source = pd.read_pickle(file)
    arr = dict()
    for i in range(0, len(source)):
        if arr.get(source.iloc[i][2]) :
            arr[source.iloc[i][2]]  = arr[source.iloc[i][2]] + 1
        else :
            arr[source.iloc[i][2]] = 1
    print(arr)

def filterUtf8(rootPath, targetPath):
    allDir = os.listdir(rootPath)
    for dir in allDir:
        path = rootPath + os.sep + dir
        allFile = os.listdir(path)
        for file in allFile:
            filePath = path + os.sep + file
            with open(filePath, encoding="utf8") as f:
                try:
                    f.readlines()
                except UnicodeDecodeError:
                    f.close()
                    print("file is not utf8: " + filePath)
                    targetDir = targetPath + os.sep + dir
                    if not os.path.exists(targetDir):
                        os.mkdir(targetDir)
                    targetFile = targetDir + os.sep + file
                    shutil.move(filePath, targetFile)

def test():
    try:
        with open("D://ABS/ProgramData/34/2616.txt") as f:
            print(f.readlines())
    except UnicodeDecodeError:
        print("error")
        os.mkdir("D://ABS/notUTF8/34")
        shutil.move("D://ABS/ProgramData/34/2616.txt", "D://ABS/notUTF8/34/2616.txt")

if __name__ == "__main__" :
    # test()

    filterUtf8("D://ABS/ProgramData", "d://ABS/notUTF8")
    d2p = data2pkl("D://ABS/ProgramData", "programs.pkl")
    d2p.generate(104, 50)


    # source = pd.read_pickle( 'mydata/programs.pkl')
    # print(source.iloc[0][1])

    # analizeSampleData('clone/data/c/programs.pkl')
    # analizeSampleData('clone/data/c/oj_clone_ids.pkl')
    # source = pd.read_pickle( 'clone/data/c/oj_clone_ids.pkl')
    # print(source)

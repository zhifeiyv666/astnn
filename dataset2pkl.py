import pandas as pd
import os
import shutil
import random

class data2pkl :

    DEFAULT_OUTPUT_FILE_PATH = "mydata/"

    def __init__(self, datasetFilePath, outputFileName = "programs.pkl", outputClonePairFileName = "clone_ids.pkl", outputFileRootPath=DEFAULT_OUTPUT_FILE_PATH):
        self.datasetFilePath = datasetFilePath
        self.checkExists()
        self.outputFileRootPath = outputFileRootPath
        self.outputFileName = self.outputFileRootPath + outputFileName
        self.outputClonePairFileName = self.outputFileRootPath + outputClonePairFileName
        self.data = []

    def checkOrCreate(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def checkExists(self):
        if not os.path.exists(self.datasetFilePath):
            raise FileNotFoundError

    def generate(self, questionCount, eachQuestionCount):
        print("======  start generate programs =====")
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
            picked = allFile[0:eachQuestionCount]
            for cloneIndex in picked:
                file = path + os.sep + str(cloneIndex)
                with open(file, encoding="utf8") as f:
                    sourceCode = "".join(f.readlines())
                    currentData = [index, sourceCode, questionIndex]
                    self.data.append(currentData)
                    index+=1

        dataframe = pd.DataFrame(self.data)
        dataframe.to_pickle(self.outputFileName)

        # generate  clone pairs:
        print("======  start generate clone pairs =====")
        print("data length is : ", len(self.data))
        clone_pairs = []
        for i in range(50000):
            id1 = random.randint(0, len(self.data) - 1)
            id2 = random.randint(0, len(self.data) - 1)
            label = 0
            print("id1: ",id1, "   id2: ", id2)
            if self.data[id1][2] == self.data[id2][2]:
                label = 1
            clone_pairs.append([id1, id2, label])
        clone_pairs_dataframe = pd.DataFrame(clone_pairs , columns=["id1", "id2", "label"])
        dataframe.to_pickle(self.outputClonePairFileName)


def analizeSampleData(file):
    source = pd.read_pickle(file)
    print(source)
    print("============")
    arr = lst = [0 for i in range(105)]
    for i in range(0, len(source)):
        arr[source.iloc[i][2]] = arr[source.iloc[i][2]] + 1
    for i in range(len(arr)):
        print(i, " : ", arr[i])

def analizeCloneIds(file):
    source = pd.read_pickle(file)
    print(source)
    arr = dict()
    id1 = []
    id2 = []
    msg = [[0, 1000000000000000] for i in range(2)]
    for i in range(0, len(source)):
        if arr.get(source.iloc[i][2]):
            arr[source.iloc[i][2]] = arr[source.iloc[i][2]] + 1
        else:
            arr[source.iloc[i][2]] = 1

        cur = source.iloc[i]
        for j in range(2):
            if cur[j] > msg[j][0]:
                msg[j][0] = cur[j]
            if cur[j] < msg[j][1]:
                msg[j][1] = cur[j]
        if cur[2] == 1:
            id1.append(cur[0])
            id2.append(cur[1])
    print("id1 max: ", msg[0][0], "   id1 min: ", msg[0][1])
    print("id2 max: ", msg[1][0], "   id2 min: ", msg[1][1])
    print("=======")
    print("id1: ", id1)
    print("id2: ", id2)
    print("=======")
    # print(arr)

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

def analize():
    # source = pd.read_pickle( 'mydata/programs.pkl')
    # print(source.iloc[0][1])

    print("========== programs  ==============")
    analizeSampleData('clone/data/c/programs.pkl')
    print("========== clone ids  ==============")
    analizeCloneIds('clone/data/c/oj_clone_ids.pkl')
    source = pd.read_pickle( 'clone/data/c/oj_clone_ids.pkl')
    print(source)


if __name__ == "__main__" :
    # test()
    # analize()

    filterUtf8("D://ABS/ProgramData", "d://ABS/notUTF8")
    d2p = data2pkl("D://ABS/ProgramData","50.pkl","50_clone.pkl")
    d2p.generate(104, 50)



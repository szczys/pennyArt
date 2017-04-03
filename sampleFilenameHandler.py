import glob

SAMPLEBASENAME = 'sampleSet/{number}-penny.png'

def getFileNumIdx(samplebasename=SAMPLEBASENAME):
    premask = samplebasename.format(number="######")
    fileNumIdx = len(premask.split("######")[0])
    return fileNumIdx

def getNextSampleFilename(samplebasename=SAMPLEBASENAME):
    #This will be called once and will find the highest
    #existing sample number and increment it by 1.
    #It will work even if there are some samples missing
    query = glob.glob(samplebasename.format(number="*"))
    if query == []:
        return samplebasename.format(number="000001")
    else:
        fileNumIdx = getFileNumIdx()
        highest = 0
        for fn in query:
            testVal = int(fn[fileNumIdx:fileNumIdx+6])
            if  testVal > highest:
                highest = testVal
        return makeSampleFilename(highest+1)

def makeSampleFilename(num, samplebasename=SAMPLEBASENAME):
    nextNum = str(num)
    nextNum = '0'*(6-len(nextNum)) + nextNum
    return samplebasename.format(number=nextNum)

def incrementFilename(curFn):
    fileNumIdx = getFileNumIdx()
    highest = int(curFn[fileNumIdx:fileNumIdx+6])+1
    return makeSampleFilename(highest)

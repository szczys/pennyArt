import pennyArt

penValues = pennyArt.unPicklePennies()

mosaicVals = pennyArt.unPickleHelper('circlesAndLum.p')
#print penValues.keys()

#get the nearest value in a list or set of dict keys
#print min(penValues, key=lambda x:abs(x-51))
#print min(penValues, key=lambda x:abs(x-99))


def map256(vals):
    """ Map dictionary key values to a 0-255 range.

    Your input dictionary will have a smaller range than 0-256. For instance
    you may have 49-91. The return dictionary will contain keys 0, 255 and some
    values in between. The point is to normalize the span of the input acrouss
    and 8-bit value range.

    Attributes:
    *  vals - a dictionary with intergers between 0-255 as keys

    Returns:
    *  dictionary with keys between 0-255 whose values are the keys from the input dictionary
    """

    bottomOffset = min(vals.keys())
    steps = 255.0/(max(vals.keys())-bottomOffset)

    returnDict = {}
    for k in vals.keys():
        returnKey = int((k-bottomOffset) * steps)
        returnDict[returnKey] = k
    return returnDict


def placePennies(penDict,pixelList,maxError):
    """Place pennies in the image matching best as possible

    Attributes:
    * penDict like dict(luminosity:[pennyFilename1,pennyFilename2])
    * pixelList like list((x,y),luminosity)
    * maxError is how far from target luminosity is allowed. Error starts at 0
        and increases as matching gets harder until maxError is met. Setting
        maxError to zero enables infinite error.

    Returns:
    * list like list((x,y),pennyFilename,errorMargin)
    * leftover pixelList like list((x,y),luminosity)

    """
    #get dicts we can remove pennies and pixels from
    pennyTriage = dict(penDict)
    mosaicDict = {}
    for m in pixelList:
        mosaicDict.setdefault(m[1],[]).append(m[0])
    print mosaicDict

    #get value spans (do this before removing from these dicts)
    pennySpread = map256(pennyTriage)
    imgSpread = map256(mosaicDict)

    print len(pennySpread)
    print len(imgSpread)

    #TODO: Implement way to generate ideal penny list (or need)

    #Flow:
    ## Start with penny set
    ## set error margin
    cantMatchFlag = False
    errorMargin = 0
    matchedPennyList = []
    ## Begin loop;
    while(cantMatchFlag == False):
        ### iterate all pennies recording matches and removing from set
        for pMap in pennySpread.keys():
            closestPixMap = min(imgSpread.keys(), key=lambda x:abs(x-pMap))
            print pMap,closestPixMap
            ### record pixelLocation, pennySampleFn, error margin
        ### increment the error margin
        errorMargin += 1
        cantMatchFlag = True
        ### break if no pennies left
        ### break if image pixels have all been filled
        ### break if error margin too great
        ### goto loop
    ## return recorded set and set of pixelLocations still remaining
    return matchedPennyList,

placePennies(penValues, mosaicVals, 0)

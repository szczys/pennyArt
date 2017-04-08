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

def popTriagePenny(pMap, pennySpread, triagePennies):
    """Return penny information and remove it from the two input lists"""
    mapIndex = pennySpread[pMap]
    #getPenny filename & remove penny from list
    pennyFn = triagePennies[mapIndex].pop()
    #remove this liminostiy value from both lists as necessary
    if len(triagePennies[mapIndex]) == 0:
        triagePennies.pop(mapIndex,None)
        pennySpread.pop(mapIndex,None)
        print "Pennies Left:",len(triagePennies.keys())
    #return penny filename
    return pennyFn

def popTriagePixel(closestPixMap, imageSpread, pixelList):
    """Return pixel information and remove it from the two input lists"""
    #get pixel coordinates
    #remove pixel from list
    #remove this liminostiy value from both lists as necessary
    #return pixle coordinates
    return "Needs implemenation"

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

            if (abs(pMap-closestPixMap) <= errorMargin) or maxError == 0:
                ### make sure we didn't already pull all these pennies
                if pMap in pennySpread.keys():
                    ### get penny info and remove it from the set
                    thisPenny = popTriagePenny(pMap, pennySpread, pennyTriage)
                    ### get pixel info and remvoe it from the set
                    thisPixel = popTriagePixel(closestPixMap, imgSpread, pixelList)
                    ### record pixelLocation, pennySampleFn, error margin
                    matchedPennyList.append([thisPixel, thisPenny, errorMargin])
        ### increment the error margin
        errorMargin += 1

        ### break if no pennies left
        ### break if image pixels have all been filled
        ### break if error margin too great
        if len(pennyTriage) == 0 or \
            len(pixelList) == 0 or \
            errorMargin > 255 or \
            (maxError > 0 and errorMargin > maxError):
            cantMatchFlag = True
        ### goto loop
    ## return recorded set and set of pixelLocations still remaining
    return matchedPennyList,pixelList

penData,leftoverPix = placePennies(penValues, mosaicVals, 1)
print
print len(penData)
print penData
print
print len(leftoverPix)

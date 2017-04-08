import pennyArt

penValues = pennyArt.unPicklePennies()

mosaicVals = pennyArt.unPicklePaintByNumber()
for i in mosaicVals:
    print i
#print penValues.keys()

#get the nearest value in a list or set of dict keys
print min(penValues, key=lambda x:abs(x-51))
print min(penValues, key=lambda x:abs(x-99))


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

#Let's place pennies in the image as best we can:
def placePennies():
    pennySpread = map256(penValues)
    imgSpread = map256(mosaicVals)

    #TODO: Implement way to generate ideal penny list (or need)

    #Flow:
    ## Start with penny set
    ## set error margin
    ## Begin loop;
    ### iterate all pennies recording matches and removing from set
    ### record pixelLocation, pennySampleFn, error margin
    ### increment the error margin
    ### break if no pennies left
    ### break if image pixels have all been filled
    ### break if error margin too great
    ### goto loop
    ## return recorded set and set of pixelLocations still remaining

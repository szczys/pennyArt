import pennyArt

penValues = pennyArt.unPickleHelper('pennySet.p')

mosaicVals = pennyArt.unPickleHelper('paintByNumber.p')
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

test = [penValues,{92:0, 49:0}, {255:0,0:0}, {2:0, 129:0}]
print sorted(map256(penValues).keys())
for i in test:
    print i
    print map256(i)

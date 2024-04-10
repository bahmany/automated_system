
def convertFormMessage(errors):
    res = []
    for field in list(errors.keys()):
        for f in errors[field]:
            res.append({"fieldName": field, "message": f})
    return res


def convertFormMessageToJson(errors):
    res = {}
    for field in list(errors.keys()):
        for f in errors[field]:
            res.append({"fieldName": field, "message": f})
    return res



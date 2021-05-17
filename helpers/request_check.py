def checkGet(request):
    return request.method == 'GET'

def checkPost(request):
    return request.method == 'POST'    

def checkPut(request):
    return request.method == 'PUT'


def checkUpdate(request):
    return request.method == 'UPDATE'
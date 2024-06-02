# 全局上下文
import jsonpickle

def getSessionInfo(request):
    suser = request.session.get('user','')
    if suser:
        return {'user':jsonpickle.loads(suser)}

    return {'user':''}



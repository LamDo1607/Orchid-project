from rest_framework.decorators import api_view
import datetime
from dateutil.parser import parse
from api.models import Log, User
from api.apps import *
from mongoengine.queryset.visitor import Q
from api.views.loginsession import *
from api.auth import *
import os
from lib.TGMT.TGMTpaging import Paging

####################################################################################################

def WriteLog(activity, exception):
    try:
        log = Log(
            activity=activity,
            exception=exception,
            timeCreate = utcnow()
        )
        log.save()
        return True    
    except Exception as e:
        return False

####################################################################################################

@api_view(["POST"])           
def GetLogList(request):
    try:
        _token = request.POST.get("token")
        jwt = decode(_token)

        RequireLevel(jwt, ["Root", "Admin"])

        _fromDateStr = RequireParamExist(request, "fromDate")
        _toDateStr = RequireParamExist(request, "toDate")

        _fromDate = parse(_fromDateStr) + datetime.timedelta(hours=-7)
        _toDate = parse(_toDateStr) + datetime.timedelta(days=1) + datetime.timedelta(hours=-7)

        logs = Log.objects(timeCreate__gte=_fromDate, timeCreate__lt=_toDate, isDeleted=False)

        _search_string = GetParam(request, "search_string")

        _order_by = request.POST.get('order_by')
        if(_order_by != None and _order_by == "desc"):
            logs = logs.order_by("-timeCreate")
            
        if(_search_string != None and _search_string != ""):
            logs = logs(exception__icontains=_search_string) 

        respond = Paging(request, logs)

        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

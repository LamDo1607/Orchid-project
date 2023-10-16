from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import History, LoginSession
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from lib.TGMT.TGMTpaging import Paging

####################################################################################################

@api_view(["POST"])
def GetHistoryList(request):
    try:
        _token = request.POST.get('token')
        loginSession = api.auth.decode(_token)

        _user_id = request.POST.get('user_id') 
        _userID = request.POST.get('userID')
        _order_by = request.POST.get('order_by')

        _fromDateStr =  RequireParamExist(request, "fromDate", "từ ngày")
        _toDateStr = RequireParamExist(request, "toDate", "đến ngày")

        _fromDate = parse(_fromDateStr) + datetime.timedelta(hours=-7)
        _toDate = parse(_toDateStr) +  datetime.timedelta(days=1) + datetime.timedelta(hours=-7)

        histories = History.objects(timeCreate__gte=_fromDate, timeCreate__lt=_toDate, isDeleted=False)

        if(_order_by != None and _order_by in ["timeCreate", "-timeCreate"]):
            histories = histories.order_by(_order_by)

        respond = Paging(request, histories)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))

from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import User, LoginSession, Orchid
from api.views.log import WriteLog
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging

####################################################################################################

@api_view(["POST"])
def GetOrchidList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)       
            

        _name = GetParam(request, 'name')
        _scienceName = GetParam(request, 'scienceName')
        _author = GetParam(request, 'author')
        _address = GetParam(request, 'address')
        _note = GetParam(request, 'note')
        _dateCreate = GetParam(request, 'dateCreate')
        
        orchidTable = Orchid.objects(isDeleted=False)     

        respond = Paging(request, orchidTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateOrchid(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _name = RequireParamExist(request, 'name')
        _scienceName = GetParam(request, 'scienceName')
        _address = GetParam(request, 'address')
        _note = GetParam(request, 'note')

        orchid = None
        if(IsPk(_pk)):
            try:
                orchid = Orchid.objects.get(pk=_pk, isDeleted=False)
            except Orchid.DoesNotExist:      
                pass

        if(orchid == None):
            orchid = Orchid(
                author = jwt["email"],
                dateCreate = utcnow(),
                )
        orchid.name = _name
        orchid.scienceName = _scienceName
        orchid.address = _address
        orchid.note = _note
        orchid.save()
        return SuccessResponse("cập nhật thành công")
    except Exception as e:
        WriteLog("UpdateOrchid", str(e))
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteOrchid(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')


        orchid = Orchid.objects.get(pk=_pk, isDeleted=False)
        orchid.isDeleted = True 
        orchid.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
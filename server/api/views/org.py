from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import hashlib
import datetime
import api.auth
from api.models import Org, User, LoginSession
from api.apps import *
from api.views.loginsession import *
from api.views.activity import AddActivity
from lib.TGMT.TGMTpaging import Paging
from unidecode import unidecode
from mongoengine.queryset.visitor import Q

####################################################################################################

@api_view(["POST"])           
def UpdateOrg(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)
        
        RequireLevel(loginSession, ["Root", "Admin"])

        _name = RequireParamExist(request, "name", "tên tổ chức")    
        _address = GetParam(request, "address") 
        _manager = RequireParamExist(request, "manager", "tên người đại diện")
        _position = GetParam(request, "position") 
        _phone1 = GetParam(request, "phone1") #group user
        _phone2 = GetParam(request, "phone2") #presenter
        _pk = GetParam(request, "pk") 
    
        isExist = False
        org = None
        if(IsPk(_pk)):
            try:
                org = Org.objects.get(pk=_pk, isDeleted=False)
                org.timeUpdate = utcnow()
                isExist = True
            except Org.DoesNotExist:
                pass
            

        if(org == None):
            org = Org(name =_name, timeCreate = utcnow())

        if(_name != None and _name != ""):
            _name_ascii = unidecode(_name)
            org.name = _name
            org.name_ascii = _name_ascii

        if(_address != None and _address != ""):
            org.address = _address

        if(_manager != None and _manager != ""):
            _manager_ascii = unidecode(_manager)
            org.manager = _manager
            org.manager_ascii = _manager_ascii

        if(_position != None and _position != ""):
            org.position = _position

        if(_phone1 != None and _phone1 != ""):
            org.phone1 = _phone1

        if(_phone2 != None and _phone2 != ""):
            org.phone2 = _phone2
            
        org.save()

        if(isExist):
            usersInOrg = User.objects(org_pk=str(org.pk), isDeleted=False)
            for user in usersInOrg:
                user.orgName = org.name
                user.save()
                
            AddActivity(loginSession["email"], "Cập nhật tổ chức", org.name)
            return SuccessResponse("Câp nhật tổ chức thành công")
        else:
            AddActivity(loginSession["email"], "Thêm tổ chức", org.name)
            return SuccessResponse("Thêm tổ chức thành công")
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])           
def GetOrgs(request):
    try:
        _token = GetParam(request, "token")
        loginSession = FindLoginSession(_token) 
        
        

        orgList = Org.objects(isDeleted=False)
        
        _search_string = GetParam(request, 'search_string')
        if(_search_string != None and _search_string != ""):
            _search_string_ascii = unidecode(_search_string)
            orgList = orgList.filter(Q(name__icontains=_search_string) |
                                    Q(name_ascii__icontains=_search_string_ascii) |
                                    Q(manager__icontains=_search_string) |
                                    Q(manager_ascii__icontains=_search_string_ascii))

        respond = Paging(request, orgList)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse("Có lỗi: "+ str(e))       

####################################################################################################

@api_view(["POST"])           
def GetOrg(request):
    try:        
        _token = GetParam(request, "token")

        loginSession = FindLoginSession(_token)
        _name = GetParam(request, "org_id")
        if(_name == None or _name == ""):
            _org_id = loginSession['org_id']

        org = Org.objects.get(orgID=_org_id, isDeleted=False)  
        return JsonResponse(org.to_json())
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])           
def RemoveOrg(request):
    try:
        _token = GetParam(request, "token")
        loginSession = FindLoginSession(_token)

        _pk = RequireParamExist(request, "pk") #  

    
        org = Org.objects.get(pk=_pk)
        
        org.isDeleted =  True
        org.timeUpdate = utcnow()
        org.save()

        AddActivity(loginSession["email"], "Xóa tổ chức", org.name)
        return SuccessResponse("Xóa tổ chức thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

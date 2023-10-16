from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import Org, User, LoginSession
from api.views.log import WriteLog
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from lib.TGMT.TGMTemail import SendEmailAsync

####################################################################################################

@api_view(["POST"])
def login(request):
    _email = request.POST.get('email').lower()
    _password = request.POST.get('password')

    hashed_password = HashPassword(_password)

    try:
        _user = User.objects.get(email=_email, isDeleted=False)
        if(not settings.DEBUG and _user.password != hashed_password):
            return ErrorResponse("Không đúng email/password")
    except User.DoesNotExist:
        return ErrorResponse("Không đúng email/password")

    try:
        login_session = LoginSession(email = _email,
                                    fullname = _user.fullname,
                                    level = _user.level,                                    
                                    loginTime = utcnow()
                                    )
        login_session.save()
        payload = {
            'email': _email,
            'fullname' : _user.fullname,
            'level' : _user.level,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
            'loginSession_pk' : str(login_session.pk)
        }

        jwt_token = api.auth.encode(payload)
        _user.password = ""
        result = json.loads(_user.to_json())
        result["token"] = jwt_token['token']

        return ObjResponse(result)
    except Exception as e:
        return ErrorResponse('Có lỗi: ' + str(e))

####################################################################################################

@api_view(["POST"])
def logout(request):
    try:
        _user_id = request.POST.get('user_id')
        _user_id = _user_id.lower()
        _image = request.POST.get('image')
        _token = request.POST.get('token')
        loginSession = LoginSession.objects.get(token = _token)
   
        if(_image != ""):
            _save_folder = "logout"
            _file_name = _user_id + "_"
        else:
            _imagePath = ""
        loginSession.imageLogoutPath = _imagePath
        loginSession.logoutTime = datetime.datetime.utcnow()
        loginSession.save()

        return SuccessResponse('Logout thành công')

    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

def HashPassword(password):
    hash_routine = 5
    hashed_password = password
    while hash_routine != 0 :
       hashed_password = hashlib.sha224(hashed_password.encode('utf-8')).hexdigest()
       hash_routine = hash_routine - 1
    return hashed_password

####################################################################################################

@api_view(["POST"])
def GetUser(request):
    try:
        _token = request.POST.get('token')
        loginSession = api.auth.decode(_token)

        _email = request.POST.get('email')
        user = User.objects.get(email=_email, isDeleted=False)
        user.password = None

        return JsonResponse(user.to_json())
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])
def GetUserList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)       
            

        _level = GetParam(request, 'level')
        _search_string = GetParam(request, 'search_string')
        _status = GetParam(request, 'status')
        _org_pk = GetParam(request, 'org_pk')
        _order_by = GetParam(request, 'order_by')
        

        userTable = User.objects(email__ne="root", isDeleted=False).exclude("password")  

        if(_level != None and _level != ""):
            userTable = userTable(level=_level)

        if(_status != None and _status != "" and _status != "all"):
            userTable = userTable(status=_status)

        if(_search_string != None and _search_string != ""):
            userTable = userTable(email__icontains=_search_string)        

        if(IsPk(_org_pk)):
            userTable = userTable(org_pk=_org_pk)


        if(_order_by != None and _order_by == "desc"):
            userTable = userTable.order_by("-timeRegister")
       
        # printt(userTable.to_json())
        respond = Paging(request, userTable)

        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])
def ChangePassword(request):
    try:
        _token = request.POST.get("token")
        if(len(_token) == 24):
            loginSession = LoginSession.objects.get(pk=_token, isDeleted=False)
            if(loginSession.purpose != "ResetPassword"):
                return ErrorResponse("Link không hợp lệ")
        else:            
            loginSession = api.auth.decode(_token)
        
            _email = loginSession["email"]
            _password = request.POST.get('password')
            hashed_password = HashPassword(_password)
            _newPassword = request.POST.get('newPassword')

            user = User.objects.get(email=_email, isDeleted=False)

            if(user.password != hashed_password):
                return ErrorResponse("Password cũ không đúng")
        
        hashed_newpassword = HashPassword(_newPassword)
        user.password = hashed_newpassword
        user.save()

        
        return SuccessResponse("Đổi mật khẩu thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

@api_view(["POST"])
def ResetPassword(request):
    try:
        _username = request.POST.get('username')
        _password = _username
        try:
            user = User.objects.get(username=_username, isDeleted=False)
        except User.DoesNotExist:
            return Response(
                {'Error': "Không tìm thấy user: "+ _username},
                status=ERROR_CODE,
                content_type="application/json"
            )
        if user:
            hashed_newpassword = HashPassword(_password)
            user.password = hashed_newpassword
            user.isPasswordChanged = False
            user.save()
            return Response(
                {'Success': "Đổi mật khẩu thành công"},
                status=SUCCESS_CODE,
                content_type="application/json"
            )
    except Exception as e:
        return Response(
            {'Error': "Thông tin không đúng, lỗi: " + str(e)},
            status=ERROR_CODE,
            content_type="application/json"
            )


####################################################################################################

@api_view(["POST"])
def Register(request):
    try:
        _email = request.POST.get('email').lower()
        _name = request.POST.get('name')
        _position = request.POST.get('position')
        _password = request.POST.get('password')
        _phone = request.POST.get('phone')
        
        user = None
        try:
            user =  User.objects.get(email=_email, isDeleted=False)
            already_existed = True
        except User.MultipleObjectsReturned:
            already_existed = True
        except User.DoesNotExist:
            already_existed = False
        
        hashed_password = HashPassword(_password)
        
        if(user == None):
            user = User(email = _email)
        else:
            if(user.status != "Invited"):
                return ErrorResponse("Email này đã được đăng ký")

        user.fullname = _name
        user.password = hashed_password
        user.phone = _phone        
    
       
        user.timeUpdate = datetime.datetime.utcnow()

        user.save()

        #create login session
        login_session = LoginSession(email = _email,
                                    fullname = user.fullname,
                                    level = user.level,
                                    purpose = "ConfirmEmail",
                                    loginTime = datetime.datetime.utcnow(),
                                    validTo = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                                    )
        login_session.save()

        SendEmailAsync("Xác nhận đăng ký orchid account",
                    "<!DOCTYPE html>" +
                    "<html><head></head><body>" +
                    "<p>Xin chào bạn</p>" +		
                    "<p>Bạn nhận được email vì đã đăng ký sử dụng dịch vụ tại " + settings.HOST + ". </br>" + 
                    "Nếu đúng là bạn thì click vào link bên dưới để xác nhận email, nếu không phải bạn xin vui lòng bỏ qua email này.</p> </br>" +
                    "<p>" + settings.HOST + "/redirect?token=" + str(login_session.pk) + "</p>" +
                    "<p>Đây là email tự động, vui lòng không reply.</p>" +
                    "</body></html>",
                    _email
                )

        return SuccessResponse("Đăng ký thành công, vui lòng kiểm tra email để xác nhận")
    except Exception as e:
        WriteLog("Register", str(e))
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateUser(request):
    try:
        _token = GetParam(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _email = RequireParamExist(request, 'email')
        _phone = GetParam(request, 'phone')
        _fullname = GetParam(request, 'fullname')
        _org_pk = GetParam(request, 'org_pk')

        user = User.objects.get(pk=_pk, isDeleted=False)

        if(IsPk(_org_pk)):
            org = Org.objects.get(pk=_org_pk, isDeleted=False)
            user.orgName = org.name
            user.org_pk = _org_pk
            

        user.email = _email
        user.phone = _phone
        user.fullname = _fullname
        user.save()
        return SuccessResponse("cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

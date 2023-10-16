# we need to include new view here
from .user import login, logout, GetUser, ChangePassword, ResetPassword, Register, GetUserList, UpdateUser
from .loginsession import GetLoginSession, verifyToken, Redirect
from .webcam import StopWebcam
from .opencv import DetectFace
from .bever import DetectBeverage
from .history import GetHistoryList
from .orchid import UpdateOrchid, GetOrchidList, DeleteOrchid
from .location import GetLocationList, UpdateLocation, DeleteLocation
from .org import  GetOrgs, RemoveOrg,UpdateOrg
from .activity import  GetActivityList, AddActivity
from .fileupload import JoditUpload
from .log import GetLogList
from .species import  UpdateSpecies,GetSpecies,RemoveSpecies

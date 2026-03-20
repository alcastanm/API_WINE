import requests
from google.auth.transport import requests as google_requests
from fastapi import APIRouter, Depends
from CORE.SECURITY.auth_dependency import get_current_user
from CORE.SERVICES.authorizationService import authorizationService
from CORE.interfaces_services.IauthorizationService import IauthorizationService
from ENTITIES.domine.UsersModel import UsersModel
from src.ENTITIES.dto.googleParam import googleParam
from src.CONTROLLER.RESPONSES.customResponse import customResponse
from google.oauth2 import id_token
from datetime import datetime, timezone
from CORE.SECURITY.jwt_handler import create_access_token
from src.CORE.SECURITY.security_config import GOOGLE_CLIENT_ID, MICROSOFT_CLIENT_ID
from jose import jwt

authRoute = APIRouter()

JWKS_URL = "https://login.microsoftonline.com/common/discovery/v2.0/keys"

@authRoute.post("/auth/social-login")
async def auth(data:googleParam,
               authorization_service:IauthorizationService=Depends(authorizationService)):
    currentDate = datetime.now(timezone.utc)
    D_Name  = ''
    D_Email = ''
    try:
        if data.provider == "google":        
            idinfo = id_token.verify_oauth2_token(
                            data.token,
                            google_requests.Request(),
                            GOOGLE_CLIENT_ID
                        )        
        
            # se arma el objeto de usuario para ir a guardarlo si no existe
            user = UsersModel(  id = 0,
                                email =idinfo["email"],
                                name =  idinfo["name"],
                                picture = idinfo["picture"],
                                provider = data.provider,
                                created_at = currentDate
                                )
            res = await authorization_service.saveUser(user)
            D_Name  = res.name
            D_Email = res.email 
            D_picture = idinfo["picture"]          

            # se genera token de la app wine
            access_token = create_access_token({
                "user_id": res.id,
                "email": res.email
            })
            
        if data.provider=='microsoft':
            # obtener claves públicas de Microsoft
            jwks = requests.get(JWKS_URL).json() 
            
            # obtener header del token
            unverified_header = jwt.get_unverified_header(data.token) 
            
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }

            if not rsa_key:
                raise Exception("Unable to find appropriate key")
            
            claims  = jwt.get_unverified_claims(data.token)
            issuer = claims["iss"]
            payload = jwt.decode(
                data.token,
                rsa_key,
                algorithms=["RS256"],
                audience=MICROSOFT_CLIENT_ID,
                issuer=issuer
            )
            
            
            # se arma el objeto de usuario para ir a guardarlo si no existe
            user = UsersModel(  id = 0,
                                email =payload.get("preferred_username"),
                                name =  payload.get("name"),
                                picture = '',
                                provider = data.provider,
                                created_at = currentDate
                                )
            res = await authorization_service.saveUser(user)            
            
            
            D_Name  = payload.get("name"),
            D_Email = payload.get("preferred_username")
            D_picture = ""
            
            access_token_microsoft = create_access_token({
                "user_id": res.id,
                "email": D_Email
            })                
                                                       

        returnedObj = { "access_token":access_token_microsoft if data.provider=='microsoft' else access_token ,
                        "user":{
                                "email":D_Email ,
                                "name": D_Name,
                                "picture":D_picture                                
                                }
                        }           
        
        return customResponse(data=returnedObj,isSuccess=True,returnedMessage="Well done")
 
    except Exception as e:
      return customResponse(data=None,isSuccess=False,returnedMessage="There is an Error!!!!")
    



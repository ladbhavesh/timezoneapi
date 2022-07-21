from fastapi import Request
from fastapi.responses import JSONResponse
import base64

from config import getConfig

class AuthMiddleware:
  
    def __init__(self, bypassroutes):
        self.bypassroutes = bypassroutes

    def _isAuth(self, request: Request):
        authheader = request.headers.get("Authorization")

        if authheader == None:
            return False
        
        startsWithBasic = authheader.startswith("Basic ")

        if startsWithBasic == False:
            return False

        authDetails = authheader.split(' ')


        decodedString = base64.b64decode(authDetails[1]).decode('utf-8')

        creds = decodedString.split(':')

        if creds[0] == getConfig('api_secretuser') and creds[1] == getConfig('api_secretpassword'):
            return True

        return False

        

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        #content_type = request.headers.get('Content-Type')
        #print(content_type)

        if request.url.path in self.bypassroutes:
            response = await call_next(request)
            return response
        else:
            if self._isAuth(request) == False:
                content = {"error": "unauthorized"}
                return JSONResponse(content=content, status_code=401)
            else:
                response = await call_next(request)
                return response                

        
        # process the request and get the response    
        # response = await call_next(request)
        
        # return response
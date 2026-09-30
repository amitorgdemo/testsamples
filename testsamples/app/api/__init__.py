import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.vnet_api import router as vnet_router
from app.api.auth_api import router as auth_router
from app.core.security import verify_access_token


def create_app() -> FastAPI:
    app = FastAPI(
        title="Azure Infra Provision Service", 
        version="1.0.0",
        # This re-enables the Authorize padlock globally in Swagger UI for your middleware!
        swagger_ui_parameters={"persistAuthorization": True}
    )
    
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(vnet_router, prefix="/api/v1")
    
    @app.middleware("http")
    async def global_auth_middleware(request: Request, call_next):
        public_endpoints = [
            "/docs",
            "/openapi.json",
            "/api/v1/auth/token"
        ]
        
        if request.url.path in public_endpoints:
            return await call_next(request)
            
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or improperly formatted Bearer token parameter."}
            )
            
        try:
            token_string = auth_header.split(" ")[1]
            user_context = verify_access_token(token_string) # Pass exact string
        except IndexError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Bearer token string is malformed."}
            )
        
        if not user_context:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token validation failed or session has expired."}
            )
            
        # Attach context downstream
        request.state.user = user_context
        return await call_next(request)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time= time.perf_counter()
        response = await call_next(request)
        process_time= time.perf_counter()-start_time
        response.headers["X-Process-Time"] = str(time)

        return response
    
    return app

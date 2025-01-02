from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.session import get_db

# Import the token validation function from the token_validation module
from token_validation import verify_access_token

# Create a FastAPI app instance
app = FastAPI()

# Define the OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Define a custom middleware for token verification
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request : str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db) #"might need to be configure further" 
        #we can pass the requested token here or pass it when using the function, whichever is the best course
        try:
            # Call the verify_access_token to validate the token
            verify_access_token(request)
            # If token validation succeeds, continue to the next middleware or route handler          
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # If token validation fails due to HTTPException, return the error response
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            # If token validation fails due to other exceptions, return a generic error response
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

# Add the custom middleware to the FastAPI app
app.add_middleware(CustomMiddleware)
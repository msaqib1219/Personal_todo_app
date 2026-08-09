import jwt
from jwt import PyJWKClient, InvalidTokenError, ExpiredSignatureError
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config import config
import logging

logger = logging.getLogger(__name__)

jwks_client = PyJWKClient(config.JWKS_URL)
security = HTTPBearer(auto_error=False)

async def get_current_user_id(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if not credentials:
        logger.warning("Missing authorization header")
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA"],
            audience=None,
            options={"verify_aud": False},
        )
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            logger.warning("Token missing user_id/sub claim")
            raise HTTPException(status_code=401, detail="Not authenticated")

        request.state.user_id = user_id
        return user_id

    except ExpiredSignatureError:
        logger.warning("Expired JWT token")
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {e}")
        raise HTTPException(status_code=401, detail="Not authenticated")
    except Exception as e:
        logger.error(f"JWT verification failed: {e}")
        raise HTTPException(status_code=401, detail="Not authenticated")
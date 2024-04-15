from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Represents the response returned to the client upon attempting authentication. It includes the authentication status and, on success, an access token for the authenticated session.
    """

    success: bool
    access_token: Optional[str] = None
    error_message: Optional[str] = None


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates user credentials and provides access token.

    Args:
        email (str): The email of the user attempting to authenticate. This email will be used to identify the user record in the database.
        password (str): The plaintext password provided by the user. This will be securely hashed and compared against the stored hash in the database.

    Returns:
        AuthenticateUserResponse: Represents the response returned to the client upon attempting authentication. It includes the authentication status and, on success, an access token for the authenticated session.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None:
        return AuthenticateUserResponse(success=False, error_message="User not found.")
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        fake_token = "generated_access_token"
        return AuthenticateUserResponse(success=True, access_token=fake_token)
    else:
        return AuthenticateUserResponse(
            success=False, error_message="Invalid credentials."
        )

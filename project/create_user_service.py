from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    A model to convey the outcome of the create user operation, including the user ID for the newly created user if successful.
    """

    success: bool
    user_id: Optional[str] = None
    message: str


async def create_user(email: str, password: str) -> CreateUserResponse:
    """
    Endpoint to register a new user.

    Args:
    email (str): The email address for the new user. Must be unique across all users.
    password (str): The plaintext password for the new user. This will be hashed and salted before storage.

    Returns:
    CreateUserResponse: A model to convey the outcome of the create user operation, including the user ID for the newly created user if successful.

    Example:
        create_user('john@example.com', 'password123')
        > CreateUserResponse(success=True, user_id='ckl23j4...', message='User successfully created.')
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return CreateUserResponse(
            success=False, message="A user with this email already exists."
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    try:
        user = await prisma.models.User.prisma().create(
            data={"email": email, "password": hashed_password, "role": "User"}
        )
        return CreateUserResponse(
            success=True, user_id=user.id, message="User successfully created."
        )
    except Exception as e:
        return CreateUserResponse(
            success=False, message="An error occurred while creating the user."
        )

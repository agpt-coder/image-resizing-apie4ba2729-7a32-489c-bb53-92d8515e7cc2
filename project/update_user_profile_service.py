from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    This model provides feedback on the successful update of the user's profile.
    """

    success: bool
    message: str


async def update_user_profile(
    email: str,
    fullName: str,
    password: Optional[str] = None,
    phoneNumber: Optional[str] = None,
    bio: Optional[str] = None,
) -> UpdateUserProfileResponse:
    """
    Allows users to update their profile information

    Args:
        email (str): The user's new email, must be unique across the system.
        fullName (str): The full name of the user for profile display.
        password (Optional[str]): A new password for the user, if updating. Optional, as changing the password should not be mandatory on profile update.
        phoneNumber (Optional[str]): The user's phone number. Optional for users who wish to add this information.
        bio (Optional[str]): Short biography or description about the user. Optional and can be provided for user engagement.

    Returns:
        UpdateUserProfileResponse: This model provides feedback on the successful update of the user's profile.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"email": email})
        if user is None:
            return UpdateUserProfileResponse(
                success=False, message="User with given email does not exist."
            )
        update_data = {"fullName": fullName}
        if password is not None:
            update_data["password"] = password
        if phoneNumber is not None:
            update_data["phoneNumber"] = phoneNumber
        if bio is not None:
            update_data["bio"] = bio
        await prisma.models.User.prisma().update(
            where={"email": email}, data=update_data
        )
        return UpdateUserProfileResponse(
            success=True, message="User profile updated successfully."
        )
    except Exception as e:
        return UpdateUserProfileResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )

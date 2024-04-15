import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticate_user_service
import project.create_user_service
import project.resize_image_service
import project.update_user_profile_service
import project.upload_image_service
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Image Resizing API",
    lifespan=lifespan,
    description="The project involves developing a feature that accepts an image file and desired dimensions, then resizes the image to fit within those specifications, with the option to crop the image to maintain the aspect ratio or to add padding to fit the specified dimensions without cropping. Key preferences and requirements include: - The use of PNG format for its support of transparency and the ability to maintain high image quality after compression and resizing. - Desired dimensions are set at 1280x720 pixels, chosen for its balance between quality and file size, suitable for both online viewing and moderate-quality printing. - Keeping the original aspect ratio of the image is essential to avoid stretching or squashing, maintaining the visual fidelity of the original image. - When adjusting the aspect ratio, padding is preferred over cropping to ensure no part of the image is lost, maintaining the integrity of the visual content. The tech stack for this project includes Python as the programming language, FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM. This stack supports the development of high-performance, scalable applications, and ensures efficient database management and seamless deployment of web services.",
)


@app.put(
    "/users/profile/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    email: str,
    fullName: str,
    password: Optional[str],
    phoneNumber: Optional[str],
    bio: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Allows users to update their profile information
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            email, fullName, password, phoneNumber, bio
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/authenticate",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates user credentials and provides access token
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register", response_model=project.create_user_service.CreateUserResponse
)
async def api_post_create_user(
    email: str, password: str
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Endpoint to register a new user
    """
    try:
        res = await project.create_user_service.create_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/images/resize", response_model=project.resize_image_service.ResizeImageResponse
)
async def api_post_resize_image(
    userId: str,
    originalImageUrl: str,
    desiredWidth: int,
    desiredHeight: int,
    crop: bool,
    padding: bool,
    paddingColor: Optional[str],
) -> project.resize_image_service.ResizeImageResponse | Response:
    """
    Processes the image resizing request with user-defined specifications
    """
    try:
        res = await project.resize_image_service.resize_image(
            userId,
            originalImageUrl,
            desiredWidth,
            desiredHeight,
            crop,
            padding,
            paddingColor,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/images/upload", response_model=project.upload_image_service.UploadImageResponse
)
async def api_post_upload_image(
    image_file: UploadFile,
    desired_width: Optional[int],
    desired_height: Optional[int],
    maintain_aspect_ratio: Optional[bool],
    use_padding: Optional[bool],
    padding_color: Optional[str],
) -> project.upload_image_service.UploadImageResponse | Response:
    """
    Endpoint for image upload and initial processing
    """
    try:
        res = await project.upload_image_service.upload_image(
            image_file,
            desired_width,
            desired_height,
            maintain_aspect_ratio,
            use_padding,
            padding_color,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

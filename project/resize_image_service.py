import io
from typing import Optional

import httpx
import prisma
import prisma.models
from PIL import Image as PILImage
from PIL import ImageOps
from pydantic import BaseModel


class ResizeImageResponse(BaseModel):
    """
    Response model for an image resize operation, including original and resized image URLs.
    """

    originalImageUrl: str
    resizedImageUrl: str
    status: str


async def resize_image(
    userId: str,
    originalImageUrl: str,
    desiredWidth: int,
    desiredHeight: int,
    crop: bool,
    padding: bool,
    paddingColor: Optional[str],
) -> ResizeImageResponse:
    """
    Processes the image resizing request with user-defined specifications.

    Args:
        userId (str): The ID of the user submitting the image for resizing.
        originalImageUrl (str): URL pointing to the location of the image to be resized.
        desiredWidth (int): The desired width for the resized image.
        desiredHeight (int): The desired height for the resized image.
        crop (bool): Whether the image should be cropped to maintain aspect ratio.
        padding (bool): Whether the image should be padded to fit dimensions without cropping.
        paddingColor (Optional[str]): The color to use for padding if applicable.

    Returns:
        ResizeImageResponse: Response model for an image resize operation, including original and resized image URLs.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(originalImageUrl)
        image_bytes = io.BytesIO(response.content)
        image = PILImage.open(image_bytes)
        if crop:
            image = ImageOps.fit(image, (desiredWidth, desiredHeight), PILImage.LANCZOS)
        elif padding:
            image = ImageOps.pad(
                image, (desiredWidth, desiredHeight), color=paddingColor
            )
        else:
            image = image.resize((desiredWidth, desiredHeight), PILImage.LANCZOS)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        resized_image_url = "https://example.com/resized-image-url.png"
        await prisma.models.Image.prisma().create(
            data={
                "userId": userId,
                "originalUrl": originalImageUrl,
                "resizedUrl": resized_image_url,
                "desiredWidth": desiredWidth,
                "desiredHeight": desiredHeight,
                "crop": crop,
                "padding": padding,
                "paddingColor": paddingColor if paddingColor else "",
            }
        )
        return ResizeImageResponse(
            originalImageUrl=originalImageUrl,
            resizedImageUrl=resized_image_url,
            status="success",
        )

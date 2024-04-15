import io
import uuid
from typing import Optional

from fastapi import UploadFile
from PIL import Image as PILImage
from PIL import ImageOps
from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    """
    Response model for the image upload endpoint. Provides a reference ID for the uploaded image and initial processing status.
    """

    image_id: str
    status: str
    message: Optional[str] = None


async def upload_image(
    image_file: UploadFile,
    desired_width: Optional[int] = 1280,
    desired_height: Optional[int] = 720,
    maintain_aspect_ratio: Optional[bool] = True,
    use_padding: Optional[bool] = False,
    padding_color: Optional[str] = "#FFFFFF",
) -> UploadImageResponse:
    """
    Endpoint for image upload and initial processing

    Args:
        image_file (UploadFile): The binary file of the image being uploaded. Accepts various formats as it will be converted to PNG format during processing.
        desired_width (Optional[int]): Optional. The desired width for the image after resizing. Defaults to pre-specified dimensions if not provided.
        desired_height (Optional[int]): Optional. The desired height for the image after resizing. Defaults to pre-specified dimensions if not provided.
        maintain_aspect_ratio (Optional[bool]): Optional. A boolean indicating if the image should maintain its aspect ratio when resized. If true, the image may be padded or cropped depending on the additional parameters.
        use_padding (Optional[bool]): Optional. Indicates whether to use padding to maintain aspect ratio. Ignored if maintain_aspect_ratio is False or not provided. Defaults to False.
        padding_color (Optional[str]): Optional. Specifies the color for padding (in hex format, e.g., '#FFFFFF'). Ignored if use_padding is False or not provided.

    Returns:
        UploadImageResponse: Response model for the image upload endpoint. Provides a reference ID for the uploaded image and initial processing status.
    """
    contents = await image_file.read()
    try:
        with PILImage.open(io.BytesIO(contents)) as img:
            src_width, src_height = img.size
            new_width, new_height = (src_width, src_height)
            if maintain_aspect_ratio:
                ratio = (
                    min(desired_width / src_width, desired_height / src_height)
                    if desired_width and desired_height
                    else 1
                )
                new_width, new_height = (
                    int(src_width * ratio),
                    int(src_height * ratio),
                )
                img = img.resize(
                    (new_width, new_height), PILImage.ANTIALIAS
                )  # TODO(autogpt): "ANTIALIAS" is not a known member of module "PIL.Image". reportAttributeAccessIssue
                if (
                    use_padding
                    and desired_width is not None
                    and (desired_height is not None)
                    and (new_width < desired_width or new_height < desired_height)
                ):
                    horizontal_padding = (
                        (desired_width - new_width) // 2
                        if desired_width is not None
                        else 0
                    )
                    vertical_padding = (
                        (desired_height - new_height) // 2
                        if desired_height is not None
                        else 0
                    )
                    img = ImageOps.expand(
                        img,
                        border=(horizontal_padding, vertical_padding),
                        fill=padding_color,
                    )
            else:
                img = img.resize(
                    (desired_width, desired_height), PILImage.ANTIALIAS
                )  # TODO(autogpt): "ANTIALIAS" is not a known member of module "PIL.Image". reportAttributeAccessIssue
            output = io.BytesIO()
            img.save(output, format="PNG")
            output.seek(0)
            image_id = str(uuid.uuid4())
            temp_file_path = f"/tmp/{image_id}.png"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(output.getvalue())
            return UploadImageResponse(
                image_id=image_id,
                status="pending",
                message="Image uploaded successfully and processing started.",
            )
    except Exception as e:
        return UploadImageResponse(
            image_id="error",
            status="failed",
            message=f"Failed to process the image: {str(e)}",
        )

from google.cloud import storage

import io

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import HTTPException

from andelsbolig.advertisement.service import do_patch_advertisement
from andelsbolig.security.service import is_authenticated
from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.config.properties import RUNNING_TESTS, BUCKET_NAME, S3_URL
from andelsbolig.misc.logger import get_logger


router = APIRouter()
db = AdvertisementRepository()
logger = get_logger(__name__)


client = storage.Client()
bucket = client.get_bucket(BUCKET_NAME)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...), jwt=Depends(is_authenticated)):
    blob = bucket.blob(file.filename)

    if RUNNING_TESTS:
        # I manually uploaded car.png
        url = f"{S3_URL}/car.png"
        thumbnail_url = f"{S3_URL}/thumbnail_car.png"
        return_response = {"message": "File uploaded successfully", "original_url": url, "thumbnail_url": thumbnail_url}
    else:
        blob.upload_from_file(file.file, content_type=file.content_type)
        url = f"{S3_URL}/{file.filename}"

        # Create thumbnail
        file.file.seek(0)
        image = Image.open(file.file)
        image.thumbnail((500, 500))

        thumbnail_io = io.BytesIO()
        image.save(thumbnail_io, format=image.format)
        thumbnail_io.seek(0)

        # Upload thumbnail
        thumbnail_filename = f"thumbnail_{file.filename}"
        thumbnail_blob = bucket.blob(thumbnail_filename)
        thumbnail_blob.upload_from_file(thumbnail_io, content_type=file.content_type)
        thumbnail_url = f"{S3_URL}/{thumbnail_filename}"
        return_response = {"message": "File uploaded successfully", "original_url": url, "thumbnail_url": thumbnail_url}

    do_patch_advertisement({"url": url}, jwt)
    return return_response


@router.delete("/upload/{thumbnail_name}")
def delete_image(thumbnail_name: str, jwt=Depends(is_authenticated)):
    """
    Delete an image entry from the database and storage.

    Args:
        thumbnail_name (str): The name of the thumbnail to delete.

    Raises:
        HTTPException: If the image is not found in the database.
    """
    thumbnail_url = f"{S3_URL}/{thumbnail_name}"
    result = db.update(
        {"created_by": jwt.sub},
        {"$pull": {"images": {"thumbnail_url": thumbnail_url}}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Image not found")

from fastapi import UploadFile
import base64
import requests
import os
import io
import cloudinary
import cloudinary.uploader


class ImagesManagement():
    async def UploadImageCloudinary(picture: UploadFile,folder:str) -> str:
        
        cloudinary.config(
            cloud_name="dn2qs6ce4",
            api_key="341742669668615",
            api_secret="w1MYSQQpJIzyHO0AUhX9DbR7Hd4",
            secure=True
        )

        contents = await picture.read()
        
        filename_without_ext, ext = os.path.splitext(picture.filename)

        print(f"Tamaño archivo leído: {len(contents)} bytes")
        print(f"Nombre archivo: {picture.filename}")

        if len(contents) == 0:
            raise Exception("¡La imagen está vacía!")

        # public_id = f"Images/{folder}/{picture.filename}"
        public_id = f"Images/{folder}/{filename_without_ext}"

        result = cloudinary.uploader.upload(
            io.BytesIO(contents),
            public_id=public_id,
            resource_type="image",
            overwrite=True,
            unique_filename=False,
            invalidate=True
        )

        print(result)

        url = result["secure_url"]
        return url
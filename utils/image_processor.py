import asyncio
import io
from PIL import Image
import requests
import os
from typing import Optional, BinaryIO
import logging

logger = logging.getLogger(__name__)

async def process_image(image_url: str, max_size: tuple[int, int] = (256, 256)) -> Optional[BinaryIO]:
    """Downloads, resizes, and returns an image from a URL.

    Args:
        image_url: The URL of the image to download.
        max_size: The maximum dimensions (width, height) for the resized image.

    Returns:
        A BytesIO object containing the processed image, or None if an error occurred.
    """
    cache_dir = os.getenv("IMAGE_CACHE_DIR", "./images")
    os.makedirs(cache_dir, exist_ok=True)
    filename = os.path.join(cache_dir, os.path.basename(image_url))

    try:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return io.BytesIO(f.read())

        async with asyncio.timeout(10):
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

        image = Image.open(io.BytesIO(response.content))
        image.thumbnail(max_size)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)

        with open(filename, "wb") as f:
            f.write(image_bytes.getvalue())

        return image_bytes

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading image from {image_url}: {e}")
        return None
    except IOError as e:
        logger.error(f"Error processing image from {image_url}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error processing image from {image_url}: {e}")
        return None
import os
import uuid
from fastapi import UploadFile
import config
import requests
from urllib.parse import urlparse
import mimetypes
from PIL import Image
try:
    import magic
except ImportError:
    # Fallback if python-magic is not installed
    magic = None

from utils.gdrive import download_file as gdrive_download
from utils.temp_storage import temp_storage
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("utils.helpers")

def save_uploaded_image(image: UploadFile) -> tuple[bool, str]:
    """Save an uploaded image and return the path"""
    try:
        # Extract file extension
        file_extension = image.filename.split(".")[-1].lower()
        
        # Validate file extension
        if file_extension not in config.ALLOWED_IMAGE_EXTENSIONS:
            return False, f"Invalid image format. Supported formats: {', '.join(config.ALLOWED_IMAGE_EXTENSIONS)}"
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate a unique filename
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join("uploads", unique_filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(image.file.read())
            
        return True, file_path
    
    except Exception as e:
        return False, f"Error saving image: {str(e)}"

def save_downloaded_image(image_url: str) -> tuple[bool, str]:
    """Download and save an image from URL and return the path"""
    try:
        # Get the file extension from URL
        parsed_url = urlparse(image_url)
        path = parsed_url.path
        
        # Try to get extension from URL
        file_extension = os.path.splitext(path)[1].lower().strip('.')
        
        # If extension not in URL, try to get from content-type
        if not file_extension or file_extension not in config.ALLOWED_IMAGE_EXTENSIONS:
            response = requests.head(image_url)
            content_type = response.headers.get('Content-Type', '')
            file_extension = mimetypes.guess_extension(content_type)
            if file_extension:
                file_extension = file_extension.lower().strip('.')
        
        # Validate file extension
        if not file_extension or file_extension not in config.ALLOWED_IMAGE_EXTENSIONS:
            return False, f"Invalid image format. Supported formats: {', '.join(config.ALLOWED_IMAGE_EXTENSIONS)}"
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate a unique filename
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join("uploads", unique_filename)
        
        # Download and save the file
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return False, f"Failed to download image. Status code: {response.status_code}"
        
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            
        return True, file_path
    
    except Exception as e:
        return False, f"Error saving image: {str(e)}"

def detect_image_type(file_path: str) -> str:
    """
    Detect image type using multiple methods
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Image type as string (e.g., 'jpg', 'png') or None if not detected
    """
    # Try using PIL first
    try:
        with Image.open(file_path) as img:
            image_format = img.format
            if image_format:
                return image_format.lower()
    except Exception:
        logger.warning(f"PIL could not identify image format for: {file_path}")
    
    # Try using python-magic if available
    if magic:
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)
            if mime_type and mime_type.startswith('image/'):
                return mime_type.split('/')[1]
        except Exception:
            logger.warning(f"python-magic could not identify image format for: {file_path}")
    
    # Try using file extension as fallback
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')
    if file_extension in config.ALLOWED_IMAGE_EXTENSIONS:
        return file_extension
    
    # Could not identify the image type
    return None

def process_drive_image(drive_url: str) -> tuple[bool, str, str]:
    """
    Process an image from Google Drive
    
    Args:
        drive_url: Google Drive URL to the image
        
    Returns:
        Tuple of (success, temp_path, permanent_path_or_error)
    """
    try:
        logger.info(f"Processing Google Drive image: {drive_url}")
        
        # First download to temporary location
        success, temp_path = gdrive_download(drive_url)
        
        if not success:
            logger.error(f"Failed to download image from Google Drive: {temp_path}")
            return False, None, temp_path  # temp_path contains error message
        
        # Validate that it's actually an image
        image_type = detect_image_type(temp_path)
        
        # Check if it's an allowed image type
        if not image_type or image_type.lower() not in config.ALLOWED_IMAGE_EXTENSIONS:
            # Remove the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False, None, f"Invalid image format: {image_type or 'unknown'}"
        
        # Create a unique filename for permanent storage
        permanent_filename = f"{uuid.uuid4().hex}.{image_type.lower()}"
        permanent_path = os.path.join("uploads", permanent_filename)
        
        logger.info(f"Validated Google Drive image. Temporary path: {temp_path}")
        return True, temp_path, permanent_path
        
    except Exception as e:
        logger.error(f"Error processing Google Drive image: {str(e)}")
        return False, None, f"Error processing image: {str(e)}"

def process_submission_image(url: str, is_form_data: bool = False) -> dict:
    """
    Process an image from either a URL or uploaded file
    
    Args:
        url: URL to the image (can be Google Drive or other URLs)
        is_form_data: Whether the URL comes from a form upload
        
    Returns:
        Dictionary with image information
    """
    result = {
        "success": False,
        "local_path": None,
        "original_url": url,
        "message": ""
    }
    
    try:
        # Skip empty URLs
        if not url:
            result["message"] = "No image URL provided"
            return result
            
        # For Google Drive URLs, use the special processor
        if "drive.google.com" in url or "docs.google.com" in url:
            success, temp_path, perm_path = process_drive_image(url)
            if success:
                result["success"] = True
                result["local_path"] = temp_path
                result["permanent_path"] = perm_path
            else:
                result["message"] = perm_path  # Error message
        else:
            # For regular URLs, download directly
            success, local_path = save_downloaded_image(url)
            if success:
                result["success"] = True
                result["local_path"] = local_path
            else:
                result["message"] = local_path  # Error message
                
        return result
        
    except Exception as e:
        result["message"] = f"Error processing image: {str(e)}"
        return result

def approve_and_save_image(temp_path: str, permanent_path: str) -> bool:
    """
    Move a temporary image to permanent storage after approval
    
    Args:
        temp_path: Path to the temporary image
        permanent_path: Path where the image should be permanently stored
        
    Returns:
        True if successful, False otherwise
    """
    if not temp_path or not os.path.exists(temp_path):
        logger.error(f"Temporary image not found: {temp_path}")
        return False
    
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(os.path.dirname(permanent_path), exist_ok=True)
        
        # Move the file (can use our temp_storage utility)
        if temp_storage.move_to_permanent(temp_path, permanent_path):
            logger.info(f"Image approved and saved to {permanent_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error saving approved image: {str(e)}")
        return False

def reject_image(temp_path: str) -> bool:
    """
    Delete a temporary image that has been rejected
    
    Args:
        temp_path: Path to the temporary image
        
    Returns:
        True if successful, False otherwise
    """
    if not temp_path or not os.path.exists(temp_path):
        logger.warning(f"Rejected image not found (may have already been deleted): {temp_path}")
        return True
    
    try:
        os.remove(temp_path)
        logger.info(f"Rejected image deleted: {temp_path}")
        return True
    except Exception as e:
        logger.error(f"Error deleting rejected image: {str(e)}")
        return False

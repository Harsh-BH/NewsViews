"""
Utility functions for Google Drive operations
"""
import re
import requests
from urllib.parse import urlparse, parse_qs
import os
import tempfile
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("utils.gdrive")

def extract_file_id(drive_url: str) -> str:
    """
    Extract Google Drive file ID from various Google Drive URL formats
    """
    # Standard drive link format
    # https://drive.google.com/file/d/FILEID/view
    file_id_match = re.search(r'\/d\/(.+?)(?:\/|$)', drive_url)
    if file_id_match:
        return file_id_match.group(1)
    
    # Alternate format with query parameters
    # https://drive.google.com/open?id=FILEID
    parsed_url = urlparse(drive_url)
    if 'drive.google.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'id' in query_params:
            return query_params['id'][0]
    
    # Sharing URLs
    # https://docs.google.com/file/d/FILEID/edit
    file_id_match = re.search(r'\/file\/d\/(.+?)(?:\/|$)', drive_url)
    if file_id_match:
        return file_id_match.group(1)
    
    # Export URLs (for Google Docs, Sheets, etc.)
    # https://docs.google.com/document/d/FILEID/export?format=pdf
    file_id_match = re.search(r'\/d\/(.+?)(?:\/|$)', drive_url)
    if file_id_match:
        return file_id_match.group(1)
        
    # If no pattern matches, return the original URL
    logger.warning(f"Could not extract Google Drive file ID from URL: {drive_url}")
    return None

def get_direct_download_url(file_id: str) -> str:
    """
    Convert a Google Drive file ID to a direct download URL
    """
    if not file_id:
        return None
    
    # This is the format that works for public files
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def download_file(url: str, dest_path: str = None) -> tuple[bool, str]:
    """
    Download a file from Google Drive to a local path
    
    Args:
        url: Google Drive URL or file ID
        dest_path: Destination path (if None, a temporary file will be created)
        
    Returns:
        Tuple of (success, file_path_or_error_message)
    """
    try:
        # Extract file ID if URL is provided
        file_id = extract_file_id(url) if url.startswith('http') else url
        
        if not file_id:
            return False, f"Invalid Google Drive URL: {url}"
            
        # Get direct download URL
        direct_url = get_direct_download_url(file_id)
        
        # Create a temporary file if destination path is not provided
        if not dest_path:
            # Create temporary directory if it doesn't exist
            temp_dir = os.path.join(tempfile.gettempdir(), 'newsviews_temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            # For temporary files, we'll use a generic extension since we don't know the type yet
            temp_file = tempfile.NamedTemporaryFile(delete=False, 
                                                   suffix='.tmp', 
                                                   dir=temp_dir, 
                                                   prefix='gdrive_')
            dest_path = temp_file.name
            temp_file.close()
        
        # Download the file
        logger.info(f"Downloading file from Google Drive: {file_id} to {dest_path}")
        response = requests.get(direct_url, stream=True)
        
        if response.status_code != 200:
            return False, f"Failed to download file. Status code: {response.status_code}"
            
        # Check if this is the "Google Drive can't scan this file for viruses" page
        if 'Content-Disposition' not in response.headers:
            # For large files, Google Drive shows a confirmation page
            # We need to use a different approach for large files
            confirm_match = re.search(r'confirm=([^&]+)', response.text)
            if confirm_match:
                confirm_code = confirm_match.group(1)
                direct_url += f"&confirm={confirm_code}"
                response = requests.get(direct_url, stream=True)
                if response.status_code != 200:
                    return False, f"Failed to download large file. Status code: {response.status_code}"
        
        # Write the file to the destination path
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)
                    
        logger.info(f"Successfully downloaded file to {dest_path}")
        return True, dest_path
    
    except Exception as e:
        error_msg = f"Error downloading file: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

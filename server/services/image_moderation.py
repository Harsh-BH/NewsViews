import base64
import os
import io
from PIL import Image
import groq
from models import ImageModerationResult
import config
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("services.image_moderation")

class ImageModerator:
    def __init__(self):
        self.client = groq.Groq(api_key=config.GROQ_API_KEY)
        
    def moderate_image(self, image_path: str) -> ImageModerationResult:
        """Check if an image is appropriate using file analysis and Groq's LLM for additional checks"""
        try:
            # Validate file exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return ImageModerationResult(
                    is_appropriate=False, 
                    reason="Image file not found"
                )
                
            logger.info(f"Moderating image: {image_path}")
            
            # First, perform a basic file analysis
            try:
                # File size check
                file_size = os.path.getsize(image_path)
                file_size_mb = file_size / (1024 * 1024)
                
                # Open the image to validate and extract properties
                with Image.open(image_path) as img:
                    width, height = img.size
                    format_name = img.format
                    mode = img.mode
                    
                    # Analyze basic image properties
                    is_very_small = width < 50 or height < 50
                    is_very_large = width > 5000 or height > 5000 or file_size_mb > 10
                    is_transparent = 'A' in mode
                    
                    logger.info(f"Image properties: {width}x{height}, {format_name}, {mode}, {file_size_mb:.2f}MB")
                    
                    # Check for suspicious image characteristics
                    if is_very_small:
                        return ImageModerationResult(is_appropriate=False, reason="Image dimensions are too small")
                    
                    if is_very_large:
                        logger.warning(f"Image is very large: {width}x{height}, {file_size_mb:.2f}MB")
                        # We'll still allow large images, but resize them
                        
                    # Create a textual description of the image for Groq to analyze
                    image_description = f"Image information: {width}x{height} pixels, {format_name} format, {file_size_mb:.2f}MB file size, color mode: {mode}."
                    
                    # Resize if necessary to reduce size
                    if width > 2000 or height > 2000:
                        logger.info(f"Resizing large image: {width}x{height}")
                        img.thumbnail((2000, 2000))
                        
                        # Save to a buffer to get a description of colors
                        buffer = io.BytesIO()
                        img.save(buffer, format="PNG")
                    
                    # Get a summary of color distribution for the image
                    try:
                        # Sample some pixels to describe the color palette
                        colors = img.getcolors(maxcolors=10)
                        if colors:
                            color_description = "Image contains predominantly "
                            
                            # Sort colors by count (most frequent first)
                            colors.sort(key=lambda x: x[0], reverse=True)
                            
                            # Add top 3 colors to description
                            for i, (count, color) in enumerate(colors[:3]):
                                if i > 0:
                                    color_description += ", "
                                
                                if isinstance(color, tuple) and len(color) >= 3:
                                    r, g, b = color[:3]
                                    
                                    # Simple color naming
                                    if r > 200 and g > 200 and b > 200:
                                        color_name = "white"
                                    elif r < 50 and g < 50 and b < 50:
                                        color_name = "black"
                                    elif r > 200 and g < 100 and b < 100:
                                        color_name = "red"
                                    elif r < 100 and g > 200 and b < 100:
                                        color_name = "green"
                                    elif r < 100 and g < 100 and b > 200:
                                        color_name = "blue"
                                    elif r > 200 and g > 200 and b < 100:
                                        color_name = "yellow"
                                    else:
                                        color_name = f"RGB({r},{g},{b})"
                                        
                                    color_description += f"{color_name}"
                            
                            image_description += " " + color_description
                    except:
                        # If color analysis fails, just continue
                        pass
                
                # Now send the text description to Groq API
                logger.info("Sending image description to Groq API for moderation")
                response = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an image moderator. You'll be given a description of an image file. " +
                                      "Based on the information provided, determine if the image is likely " +
                                      "appropriate for a public news website. Respond with APPROPRIATE or INAPPROPRIATE. " +
                                      "Since you cannot see the actual image content, focus on technical aspects " +
                                      "and assume the image is appropriate unless there are suspicious technical " +
                                      "characteristics."
                        },
                        {
                            "role": "user",
                            "content": f"Based on this information about an uploaded image, is it likely appropriate for a public news website? {image_description}"
                        }
                    ],
                    max_tokens=100
                )
                
                # Parse response
                result = response.choices[0].message.content.strip().upper()
                logger.info(f"Moderation result based on image properties: {result}")
                
                if "INAPPROPRIATE" in result:
                    reason = result.replace("INAPPROPRIATE", "").strip()
                    logger.warning(f"Image deemed potentially inappropriate based on properties: {reason}")
                    return ImageModerationResult(is_appropriate=False, reason=reason)
                else:
                    logger.info("Image passed basic property moderation check")
                    return ImageModerationResult(is_appropriate=True)
                    
            except Exception as img_err:
                logger.error(f"Error analyzing image: {str(img_err)}")
                return ImageModerationResult(
                    is_appropriate=False,
                    reason=f"Error analyzing image: {str(img_err)}"
                )
                
        except Exception as e:
            logger.error(f"Error during image moderation: {str(e)}")
            return ImageModerationResult(
                is_appropriate=False, 
                reason=f"Error processing image: {str(e)}"
            )
    
    def moderate_image_with_fallback(self, image_path: str) -> ImageModerationResult:
        """Alternative implementation that doesn't require sending the image to Groq"""
        try:
            # Validate file exists
            if not os.path.exists(image_path):
                return ImageModerationResult(
                    is_appropriate=False, 
                    reason="Image file not found"
                )
            
            # Get file stats
            file_size = os.path.getsize(image_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Basic size check
            if file_size_mb > 20:  # 20MB is very large for a normal news image
                return ImageModerationResult(
                    is_appropriate=False,
                    reason=f"Image file is too large ({file_size_mb:.1f}MB)"
                )
                
            # Try to open and validate the image
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    format = img.format
                    
                    # Perform basic checks
                    if width < 50 or height < 50:
                        return ImageModerationResult(
                            is_appropriate=False,
                            reason="Image dimensions are too small"
                        )
                        
                    if width > 8000 or height > 8000:
                        return ImageModerationResult(
                            is_appropriate=False,
                            reason=f"Image dimensions are too large ({width}x{height})"
                        )
            except Exception as e:
                return ImageModerationResult(
                    is_appropriate=False,
                    reason=f"Invalid image file: {str(e)}"
                )
                
            # If we get here, the image passes basic checks
            # Since we can't check actual content, we treat the image as appropriate
            logger.info(f"Image passed basic validation checks: {image_path}")
            return ImageModerationResult(is_appropriate=True)
            
        except Exception as e:
            return ImageModerationResult(
                is_appropriate=False,
                reason=f"Error processing image: {str(e)}"
            )

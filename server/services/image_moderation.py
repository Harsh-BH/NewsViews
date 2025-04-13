import httpx
import base64
from PIL import Image
import io
import os
from config import settings
from typing import Tuple, Dict, Any

class ImageModerationService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def moderate_image(self, image_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if the image is appropriate using OpenAI's GPT-4o API.
        Returns (is_appropriate, response_details)
        """
        # Check if file exists
        if not os.path.exists(image_path):
            return False, {"error": "Image file not found"}
            
        try:
            # Open the image and convert to base64
            with Image.open(image_path) as img:
                # Resize large images to reduce API costs and processing time
                max_size = 1024
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size))
                
                # Convert to RGB if it has an alpha channel
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Prepare the API request
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI image moderator. Analyze the uploaded image and determine if it's appropriate for a public news site. Check for violence, explicit content, hate symbols, or other inappropriate material."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Is this image appropriate for a public news website? If not, explain why."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            # Call OpenAI API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json=payload,
                    headers=self.headers
                )
                
                result = response.json()
                
                if "error" in result:
                    return False, {"error": result["error"]["message"]}
                    
                # Extract the response content
                content = result["choices"][0]["message"]["content"].lower()
                
                # Determine if the image is appropriate
                inappropriate_keywords = ["inappropriate", "not appropriate", "unsuitable", "explicit", "violent", "harmful"]
                is_appropriate = not any(keyword in content for keyword in inappropriate_keywords)
                
                return is_appropriate, {
                    "response": content,
                    "moderation_details": result
                }
                
        except Exception as e:
            return False, {"error": f"Image moderation failed: {str(e)}"}

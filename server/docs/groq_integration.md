# Groq AI Integration for Image Moderation

This document explains how Groq AI is used for image moderation in the NewsViews backend.

## Overview

NewsViews uses Groq's LLaMA 3 model to moderate images attached to news submissions. The system sends base64-encoded images to Groq's API, which evaluates whether the image is appropriate for public display.

## Groq API Input Format

### Image Moderation Request

The system sends a request to Groq's AI with the following components:

1. **Model**: `llama3-70b-8192`

2. **System Message**:
   ```
   You are an image moderator. Check if the provided image contains inappropriate content such as violence, nudity, hate symbols, etc. Respond with APPROPRIATE or INAPPROPRIATE followed by a brief reason.
   ```

3. **User Message**: Two-part message consisting of:
   - Text component: "Is this image appropriate for a public news website?"
   - Image component: Base64-encoded image in data URL format (`data:image/png;base64,`)

### Example Request Structure:

```json
{
  "model": "llama3-70b-8192",
  "messages": [
    {
      "role": "system",
      "content": "You are an image moderator. Check if the provided image contains inappropriate content such as violence, nudity, hate symbols, etc. Respond with APPROPRIATE or INAPPROPRIATE followed by a brief reason."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Is this image appropriate for a public news website?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
          }
        }
      ]
    }
  ],
  "max_tokens": 100
}
```

## Expected Response Format

The system expects Groq's API to return a text response that:

1. Starts with either "APPROPRIATE" or "INAPPROPRIATE"
2. Optionally followed by a brief explanation

Examples:
- `APPROPRIATE This is a typical outdoor festival scene with no concerning content.`
- `INAPPROPRIATE The image contains graphic violence that would not be suitable for public display.`

## Configuring Groq API

To use Groq for image moderation:

1. Sign up for a Groq API account at https://console.groq.com/
2. Obtain an API key
3. Add your API key to the `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Image Preprocessing

Before sending to Groq's API, the system performs these preprocessing steps:

1. Validates the image file exists
2. Opens the image to verify it's a valid image file
3. Resizes large images (>2000px in any dimension) to reduce API payload size
4. Converts the image to base64 format
5. Wraps the base64 data in a data URL

## Handling Moderation Results

Based on Groq's response:

- If determined appropriate: The submission continues processing
- If determined inappropriate: 
  - The image is deleted from the server
  - The submission is marked as rejected
  - The reason is stored in the database
  - If synced from Google Sheets, the entry is marked as inappropriate in the sheet

## Fallback Behavior

If Groq API is unavailable or returns an error:

1. The error is logged
2. The image is considered inappropriate by default
3. The submission is rejected with the error reason

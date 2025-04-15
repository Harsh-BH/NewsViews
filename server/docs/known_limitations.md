# Known Limitations

This document outlines known limitations and constraints of the NewsViews system.

## Image Moderation with Groq AI

As of April 2025, Groq AI does not support multimodal content in the same way that OpenAI's GPT-4o does. Specifically:

1. **No direct image analysis**: Groq cannot analyze images directly through their API. Our system works around this by:
   - Analyzing image metadata (dimensions, file size, format)
   - Using textual descriptions of these properties for basic moderation

2. **Workaround limitations**: Our current approach can detect:
   - Invalid image files
   - Suspicious file sizes or dimensions
   - Basic format violations

   It cannot detect:
   - Inappropriate visual content
   - Violence, nudity, or hate symbols in images
   - Misleading or altered images

## Alternatives

If more robust image moderation is required, consider:

1. **Switch to OpenAI**: Change the moderation service to use OpenAI's GPT-4o
2. **Dedicated image moderation API**: Implement a specialized service like Google Cloud Vision API's SafeSearch
3. **Human moderation**: Add a human review step for images before publication

## Configuration

If you wish to disable AI-based moderation completely and rely only on basic file checks:

```
# In .env file
USE_AI_MODERATION=false
```

# NewsViews Backend Input Specification

This document outlines the input types and formats expected by the NewsViews backend system.

## API Endpoints Input Format

### POST `/submissions/validate`

This endpoint expects a multipart form submission with the following fields:

| Field Name | Type | Format | Required | Description |
|------------|------|--------|----------|-------------|
| title | String | Plain text | Yes | The news title |
| description | String | Plain text | Yes | News description (min 50 characters) |
| city | String | Plain text | Yes | City where the news occurred |
| category | String | Plain text | Yes | News category (e.g., Accident, Festival, Community Event) |
| publisher_name | String | Plain text | Yes | First name of the publisher |
| publisher_phone | String | Plain text | Yes | Phone number of the publisher |
| image | File | JPEG/PNG | Yes | Image related to the news |

**Example Request:**
```
curl -X POST "http://localhost:8000/submissions/validate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Local Festival Draws Record Crowds" \
  -F "description=The annual summer festival in downtown attracted an estimated 10,000 visitors this weekend, breaking all previous attendance records. Organizers credited good weather and expanded attractions." \
  -F "city=Springfield" \
  -F "category=Festival" \
  -F "publisher_name=John" \
  -F "publisher_phone=5551234567" \
  -F "image=@festival.jpg;type=image/jpeg"
```

**Response Format:**
```json
{
  "validation": {
    "is_valid": true,
    "errors": []
  },
  "duplicate_check": {
    "is_duplicate": false,
    "similarity_score": null,
    "duplicate_entry_id": null
  },
  "image_moderation": {
    "is_appropriate": true,
    "reason": null
  },
  "submission_id": 123,
  "status": "approved"
}
```

### GET `/submissions/db`

Retrieves submissions from the database.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skip | Integer | No | Number of records to skip (default: 0) |
| limit | Integer | No | Maximum number of records to return (default: 100) |
| status | String | No | Filter by status (approved, rejected, pending) |

**Example Request:**
```
curl -X GET "http://localhost:8000/submissions/db?status=approved&limit=10" -H "accept: application/json"
```

## Google Sheets Input Format

The sync service expects the Google Sheet to have the following columns:

| Column | Format | Description |
|--------|--------|-------------|
| Timestamp | Date/Time | When the form was submitted |
| News Title | Text | Title of the news |
| News Description | Text | Description of the news (min 50 characters) |
| City | Text | City where the news occurred |
| Topic/Category | Text | News category |
| Publisher's First Name | Text | First name of the publisher |
| Publisher's Phone Number | Text | Phone number of the publisher |
| Image Upload | URL | Link to the uploaded image |

### Example Google Sheet Row:

| Timestamp | News Title | News Description | City | Topic/Category | Publisher's First Name | Publisher's Phone Number | Image Upload |
|-----------|------------|------------------|------|----------------|----------------------|------------------------|-------------|
| 2023-07-15 14:30:45 | Traffic Accident on Main Street | A three-car collision occurred on Main Street today, causing delays for about 2 hours. No serious injuries were reported. | Centerville | Accident | Mark | 5551234567 | https://drive.google.com/file/d/1234567/view |

## File Upload Requirements

### Image Files

| Parameter | Specification |
|-----------|---------------|
| Allowed Formats | JPG, JPEG, PNG |
| Maximum Size | Not explicitly limited (consider adding a limit) |
| Recommended Dimensions | Images larger than 2000x2000 pixels will be resized |

## Database Record Input Format

When creating database records, the input data is processed from either API submissions or Google Sheet entries and stored in the following format:

### `submissions` Table:

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| title | String (255) | Text | News title |
| description | Text | Text | News description |
| city | String (100) | Text | City name |
| category | String (100) | Text | News category |
| publisher_name | String (100) | Text | Publisher's name |
| publisher_phone | String (20) | Text | Publisher's phone number |
| image_path | String (255) | Path | File system path to saved image |
| is_valid | Boolean | True/False | Whether submission passed validation |
| is_duplicate | Boolean | True/False | Whether submission is a duplicate |
| duplicate_score | Float | 0.0-1.0 | Similarity score if duplicate |
| duplicate_reference_id | String | ID | Reference to duplicate entry |
| is_appropriate_image | Boolean | True/False | Whether image passed moderation |
| status | String (20) | Text | "approved", "rejected", or "pending" |

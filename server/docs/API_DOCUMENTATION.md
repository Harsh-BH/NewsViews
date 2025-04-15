# NewsViews API Documentation

This document provides details about the NewsViews API endpoints for frontend integration.

## Base URL

```
http://localhost:8000
```

For production, use the actual server domain.

## Core Endpoints

### Health Check

Check if the API is running properly.

```
GET /health
```

**Response**:
```json
{
  "status": "healthy"
}
```

### Root Endpoint

Basic welcome endpoint.

```
GET /
```

**Response**:
```json
{
  "message": "Welcome to NewsViews API"
}
```

## Submissions Endpoints

### Get All Submissions

Retrieve a list of all news submissions.

```
GET /submissions
```

**Query Parameters**:
- `skip` (optional): Number of records to skip (for pagination)
- `limit` (optional): Maximum number of records to return

**Response**:
```json
{
  "items": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "author": "string",
      "submission_date": "2023-01-01T00:00:00",
      "status": "pending",
      "media_files": ["url1", "url2"],
      "category": "string"
    }
  ],
  "total": 0,
  "page": 1,
  "pages": 1
}
```

### Get Submission by ID

Retrieve a specific submission by its ID.

```
GET /submissions/{submission_id}
```

**Response**:
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "author": "string",
  "submission_date": "2023-01-01T00:00:00",
  "status": "pending",
  "media_files": ["url1", "url2"],
  "category": "string"
}
```

### Create New Submission

Submit a new news item.

```
POST /submissions
```

**Request Body**:
```json
{
  "title": "string",
  "content": "string",
  "author": "string",
  "category": "string"
}
```

**Response**:
```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "author": "string",
  "submission_date": "2023-01-01T00:00:00",
  "status": "pending",
  "media_files": [],
  "category": "string"
}
```

### Upload Media Files

Upload media files for a submission.

```
POST /submissions/{submission_id}/upload
```

**Request**:
- Form data with files (multipart/form-data)

**Response**:
```json
{
  "file_urls": ["url1", "url2"]
}
```

### Update Submission Status

Update the status of a submission.

```
PUT /submissions/{submission_id}/status
```

**Request Body**:
```json
{
  "status": "approved" | "rejected" | "pending"
}
```

**Response**:
```json
{
  "id": "string",
  "status": "approved",
  "message": "Status updated successfully"
}
```

## Sync Endpoints

### Trigger Manual Sync

Manually trigger synchronization with Google Sheets.

```
POST /sync/trigger
```

**Response**:
```json
{
  "status": "syncing",
  "message": "Sync process started"
}
```

### Get Sync Status

Check the current status of synchronization.

```
GET /sync/status
```

**Response**:
```json
{
  "last_sync": "2023-01-01T00:00:00",
  "status": "idle" | "syncing" | "failed",
  "last_error": "string or null"
}
```

### Configure Sync Settings

Update the synchronization settings.

```
PUT /sync/config
```

**Request Body**:
```json
{
  "sheet_id": "string",
  "interval_minutes": 30
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Sync settings updated"
}
```

## Media Access

All uploaded media files can be accessed via:

```
GET /uploads/{filename}
```

## Error Responses

All API errors follow a standard format:

```json
{
  "detail": "Error message describing the issue"
}
```

Common HTTP status codes:
- `400`: Bad Request
- `404`: Resource Not Found
- `500`: Server Error

## Notes for Frontend Implementation

1. For file uploads, use multipart/form-data format
2. All dates are returned in ISO format (YYYY-MM-DDThh:mm:ss)
3. Pagination is available for list endpoints using skip/limit parameters
4. Media URLs are relative to the API base URL
# Duplicate Content Detection

This document explains how the NewsViews system detects duplicate news submissions.

## Overview

The system uses text similarity comparison to identify duplicate submissions. When a new submission is received, its description is compared against all existing submissions in the database. If the similarity exceeds a configured threshold, the new submission is flagged as a duplicate.

## Input Format

The duplicate checker receives two primary inputs:

1. **New Submission**: A `NewsSubmission` object containing:
   - `title`: String
   - `description`: String (This is the primary field used for comparison)
   - `city`: String
   - `category`: String
   - `publisher_name`: String
   - `publisher_phone`: String
   - `image_path`: String

2. **Existing Submissions**: An array of submission objects, each containing at minimum:
   - `description`: String

## Algorithm

The duplicate detection algorithm works as follows:

1. Extract the description text from all existing submissions
2. Add the new submission's description to create a complete text corpus
3. Convert all texts to TF-IDF vectors using scikit-learn's `TfidfVectorizer`
   - English stopwords are removed during this process
4. Extract the vector for the new submission (last row of the TF-IDF matrix)
5. Calculate cosine similarity between the new submission vector and all existing submission vectors
6. Find the maximum similarity score and the index of the most similar submission
7. If the maximum similarity score exceeds the configured threshold (default: 0.8), flag as duplicate

## Example Similarity Calculation

For submission descriptions:

1. Original: "Traffic accident on Main Street caused delays for several hours yesterday."
2. Potential duplicate: "Yesterday's traffic accident on Main Street led to hours of delays for motorists."

The system would:
- Convert both to TF-IDF vectors
- Calculate cosine similarity (might be ~0.85)
- Since 0.85 > 0.8 (default threshold), the second would be marked as a duplicate

## Configuration

The duplicate detection threshold can be configured in the `.env` file:

```
DUPLICATE_THRESHOLD=0.8
```

Values closer to 1.0 require higher similarity (more strict), while values closer to 0.0 are more lenient.

## Response Format

The duplicate checker returns a `DuplicateCheckResult` object containing:

```json
{
  "is_duplicate": true|false,
  "similarity_score": 0.85,  // Float between 0 and 1, or null if not a duplicate
  "duplicate_entry_id": "5"  // ID of the matching entry, or null if not a duplicate
}
```

## Handling Duplicates

When a duplicate is detected:

1. The submission is marked as a duplicate in the database
2. The similarity score and reference to the original submission are stored
3. If from Google Sheets, the entry is marked as a duplicate in the sheet
4. The system does not publish the duplicate content

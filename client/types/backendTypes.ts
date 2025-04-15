// Types representing the data structures from the backend

export interface BackendNewsItem {
  id: string;
  title: string;
  content: string;
  author?: string;
  phone?: string;
  location?: string;
  category?: string;
  media_files?: string[];
  status?: string;
  submission_date: string;
  [key: string]: unknown; // For any other properties that might be present
}

export interface BackendNewsResponse {
  items: BackendNewsItem[];
  total?: number;
  page?: number;
  pages?: number;
}

// Common error type for error handling
export interface ApiError {
  error: string;
  message: string;
  name?: string;
  url?: string;
  details?: string;
}

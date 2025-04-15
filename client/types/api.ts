
export interface ApiSubmissionItem {
  id?: string;
  title?: string;
  content?: string;
  description?: string;
  author?: string;
  publisher_name?: string;
  publisher_phone?: string;
  location?: string;
  city?: string;
  category?: string;
  image_url?: string;
  status?: string;
  timestamp?: string;
  submission_date?: string;
  media_files?: string[];
}

export interface ApiPaginatedResponse {
  items: ApiSubmissionItem[];
  total: number;
  page: number;
  pages: number;
  limit: number;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, unknown>;
}

// Define a type for unstructured data when working with unknown API responses
export type UnknownRecord = Record<string, unknown>;

// A helper type for processing raw API data with unknown structure
export type RawApiData = ApiSubmissionItem | ApiSubmissionItem[] | ApiPaginatedResponse | UnknownRecord | null;

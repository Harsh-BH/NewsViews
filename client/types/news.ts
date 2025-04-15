export interface NewsItem {
  id?: string;  // Make ID optional since we may generate it
  title: string;
  description: string;  // maps to description in API
  publisher_name: string; // From API directly
  publisher_phone?: string; // From API directly
  city: string;
  category: string;
  image_url: string | null;
  status?: 'pending' | 'approved' | 'rejected';
  submission_date?: string;
  timestamp?: string; // Some items use timestamp instead of submission_date
}

export interface NewsFilters {
  status?: string;
  city?: string;
  category?: string;
}

export interface PaginationInfo {
  total: number;
  page: number;
  pages: number;
  limit: number;
}

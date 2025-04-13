export interface NewsItem {
  id: string;
  title: string;
  description: string;
  city: string;
  category: string;
  reporter_name: string;
  contact_number: string;
  image_url: string | null;
  status: string;
  created_at: string;
}

export interface NewsFilters {
  status?: string;
  category?: string;
  city?: string;
  limit?: number;
  offset?: number;
}

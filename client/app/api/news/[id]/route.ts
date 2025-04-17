import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import axios from 'axios';

const API_BASE_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> } // Key change here
) {
  try {
    const resolvedParams = await params; // Must await the params
    const { id } = resolvedParams;

    const response = await axios.get(`${API_BASE_URL}/news/${id}`);
    
    // Process image URL
    const newsItem = response.data;
    if (newsItem.image_url && !newsItem.image_url.startsWith('http')) {
      newsItem.image_url = `${API_BASE_URL}${newsItem.image_url}`;
    }
    
    return NextResponse.json(newsItem);
  } catch (error) {
    console.error(`Error fetching news:`, error);
    return NextResponse.json(
      { error: `Failed to fetch news item` },
      { status: 404 }
    );
  }
}

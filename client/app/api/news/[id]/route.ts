import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const API_BASE_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    
    try {
      const response = await axios.get(`${API_BASE_URL}/news/${id}`);
      
      // Process image URL to ensure it has a full URL
      const newsItem = response.data;
      if (newsItem.image_url && !newsItem.image_url.startsWith('http')) {
        newsItem.image_url = `${API_BASE_URL}${newsItem.image_url}`;
      }
      
      return NextResponse.json(newsItem);
    } catch (error) {
      console.error(`Error fetching news with ID ${id}:`, error);
      return NextResponse.json(
        { error: `Failed to fetch news with ID ${id}` },
        { status: 404 }
      );
    }
  } catch (error) {
    console.error('Error in API route handler:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

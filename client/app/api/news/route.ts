import { NextRequest, NextResponse } from 'next/server';
import type { NewsItem } from '../../../types/news';
import type { BackendNewsItem } from '../../../types/backendTypes';

// Make sure this points to your actual backend server
const API_BASE_URL = 'http://localhost:8000';

export async function GET(request: NextRequest) {
  console.log("API route called: /api/news");

  try {
    // Get query parameters from the request
    const { searchParams } = new URL(request.url);
    
    // Forward the request to the correct endpoint
    const url = `${API_BASE_URL}/submissions`;
    console.log(`Forwarding request to: ${url}`);
    
    try {
      // Pass along any query parameters
      const response = await fetch(`${url}?${searchParams.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });
      
      console.log('Backend response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error:', errorText);
        return NextResponse.json(
          { error: `Backend returned status ${response.status}`, details: errorText },
          { status: response.status }
        );
      }
      
      // Parse the response
      const data = await response.json();
      console.log('Backend data structure:', Object.keys(data));
      
      // Check if we got the expected structure
      if (data && data.items && Array.isArray(data.items)) {
        // Process submissions to match our NewsItem structure
        const newsItems: NewsItem[] = data.items.map((item: BackendNewsItem) => ({
          id: item.id,
          title: item.title,
          description: item.content,
          publisher_name: item.author || 'Anonymous',
          publisher_phone: item.phone || 'N/A',
          city: item.location || 'Unknown',
          category: item.category || 'General',
          image_url: item.media_files && item.media_files.length > 0 
            ? `${API_BASE_URL}${item.media_files[0]}` 
            : null,
          status: item.status || 'approved',
          submission_date: item.submission_date
        }));
        
        // Return the processed data along with pagination info
        return NextResponse.json({
          items: newsItems,
          total: data.total || 0,
          page: data.page || 1,
          pages: data.pages || 1
        });
      } else {
        throw new Error("Invalid response format from backend");
      }
    } catch (error: unknown) {
      console.error('Error details:', error instanceof Error ? error.name : 'Unknown error', 
                    error instanceof Error ? error.message : String(error));
      
      return NextResponse.json(
        { 
          error: 'Failed to fetch from backend',
          message: error instanceof Error ? error.message : String(error),
          name: error instanceof Error ? error.name : 'Unknown error',
          url: url
        }, 
        { status: 500 }
      );
    }
  } catch (error: unknown) {
    console.error('Error in API route handler:', error instanceof Error ? error.message : String(error));
    return NextResponse.json(
      { error: 'API route error', message: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}



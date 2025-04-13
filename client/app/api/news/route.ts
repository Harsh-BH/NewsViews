import { NextRequest, NextResponse } from 'next/server';

// Make sure this points to your actual backend server
// Using hardcoded URL to eliminate environment variable issues
const API_BASE_URL = 'http://localhost:8000';

export async function GET(request: NextRequest) {
  console.log("API route called: /api/news");

  try {
    // Get URL search params
    const { searchParams } = new URL(request.url);
    
    // Simplified request to diagnose the issue
    // Just try to fetch all news without filters first
    const url = `${API_BASE_URL}/news`;
    console.log(`Attempting direct fetch from: ${url}`);
    
    try {
      // Use fetch instead of axios for a simpler request
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });
      
      console.log('Fetch response status:', response.status);
      
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
      console.log('Backend data received, count:', Array.isArray(data) ? data.length : 'not an array');
      
      // Ensure we got an array
      if (!Array.isArray(data)) {
        console.error('Backend returned non-array data:', data);
        return NextResponse.json(
          { error: 'Backend returned unexpected data format' },
          { status: 500 }
        );
      }
      
      // Process image URLs
      const newsItems = data.map(item => ({
        ...item,
        image_url: item.image_url && !item.image_url.startsWith('http') 
          ? `${API_BASE_URL}${item.image_url}` 
          : item.image_url
      }));
      
      return NextResponse.json(newsItems);
    } catch (error: any) {
      console.error('Error details:', error.name, error.message);
      console.error('Error stack:', error.stack);
      
      // For debugging, return a detailed error
      return NextResponse.json(
        { 
          error: 'Failed to fetch from backend',
          message: error.message,
          name: error.name,
          url: url
        }, 
        { status: 500 }
      );
    }
  } catch (error: any) {
    console.error('Error in API route handler:', error.message);
    return NextResponse.json(
      { error: 'API route error', message: error.message },
      { status: 500 }
    );
  }
}



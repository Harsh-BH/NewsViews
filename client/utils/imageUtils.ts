
/**
 * Converts a Google Drive sharing URL to a direct download URL
 * @param url The original URL that might be a Google Drive sharing link
 * @returns A direct image URL that can be used in img/Image components
 */
export function getDirectImageUrl(url: string | null): string {
  if (!url) {
    return 'https://images.unsplash.com/photo-1557992260-ec58e38d363c?w=800&q=80'; // Default image
  }

  // Handle Google Drive links
  if (url.includes('drive.google.com/file/d/')) {
    // Extract the file ID from the Google Drive URL
    const fileIdMatch = url.match(/\/d\/([^\/]+)/);
    if (fileIdMatch && fileIdMatch[1]) {
      const fileId = fileIdMatch[1];
      return `https://drive.google.com/uc?export=view&id=${fileId}`;
    }
  }

  // Handle another common Google Drive sharing format
  if (url.includes('drive.google.com/open?id=')) {
    const fileIdMatch = url.match(/id=([^&]+)/);
    if (fileIdMatch && fileIdMatch[1]) {
      const fileId = fileIdMatch[1];
      return `https://drive.google.com/uc?export=view&id=${fileId}`;
    }
  }

  return url; // Return the original URL if it's not a Google Drive link
}

/**
 * Checks if an image URL is valid before using it, with a fallback
 * @param url The image URL to check
 * @param fallbackUrl A fallback URL to use if the main one fails
 * @returns A promise that resolves to the valid URL
 */
export function validateImageUrl(url: string, fallbackUrl: string): Promise<string> {
  return new Promise((resolve) => {
    if (!url) {
      resolve(fallbackUrl);
      return;
    }
    
    const img = new Image();
    let resolved = false;
    
    // Set up timeout to prevent hanging
    const timeout = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        resolve(fallbackUrl);
      }
    }, 5000);
    
    img.onload = () => {
      clearTimeout(timeout);
      if (!resolved) {
        resolved = true;
        resolve(url);
      }
    };
    
    img.onerror = () => {
      clearTimeout(timeout);
      if (!resolved) {
        resolved = true;
        resolve(fallbackUrl);
      }
    };
    
    img.src = url;
  });
}

'use client';

const BOOKMARK_KEY = 'newsviews_bookmarks';

/**
 * Get all bookmarked news IDs from local storage
 */
export function getBookmarks(): string[] {
  if (typeof window === 'undefined') return [];
  
  try {
    const bookmarks = localStorage.getItem(BOOKMARK_KEY);
    return bookmarks ? JSON.parse(bookmarks) : [];
  } catch (error) {
    console.error('Error getting bookmarks:', error);
    return [];
  }
}

/**
 * Add a news ID to bookmarks
 */
export function addBookmark(newsId: string): void {
  if (typeof window === 'undefined') return;
  
  try {
    const bookmarks = getBookmarks();
    if (!bookmarks.includes(newsId)) {
      bookmarks.push(newsId);
      localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
    }
  } catch (error) {
    console.error('Error adding bookmark:', error);
  }
}

/**
 * Remove a news ID from bookmarks
 */
export function removeBookmark(newsId: string): void {
  if (typeof window === 'undefined') return;
  
  try {
    let bookmarks = getBookmarks();
    bookmarks = bookmarks.filter(id => id !== newsId);
    localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
  } catch (error) {
    console.error('Error removing bookmark:', error);
  }
}

/**
 * Check if a news ID is bookmarked
 */
export function isBookmarked(newsId: string): boolean {
  const bookmarks = getBookmarks();
  return bookmarks.includes(newsId);
}

/**
 * Toggle bookmark status for a news ID
 */
export function toggleBookmark(newsId: string): boolean {
  if (isBookmarked(newsId)) {
    removeBookmark(newsId);
    return false;
  } else {
    addBookmark(newsId);
    return true;
  }
}

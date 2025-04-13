'use client';

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Filter, Newspaper, TrendingUp, RefreshCcw } from 'lucide-react';
import { NewsItem, NewsFilters } from '../../types/news';
import NewsCard from './NewsCard';
import NewsFilters from './NewsFilters';
import { Button } from '../ui/button';
import { NewsIconAnimation } from '../svg/NewsIconAnimation';
import { EmptyStateAnimation } from '../svg/EmptyStateAnimation';
import { AnimatedPattern } from '../svg/AnimatedPattern';
import { motion } from 'framer-motion';

// Fixed popularity percentages for trending topics
const TRENDING_TOPICS = [
  { name: 'Technology', percentage: 85 },
  { name: 'Local', percentage: 65 },
  { name: 'Education', percentage: 75 },
  { name: 'Environment', percentage: 55 },
];

export default function NewsFeed() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [cities, setCities] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [filters, setFilters] = useState<NewsFilters>({
    status: 'approved',
  });
  const [errorDetails, setErrorDetails] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  
  // Use consistent values for view counts
  const viewCounts = useRef<{[key: string]: number}>({});
  
  useEffect(() => {
    async function loadNews() {
      setLoading(true);
      try {
        console.log("Fetching news...");
        
        // Try both ways to fetch news - first try the API route
        let newsData;
        try {
          const response = await axios.get('/api/news', { params: filters });
          newsData = response.data;
          console.log("Fetched from API route:", newsData);
        } catch (apiError) {
          console.warn("API route failed, trying direct backend:", apiError);
          
          // If API route fails, try direct backend
          const backendUrl = 'http://localhost:8000/news';
          const backendResponse = await axios.get(backendUrl, { params: filters });
          newsData = backendResponse.data;
          console.log("Fetched from direct backend:", newsData);
        }
        
        if (Array.isArray(newsData) && newsData.length > 0) {
          // Process image URLs
          const baseUrl = 'http://localhost:8000';
          const processedNews = newsData.map(item => {
            // Create consistent view count for each item
            if (!viewCounts.current[item.id]) {
              // Only generate once per item and store it
              viewCounts.current[item.id] = 100 + Math.floor((item.id.charCodeAt(0) + item.id.length) % 900);
            }
            
            return {
              ...item,
              image_url: item.image_url && !item.image_url.startsWith('http') 
                ? `${baseUrl}${item.image_url}` 
                : item.image_url || 'https://images.unsplash.com/photo-1557992260-ec58e38d363c?w=800&q=80'
            };
          });
          
          setNews(processedNews);
          
          // Extract unique cities and categories for filters
          setCities(Array.from(new Set(processedNews.map(item => item.city))).filter(Boolean));
          setCategories(Array.from(new Set(processedNews.map(item => item.category))).filter(Boolean));
          
          setError(null);
          setErrorDetails(null);
        } else if (Array.isArray(newsData) && newsData.length === 0) {
          // Empty array is a valid response
          setNews([]);
          setError(null);
          setErrorDetails(null);
        } else {
          throw new Error("Invalid response format");
        }
      } catch (err: any) {
        console.error("Error fetching news:", err);
        
        setError("Failed to load news");
        setErrorDetails(err.message);
        setNews([]);
      } finally {
        setLoading(false);
      }
    }
    
    loadNews();
  }, [filters]);
  
  const handleFilterChange = (newFilters: { city?: string; category?: string }) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters
    }));
  };
  
  return (
    <div className="relative min-h-screen bg-white">
      <AnimatedPattern />
      
      <div className="relative z-10">
        {/* Minimalist Header */}
        <header className="py-16 bg-gradient-to-r from-gray-50 to-gray-100">
          <div className="max-w-4xl mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="md:w-1/2">
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                >
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Stay <span className="text-blue-600">informed</span> with the latest news
                  </h1>
                  <p className="text-gray-600">
                    Discover stories that matter to you, curated by our community of reporters.
                  </p>
                </motion.div>
              </div>
              
              <div className="md:w-1/2 flex justify-center">
                <div className="w-64 h-64">
                  <NewsIconAnimation />
                </div>
              </div>
            </div>
          </div>
        </header>
        
        {/* Main Content */}
        <div className="max-w-6xl mx-auto px-4 py-12">
          {/* Top Action Bar */}
          <motion.div 
            className="flex justify-between items-center mb-8"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-center gap-2">
              <Newspaper className="h-5 w-5 text-blue-600" />
              <h2 className="text-xl font-medium text-gray-800">Latest News</h2>
            </div>
            
            <div className="flex items-center space-x-3">
              <Button 
                variant="outline" 
                size="sm"
                className="text-gray-600 border-gray-200"
                onClick={() => setShowFilters(!showFilters)}
              >
                <Filter className="h-4 w-4 mr-2" />
                Filters
              </Button>
              
              <Button 
                variant="outline" 
                size="sm"
                className="text-gray-600 border-gray-200"
                onClick={() => setFilters({ status: 'approved' })}
              >
                <RefreshCcw className="h-4 w-4 mr-2" />
                Reset
              </Button>
            </div>
          </motion.div>
          
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Filters - Minimalist Style */}
            <motion.aside 
              className={`lg:col-span-1 ${showFilters ? 'block' : 'hidden lg:block'}`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <div className="sticky top-8 space-y-6">
                <NewsFilters
                  cities={cities}
                  categories={categories}
                  onFilterChange={handleFilterChange}
                />
                
                {/* Trending Topics */}
                <div className="bg-white rounded-lg border border-gray-100 shadow-sm p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <TrendingUp className="h-4 w-4 text-blue-600" />
                    <h3 className="font-medium text-gray-800">Trending Topics</h3>
                  </div>
                  
                  <div className="space-y-3">
                    {TRENDING_TOPICS.map((topic, i) => (
                      <motion.div
                        key={topic.name}
                        className="flex items-center justify-between"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5 + i * 0.1 }}
                      >
                        <span className="text-sm text-gray-600">{topic.name}</span>
                        <div className="w-24 bg-gray-100 rounded-full h-1.5">
                          <motion.div 
                            className="bg-blue-500 h-1.5 rounded-full" 
                            initial={{ width: 0 }}
                            animate={{ width: `${topic.percentage}%` }}
                            transition={{ delay: 0.8 + i * 0.1, duration: 1 }}
                          />
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.aside>
            
            {/* Main Content - Clean Design */}
            <main className="lg:col-span-3">
              {loading ? (
                <div className="flex flex-col items-center justify-center py-20">
                  <svg className="animate-spin h-10 w-10 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p className="text-gray-500">Loading stories...</p>
                </div>
              ) : error ? (
                <motion.div 
                  className="bg-red-50 text-red-700 px-6 py-8 rounded-lg border border-red-100 text-center"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4 }}
                >
                  <p className="font-medium mb-3">{error}</p>
                  {errorDetails && (
                    <p className="text-sm mb-4">{errorDetails}</p>
                  )}
                  <Button
                    onClick={() => setFilters({ status: 'approved' })}
                    variant="outline"
                    className="border-red-200 text-red-700 hover:bg-red-100"
                  >
                    <RefreshCcw className="h-4 w-4 mr-2" />
                    Try again
                  </Button>
                </motion.div>
              ) : news.length === 0 ? (
                <motion.div 
                  className="bg-white border border-gray-100 rounded-lg p-12 text-center shadow-sm"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <EmptyStateAnimation className="mb-6" />
                  <h3 className="text-xl font-medium mb-2 text-gray-800">No stories found</h3>
                  <p className="text-gray-500 mb-6 max-w-md mx-auto">
                    We couldn't find any news matching your current filters.
                  </p>
                  <Button
                    onClick={() => setFilters({ status: 'approved' })}
                    variant="outline"
                  >
                    Reset Filters
                  </Button>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {news.map((item, index) => (
                      <NewsCard 
                        key={item.id} 
                        news={item} 
                        index={index}
                        viewCount={viewCounts.current[item.id] || 100 + index * 50}
                      />
                    ))}
                  </div>
                  
                  {news.length > 6 && (
                    <motion.div 
                      className="mt-12 text-center"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.8 }}
                    >
                      <Button variant="outline" className="border-gray-200 text-gray-700">
                        Load More Stories
                      </Button>
                    </motion.div>
                  )}
                </motion.div>
              )}
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}

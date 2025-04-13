'use client';

import { useState, useEffect } from 'react';
import { BookmarkIcon, Share2Icon, Eye } from 'lucide-react';
import { maskPhoneNumber, getFirstName } from '../../utils/stringUtils';
import { isBookmarked, toggleBookmark } from '../../utils/bookmarkUtils';
import { NewsItem } from '../../types/news';
import { Button } from '../ui/button';
import { Card, CardContent, CardFooter } from '../ui/card';
import { Badge } from '../ui/badge';
import { Avatar, AvatarFallback } from '../ui/avatar';
import { motion } from 'framer-motion';

interface NewsCardProps {
  news: NewsItem;
  index: number;
  viewCount: number;
}

export default function NewsCard({ news, index, viewCount = 100 }: NewsCardProps) {
  const [bookmarked, setBookmarked] = useState(false);
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setBookmarked(isBookmarked(news.id));
    setMounted(true);
  }, [news.id]);
  
  const handleBookmarkToggle = () => {
    const newStatus = toggleBookmark(news.id);
    setBookmarked(newStatus);
  };
  
  const reporterFirstName = getFirstName(news.reporter_name);
  const maskedPhone = maskPhoneNumber(news.contact_number);
  
  if (!mounted) {
    return <Card className="h-[300px] animate-pulse bg-gray-100"></Card>;
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="group"
    >
      <Card className="overflow-hidden h-full flex flex-col border-gray-100 hover:border-blue-100 transition-all">
        {news.image_url && (
          <div className="relative h-48 w-full overflow-hidden bg-gray-50">
            <img 
              src={news.image_url}
              alt={news.title}
              className="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900/40 to-transparent" />
            
            <motion.div 
              className="absolute bottom-4 left-4 flex gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Badge variant="secondary" className="bg-blue-100/80 text-blue-800 backdrop-blur-sm text-xs">
                {news.city}
              </Badge>
              <Badge variant="outline" className="bg-white/80 text-gray-800 backdrop-blur-sm text-xs border-0">
                {news.category}
              </Badge>
            </motion.div>
          </div>
        )}
        
        <CardContent className="flex-grow flex flex-col p-5 space-y-3">
          <div className="flex justify-between">
            <h2 className="text-lg font-medium text-gray-800 line-clamp-2 group-hover:text-blue-600 transition-colors">
              {news.title}
            </h2>
            <Button
              size="sm" 
              variant="ghost"
              className="h-8 w-8 p-0 rounded-full"
              onClick={handleBookmarkToggle}
            >
              <BookmarkIcon 
                className={`h-4 w-4 ${bookmarked ? 'fill-blue-500 text-blue-500' : 'text-gray-400'}`} 
              />
              <span className="sr-only">{bookmarked ? 'Bookmarked' : 'Bookmark'}</span>
            </Button>
          </div>
          
          <p className="text-sm text-gray-600 line-clamp-2 flex-grow">
            {news.description}
          </p>
        </CardContent>
        
        <CardFooter className="border-t border-gray-100 px-5 py-3 text-xs text-gray-500">
          <div className="flex justify-between items-center w-full">
            <div className="flex items-center gap-2">
              <Avatar className="h-6 w-6 bg-blue-100">
                <AvatarFallback className="text-blue-700 text-xs">{reporterFirstName.charAt(0)}</AvatarFallback>
              </Avatar>
              <span>{reporterFirstName}</span>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="flex items-center">
                <Eye className="h-3 w-3 mr-1" />
                <span>{viewCount}</span>
              </div>
              
              <Button
                size="sm" 
                variant="ghost"
                className="h-5 w-5 p-0"
              >
                <Share2Icon className="h-3 w-3 text-gray-400" />
                <span className="sr-only">Share</span>
              </Button>
            </div>
          </div>
        </CardFooter>
      </Card>
    </motion.div>
  );
}
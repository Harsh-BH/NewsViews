'use client';

import { useState } from 'react';
import { MapPin, Tag, X } from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { motion } from 'framer-motion';

interface NewsFiltersProps {
  cities: string[];
  categories: string[];
  onFilterChange: (filters: { city?: string; category?: string }) => void;
}

export default function NewsFilters({ cities, categories, onFilterChange }: NewsFiltersProps) {
  const [selectedCity, setSelectedCity] = useState<string | undefined>(undefined);
  const [selectedCategory, setSelectedCategory] = useState<string | undefined>(undefined);
  const [mounted, setMounted] = useState(false);
  
  // Client-side only rendering
  useState(() => {
    setMounted(true);
  });
  
  const handleCitySelect = (city: string) => {
    const value = city === selectedCity ? undefined : city;
    setSelectedCity(value);
    onFilterChange({ city: value, category: selectedCategory });
  };
  
  const handleCategorySelect = (category: string) => {
    const value = category === selectedCategory ? undefined : category;
    setSelectedCategory(value);
    onFilterChange({ city: selectedCity, category: value });
  };
  
  const handleReset = () => {
    setSelectedCity(undefined);
    setSelectedCategory(undefined);
    onFilterChange({});
  };
  
  if (!mounted) {
    return <div className="h-[300px] animate-pulse bg-gray-50 rounded-lg"></div>;
  }
  
  return (
    <div className="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100 flex justify-between items-center">
        <h3 className="font-medium text-gray-800 text-sm">Filter News</h3>
        
        {(selectedCity || selectedCategory) && (
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleReset}
            className="h-7 px-2 text-gray-500 hover:text-gray-700"
          >
            <X className="h-3 w-3 mr-1" />
            <span className="text-xs">Clear</span>
          </Button>
        )}
      </div>
      
      <div className="p-5 space-y-5">
        {/* Cities */}
        <div>
          <div className="flex items-center mb-3 text-sm text-gray-700">
            <MapPin className="h-3 w-3 mr-2 text-blue-500" />
            <span className="font-medium">Cities</span>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {cities.length > 0 ? (
              cities.map((city) => (
                <Badge 
                  key={city} 
                  variant={selectedCity === city ? "default" : "outline"}
                  className={`cursor-pointer text-xs px-2 py-0.5 ${
                    selectedCity === city 
                      ? 'bg-blue-100 hover:bg-blue-200 text-blue-800 border-0' 
                      : 'bg-white hover:bg-gray-50 text-gray-700 border-gray-200'
                  }`}
                  onClick={() => handleCitySelect(city)}
                >
                  {city}
                </Badge>
              ))
            ) : (
              <span className="text-sm text-gray-500">No cities available</span>
            )}
          </div>
        </div>
        
        {/* Categories */}
        <div>
          <div className="flex items-center mb-3 text-sm text-gray-700">
            <Tag className="h-3 w-3 mr-2 text-blue-500" />
            <span className="font-medium">Categories</span>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {categories.length > 0 ? (
              categories.map((category) => (
                <Badge 
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  className={`cursor-pointer text-xs px-2 py-0.5 ${
                    selectedCategory === category 
                      ? 'bg-green-100 hover:bg-green-200 text-green-800 border-0' 
                      : 'bg-white hover:bg-gray-50 text-gray-700 border-gray-200'
                  }`}
                  onClick={() => handleCategorySelect(category)}
                >
                  {category}
                </Badge>
              ))
            ) : (
              <span className="text-sm text-gray-500">No categories available</span>
            )}
          </div>
        </div>
        
        <motion.div 
          className="pt-2"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Button 
            onClick={handleReset}
            variant="ghost" 
            className="w-full text-gray-600 hover:text-blue-600 hover:bg-blue-50 text-xs h-8"
            disabled={!selectedCity && !selectedCategory}
          >
            Reset All Filters
          </Button>
        </motion.div>
      </div>
    </div>
  );
}

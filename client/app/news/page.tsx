import NewsFeed from '@/components/news/NewsFeed';

export const metadata = {
  title: 'News Feed | NewsViews',
  description: 'Browse the latest approved news submissions from our community',
};

export default function NewsPage() {
  return (
    <main>
      <NewsFeed />
    </main>
  );
}

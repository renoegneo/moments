import { useState, useEffect } from 'react';
import { getMomentsFeed } from '../services/api';
import MomentFeed from '../components/moments/MomentFeed';
import CreateMomentForm from '../components/moments/CreateMomentForm';
import { useAuth } from '../context/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const [moments, setMoments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const [skip, setSkip] = useState(0);
  const { user } = useAuth();

  const loadMoments = async (skipValue = 0) => {
    try {
      setLoading(true);
      const response = await getMomentsFeed(skipValue, 20);
      
      if (skipValue === 0) {
        setMoments(response.data.items);
      } else {
        setMoments(prev => [...prev, ...response.data.items]);
      }
      
      setHasMore(response.data.has_more);
      setSkip(skipValue);
    } catch (error) {
      console.error('Load moments error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMoments();
  }, []);

  const handleLoadMore = () => {
    loadMoments(skip + 20);
  };

  const handleMomentCreated = () => {
    loadMoments(0);
  };

  return (
    <div className="home-page">
      <div className="home-container">
        {user && <CreateMomentForm onMomentCreated={handleMomentCreated} />}
        
        <MomentFeed 
          moments={moments} 
          loading={loading}
          hasMore={hasMore}
          onLoadMore={handleLoadMore}
          onMomentDeleted={() => loadMoments(0)}
        />
      </div>
    </div>
  );
};

export default HomePage;
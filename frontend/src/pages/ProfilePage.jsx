import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getUserMoments, getUserStats } from '../services/api';
import { useAuth } from '../context/AuthContext';
import MomentCard from '../components/moments/MomentCard';
import './ProfilePage.css';

const ProfilePage = () => {
  const { userId } = useParams();
  const [moments, setMoments] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const [skip, setSkip] = useState(0);
  const { user } = useAuth();

  const loadProfile = async () => {
    try {
      setLoading(true);
      const [momentsRes, statsRes] = await Promise.all([
        getUserMoments(userId, 0, 20),
        getUserStats(userId)
      ]);
      
      setMoments(momentsRes.data.items);
      setHasMore(momentsRes.data.has_more);
      setStats(statsRes.data);
      setSkip(0);
    } catch (error) {
      console.error('Load profile error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, [userId]);

  const handleLoadMore = async () => {
    try {
      const newSkip = skip + 20;
      const response = await getUserMoments(userId, newSkip, 20);
      setMoments(prev => [...prev, ...response.data.items]);
      setHasMore(response.data.has_more);
      setSkip(newSkip);
    } catch (error) {
      console.error('Load more error:', error);
    }
  };

  if (loading) {
    return <div className="loading">Загрузка профиля...</div>;
  }

  const profileUser = moments[0]?.user;
  const isOwnProfile = user?.id === userId;

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-info">
            <h1>{profileUser?.username || 'Пользователь'}</h1>
            <span className="profile-role">{profileUser?.role || 'user'}</span>
          </div>

          {stats && (
            <div className="profile-stats">
              <div className="stat-item">
                <span className="stat-value">{stats.moments_count}</span>
                <span className="stat-label">моментов</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{stats.likes_received}</span>
                <span className="stat-label">получено лайков</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{stats.likes_given}</span>
                <span className="stat-label">отдано лайков</span>
              </div>
            </div>
          )}
        </div>

        <div className="profile-moments">
          <h2>{isOwnProfile ? 'Мои моменты' : 'Моменты пользователя'}</h2>
          
          {moments.length === 0 ? (
            <div className="no-moments">
              <p>{isOwnProfile ? 'У вас пока нет моментов' : 'У пользователя пока нет моментов'}</p>
            </div>
          ) : (
            <>
              {moments.map(moment => (
                <MomentCard 
                  key={moment.id} 
                  moment={moment}
                  onDeleted={loadProfile}
                />
              ))}

              {hasMore && (
                <button 
                  className="load-more-button" 
                  onClick={handleLoadMore}
                >
                  Загрузить ещё
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
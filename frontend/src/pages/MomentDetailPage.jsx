import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getMoment, toggleLike, deleteMoment } from '../services/api';
import { useAuth } from '../context/AuthContext';
import CommentList from '../components/comments/CommentList';
import './MomentDetailPage.css';

const MomentDetailPage = () => {
  const { id } = useParams();
  const [moment, setMoment] = useState(null);
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  const loadMoment = async () => {
    try {
      setLoading(true);
      const response = await getMoment(id);
      setMoment(response.data);
      setLikesCount(response.data.likes_count || 0);
    } catch (error) {
      console.error('Load moment error:', error);
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMoment();
  }, [id]);

  const handleLike = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const response = await toggleLike(id);
      setLiked(response.data.liked);
      setLikesCount(response.data.likes_count);
    } catch (error) {
      console.error('Like error:', error);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Удалить момент?')) return;

    try {
      await deleteMoment(id);
      navigate('/');
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  if (loading) {
    return <div className="loading">Щащаща...</div>;
  }

  if (!moment) {
    return null;
  }

  return (
    <div className="moment-detail-page">
      <div className="moment-detail-container">
        <div className="moment-detail-card">
          <div className="moment-detail-header">
            <div 
              className="moment-detail-author"
              onClick={() => navigate(`/profile/${moment.user.id}`)}
            >
              <span className="author-name">{moment.user.username}</span>
            </div>
            {user?.id === moment.user_id && (
              <button className="delete-button" onClick={handleDelete}>
                Удалить
              </button>
            )}
          </div>

          <div className="moment-detail-content">
            <p className="moment-detail-text">{moment.text}</p>
            {moment.image_url && (
              <img src={moment.image_url} alt="moment" className="moment-detail-image" />
            )}
          </div>

          <div className="moment-detail-footer">
            <button 
              className={`like-button ${liked ? 'liked' : ''}`}
              onClick={handleLike}
            >
              {liked ? '❤️' : '🤍'} {likesCount}
            </button>
            <span className="moment-detail-date">
              {new Date(moment.created_at).toLocaleString('ru-RU')}
            </span>
          </div>

          <CommentList momentId={id} />
        </div>
      </div>
    </div>
  );
};

export default MomentDetailPage;
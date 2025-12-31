import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toggleLike, deleteMoment } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import './MomentCard.css';

const MomentCard = ({ moment, onDeleted }) => {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(moment.likes_count || 0);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleLike = async (e) => {
    e.stopPropagation();
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      const response = await toggleLike(moment.id);
      setLiked(response.data.liked);
      setLikesCount(response.data.likes_count);
    } catch (error) {
      console.error('Like error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (!window.confirm('Удалить момент?')) return;

    try {
      await deleteMoment(moment.id);
      onDeleted?.();
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  const handleCardClick = () => {
    navigate(`/moment/${moment.id}`);
  };

  return (
    <div className="moment-card" onClick={handleCardClick}>
      <div className="moment-header">
        <div className="moment-author" onClick={(e) => {
          e.stopPropagation();
          navigate(`/profile/${moment.user.id}`);
        }}>
          <span className="author-name">{moment.user.username}</span>
        </div>
        {user?.id === moment.user_id && (
          <button className="delete-button" onClick={handleDelete}>
            ✕
          </button>
        )}
      </div>

      <div className="moment-content">
        <p className="moment-text">{moment.text}</p>
        {moment.image_url && (
          <img src={moment.image_url} alt="moment" className="moment-image" />
        )}
      </div>

      <div className="moment-footer">
        <button 
          className={`like-button ${liked ? 'liked' : ''}`}
          onClick={handleLike}
          disabled={loading}
        >
          {liked ? '❤️' : '🤍'} {likesCount}
        </button>
        <span className="comments-count">💬 {moment.comments_count || 0}</span>
        <span className="moment-date">
          {new Date(moment.created_at).toLocaleDateString('ru-RU')}
        </span>
      </div>
    </div>
  );
};

export default MomentCard;
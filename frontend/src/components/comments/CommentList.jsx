import { useState, useEffect } from 'react';
import { getComments, deleteComment } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import CommentForm from './CommentForm';
import './CommentList.css';

const CommentList = ({ momentId }) => {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  const loadComments = async () => {
    try {
      setLoading(true);
      const response = await getComments(momentId);
      setComments(response.data);
    } catch (error) {
      console.error('Load comments error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadComments();
  }, [momentId]);

  const handleDelete = async (commentId) => {
    if (!window.confirm('Удалить комментарий?')) return;

    try {
      await deleteComment(commentId);
      loadComments();
    } catch (error) {
      console.error('Delete comment error:', error);
    }
  };

  if (loading) {
    return <div className="loading">Загрузка комментариев...</div>;
  }

  return (
    <div className="comment-list">
      <h3>Комментарии ({comments.length})</h3>
      
      {comments.length === 0 ? (
        <p className="no-comments">Комментариев пока нет</p>
      ) : (
        <div className="comments">
          {comments.map(comment => (
            <div key={comment.id} className="comment">
              <div className="comment-header">
                <span className="comment-author">{comment.user.username}</span>
                <span className="comment-date">
                  {new Date(comment.created_at).toLocaleDateString('ru-RU')}
                </span>
                {user?.id === comment.user_id && (
                  <button 
                    className="delete-comment-button"
                    onClick={() => handleDelete(comment.id)}
                  >
                    ✕
                  </button>
                )}
              </div>
              <p className="comment-text">{comment.text}</p>
            </div>
          ))}
        </div>
      )}

      {user && <CommentForm momentId={momentId} onCommentCreated={loadComments} />}
    </div>
  );
};

export default CommentList;
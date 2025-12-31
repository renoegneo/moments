import { useState } from 'react';
import { createComment } from '../../services/api';
import './CommentForm.css';

const CommentForm = ({ momentId, onCommentCreated }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await createComment(momentId, { text });
      setText('');
      onCommentCreated?.();
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка добавления комментария');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="comment-form">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Написать комментарий..."
          required
          minLength={1}
          maxLength={300}
        />
        
        {error && <div className="error-message">{error}</div>}
        
        <button type="submit" disabled={loading || !text.trim()}>
          {loading ? 'Отправка...' : 'Отправить'}
        </button>
      </form>
    </div>
  );
};

export default CommentForm;
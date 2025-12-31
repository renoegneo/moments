import { useState } from 'react';
import { createMoment } from '../../services/api';
import './CreateMomentForm.css';

const CreateMomentForm = ({ onMomentCreated }) => {
  const [text, setText] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await createMoment({
        text,
        image_url: imageUrl || null
      });
      setText('');
      setImageUrl('');
      onMomentCreated?.();
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка создания момента');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-moment-form">
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Что у вас нового?"
          required
          minLength={1}
          maxLength={500}
          rows={3}
        />

        <input
          type="url"
          value={imageUrl}
          onChange={(e) => setImageUrl(e.target.value)}
          placeholder="URL изображения (опционально)"
        />

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading || !text.trim()}>
          {loading ? 'Публикация...' : 'Опубликовать'}
        </button>
      </form>
    </div>
  );
};

export default CreateMomentForm;
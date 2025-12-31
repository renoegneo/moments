import MomentCard from './MomentCard';
import './MomentFeed.css';

const MomentFeed = ({ moments, loading, hasMore, onLoadMore, onMomentDeleted }) => {
  if (loading && moments.length === 0) {
    return <div className="loading">Загрузка...</div>;
  }

  if (moments.length === 0) {
    return (
      <div className="empty-feed">
        <p>Пока нет моментов</p>
      </div>
    );
  }

  return (
    <div className="moment-feed">
      {moments.map(moment => (
        <MomentCard 
          key={moment.id} 
          moment={moment}
          onDeleted={onMomentDeleted}
        />
      ))}

      {hasMore && (
        <button 
          className="load-more-button" 
          onClick={onLoadMore}
          disabled={loading}
        >
          {loading ? 'Загрузка...' : 'Загрузить ещё'}
        </button>
      )}
    </div>
  );
};

export default MomentFeed;
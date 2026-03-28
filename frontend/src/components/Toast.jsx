function Toast({ message, type = 'error' }) {
  const bgColor = type === 'error' 
    ? '#ef4444' 
    : type === 'success' 
      ? '#22c55e' 
      : '#374151'

  return (
    <div style={{ 
      backgroundColor: bgColor, 
      color: 'white',
      position: 'fixed', 
      bottom: '1rem', 
      right: '1rem',
      padding: '0.75rem 1.5rem',
      borderRadius: '0.5rem',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      zIndex: 50,
      animation: 'fadeIn 0.3s ease-in-out'
    }}>
      <p style={{ fontSize: '0.875rem', fontWeight: 500, margin: 0 }}>{message}</p>
    </div>
  )
}

export default Toast

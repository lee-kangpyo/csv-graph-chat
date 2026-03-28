function Toast({ message, type = 'error' }) {
  const bgColor = type === 'error' 
    ? 'bg-red-500' 
    : type === 'success' 
      ? 'bg-green-500' 
      : 'bg-gray-700'

  return (
    <div className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in`}>
      <p className="text-sm font-medium">{message}</p>
    </div>
  )
}

export default Toast

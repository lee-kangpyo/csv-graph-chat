## 1. Project Setup

- [x] 1.1 Create project directory structure (backend/, frontend/)
- [x] 1.2 Setup FastAPI backend with dependencies (fastapi, uvicorn, duckdb, openai, python-multipart, sse-starlette)
- [x] 1.3 Setup React frontend with Vite (react, vite, zustand, tailwindcss, chart.js, axios)
- [x] 1.4 Configure TailwindCSS in frontend
- [x] 1.5 Add Chart.js via CDN or npm

## 2. Backend - Core Infrastructure

- [x] 2.1 Implement DuckDB connection and CSV reading
- [x] 2.2 Create data models (Pydantic) for CSV metadata, graph config
- [x] 2.3 Setup SQLite/PostgreSQL for basket storage
- [x] 2.4 Implement basket CRUD API endpoints

## 3. Backend - CSV Upload & Analysis

- [x] 3.1 Create CSV upload endpoint with file size validation (10MB limit)
- [x] 3.2 Implement header detection logic (meaningful vs meaningless vs missing)
- [x] 3.3 Implement data type detection (Date, Number, Category, Boolean)
- [x] 3.4 Create AI column inference prompt and integration

## 4. Backend - AI Conversation & SSE

- [x] 4.1 Setup LLM integration (z.ai coding plan / OpenAI compatible)
- [x] 4.2 Implement AI insight recommendation logic
- [x] 4.3 Create SSE endpoint for streaming AI responses
- [x] 4.4 Implement SQL generation for DuckDB queries
- [x] 4.5 Implement graph configuration generation (Chart.js format)

## 5. Frontend - UI Components

- [x] 5.1 Create main App layout with sidebar (basket)
- [x] 5.2 Implement ChatArea component for messages
- [x] 5.3 Implement Message component (AI vs User styling)
- [x] 5.4 Implement ChatInput with file upload button (+)
- [x] 5.5 Implement GraphView component (Chart.js rendering)
- [x] 5.6 Implement BasketSidebar component
- [x] 5.7 Implement BasketItem component (preview, delete buttons)
- [x] 5.8 Implement Toast component (3 second auto-dismiss)

## 6. Frontend - State Management

- [x] 6.1 Setup Zustand store for chat messages
- [x] 6.2 Setup Zustand store for basket state
- [x] 6.3 Setup Zustand store for current graph configuration
- [x] 6.4 Setup Zustand store for CSV metadata (columns, mapped names)

## 7. Frontend - API Integration

- [x] 7.1 Implement CSV upload with Axios
- [x] 7.2 Implement SSE client for AI streaming (EventSource or Fetch+ReadableStream)
- [x] 7.3 Implement basket CRUD with Axios
- [x] 7.4 Implement HTML download functionality

## 8. Integration & Testing

- [x] 8.1 Test CSV upload with various header scenarios
- [x] 8.2 Test AI conversation flow end-to-end
- [x] 8.3 Test chart rendering with different types (line, bar, doughnut, scatter)
- [x] 8.4 Test basket save, preview, delete
- [x] 8.5 Test HTML download
- [x] 8.6 Test error scenarios (file size, invalid CSV, API timeout)

## 9. Error Handling & Polish

- [x] 9.1 Implement toast error messages for all failure scenarios
- [x] 9.2 Add loading states during AI processing
- [x] 9.3 Add responsive design for mobile
- [x] 9.4 Add empty states (empty basket, no CSV uploaded)

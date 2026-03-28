## 1. Project Setup

- [ ] 1.1 Create project directory structure (backend/, frontend/)
- [ ] 1.2 Setup FastAPI backend with dependencies (fastapi, uvicorn, duckdb, openai, python-multipart, sse-starlette)
- [ ] 1.3 Setup React frontend with Vite (react, vite, zustand, tailwindcss, chart.js, axios)
- [ ] 1.4 Configure TailwindCSS in frontend
- [ ] 1.5 Add Chart.js via CDN or npm

## 2. Backend - Core Infrastructure

- [ ] 2.1 Implement DuckDB connection and CSV reading
- [ ] 2.2 Create data models (Pydantic) for CSV metadata, graph config
- [ ] 2.3 Setup SQLite/PostgreSQL for basket storage
- [ ] 2.4 Implement basket CRUD API endpoints

## 3. Backend - CSV Upload & Analysis

- [ ] 3.1 Create CSV upload endpoint with file size validation (10MB limit)
- [ ] 3.2 Implement header detection logic (meaningful vs meaningless vs missing)
- [ ] 3.3 Implement data type detection (Date, Number, Category, Boolean)
- [ ] 3.4 Create AI column inference prompt and integration

## 4. Backend - AI Conversation & SSE

- [ ] 4.1 Setup LLM integration (z.ai coding plan / OpenAI compatible)
- [ ] 4.2 Implement AI insight recommendation logic
- [ ] 4.3 Create SSE endpoint for streaming AI responses
- [ ] 4.4 Implement SQL generation for DuckDB queries
- [ ] 4.5 Implement graph configuration generation (Chart.js format)

## 5. Frontend - UI Components

- [ ] 5.1 Create main App layout with sidebar (basket)
- [ ] 5.2 Implement ChatArea component for messages
- [ ] 5.3 Implement Message component (AI vs User styling)
- [ ] 5.4 Implement ChatInput with file upload button (+)
- [ ] 5.5 Implement GraphView component (Chart.js rendering)
- [ ] 5.6 Implement BasketSidebar component
- [ ] 5.7 Implement BasketItem component (preview, delete buttons)
- [ ] 5.8 Implement Toast component (3 second auto-dismiss)

## 6. Frontend - State Management

- [ ] 6.1 Setup Zustand store for chat messages
- [ ] 6.2 Setup Zustand store for basket state
- [ ] 6.3 Setup Zustand store for current graph configuration
- [ ] 6.4 Setup Zustand store for CSV metadata (columns, mapped names)

## 7. Frontend - API Integration

- [ ] 7.1 Implement CSV upload with Axios
- [ ] 7.2 Implement SSE client for AI streaming (EventSource or Fetch+ReadableStream)
- [ ] 7.3 Implement basket CRUD with Axios
- [ ] 7.4 Implement HTML download functionality

## 8. Integration & Testing

- [ ] 8.1 Test CSV upload with various header scenarios
- [ ] 8.2 Test AI conversation flow end-to-end
- [ ] 8.3 Test chart rendering with different types (line, bar, doughnut, scatter)
- [ ] 8.4 Test basket save, preview, delete
- [ ] 8.5 Test HTML download
- [ ] 8.6 Test error scenarios (file size, invalid CSV, API timeout)

## 9. Error Handling & Polish

- [ ] 9.1 Implement toast error messages for all failure scenarios
- [ ] 9.2 Add loading states during AI processing
- [ ] 9.3 Add responsive design for mobile
- [ ] 9.4 Add empty states (empty basket, no CSV uploaded)

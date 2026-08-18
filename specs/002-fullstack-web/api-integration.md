# API Integration Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification defines the frontend API client and integration with the FastAPI backend for the Phase II full-stack todo application.

## API Client Architecture

### Client Configuration (`api.ts`)

```typescript
// Pseudocode
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiClient {
  getTasks(filters?: TaskFilters): Promise<Task[]>;
  getTask(id: number): Promise<Task>;
  createTask(data: CreateTaskInput): Promise<Task>;
  updateTask(id: number, data: UpdateTaskInput): Promise<Task>;
  deleteTask(id: number): Promise<void>;
  toggleComplete(id: number): Promise<Task>;
}
```

### Request/Response Flow

```
Component → API Client → HTTP Request → Backend API → Database
    ↓
UI Update ← Response ← JSON ← Query Result ← PostgreSQL
```

## Authentication Header

### Token Injection

```typescript
// Pseudocode
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const session = await getSession();
  const token = session?.token;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    // Token expired or invalid
    redirectToSignIn();
    throw new Error('Unauthorized');
  }
  
  return response;
}
```

## API Endpoints

### Task Endpoints

#### GET /api/tasks

**Purpose**: List all tasks for authenticated user

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | "all" | Filter: all/active/completed |
| priority | string | null | Filter: high/medium/low |
| category | string | null | Filter: work/home/personal/health/other |
| search | string | null | Search title and description |
| sort_by | string | "created_at" | Sort field |
| sort_order | string | "desc" | Sort direction: asc/desc |

**Request**:
```typescript
GET /api/tasks?status=active&priority=high&sort_by=due_date&sort_order=asc
Authorization: Bearer <token>
```

**Response 200**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "priority": "high",
    "category": "home",
    "due_date": "2026-03-05",
    "recurrence": "weekly",
    "due_time": "14:30",
    "reminder_minutes": 15,
    "reminder_sent": false,
    "created_at": "2026-03-02T10:00:00Z",
    "updated_at": "2026-03-02T10:00:00Z"
  }
]
```

**Response 401**:
```json
{
  "detail": "Not authenticated"
}
```

#### POST /api/tasks

**Purpose**: Create a new task

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "category": "home",
  "due_date": "2026-03-05",
  "recurrence": "weekly",
  "due_time": "14:30",
  "reminder_minutes": 15
}
```

**Response 201**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "priority": "medium",
  "category": "home",
  "due_date": "2026-03-05",
  "recurrence": "weekly",
  "due_time": "14:30",
  "reminder_minutes": 15,
  "reminder_sent": false,
  "created_at": "2026-03-02T10:00:00Z",
  "updated_at": "2026-03-02T10:00:00Z"
}
```

**Response 422**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty",
      "type": "value_error"
    }
  ]
}
```

#### GET /api/tasks/{task_id}

**Purpose**: Get a single task

**Response 200**: Task object
**Response 404**: `{"detail": "Task not found"}`

#### PUT /api/tasks/{task_id}

**Purpose**: Update a task

**Request Body**: Same as POST (partial update)
**Response 200**: Updated task object
**Response 404**: `{"detail": "Task not found"}`

#### DELETE /api/tasks/{task_id}

**Purpose**: Delete a task

**Response 204**: No content
**Response 404**: `{"detail": "Task not found"}`

#### PATCH /api/tasks/{task_id}/complete

**Purpose**: Toggle task completion

**Response 200**: Updated task object
**Response 404**: `{"detail": "Task not found"}`

## Error Handling

### Error Types

| Error | Status | Message | Action |
|-------|--------|---------|--------|
| Unauthorized | 401 | "Not authenticated" | Redirect to sign-in |
| Not Found | 404 | "Task not found" | Show error, refresh list |
| Validation | 422 | Field-specific message | Show inline error |
| Server Error | 500 | "Internal server error" | Show toast, retry |
| Network Error | - | "Connection failed" | Show toast, retry |

### Error Response Handling

```typescript
// Pseudocode
async function handleApiResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json();
    
    switch (response.status) {
      case 401:
        redirectToSignIn();
        throw new Error('Unauthorized');
      case 404:
        throw new Error('Not found');
      case 422:
        throw new ValidationError(error.detail);
      default:
        throw new Error('Server error');
    }
  }
  
  if (response.status === 204) {
    return null as T;
  }
  
  return response.json();
}
```

## Data Transformation

### API to Frontend

```typescript
// Pseudocode
function transformTask(apiTask: ApiTask): Task {
  return {
    ...apiTask,
    due_date: apiTask.due_date || undefined,
    due_time: apiTask.due_time || undefined,
    category: apiTask.category || undefined,
    recurrence: apiTask.recurrence || undefined,
  };
}
```

### Frontend to API

```typescript
// Pseudocode
function transformCreateInput(input: CreateTaskInput): ApiCreateTaskInput {
  return {
    title: input.title,
    description: input.description || null,
    priority: input.priority || 'medium',
    category: input.category || null,
    due_date: input.due_date || null,
    due_time: input.due_time || null,
    recurrence: input.recurrence || null,
    reminder_minutes: input.reminder_minutes || null,
  };
}
```

## Caching Strategy

### Cache Headers

- No-cache for task lists (always fresh)
- Stale-while-revalidate for individual tasks
- Cache invalidation on mutations

### Client-Side Cache

```typescript
// Pseudocode
const taskCache = new Map<number, Task>();

async function getTask(id: number): Promise<Task> {
  if (taskCache.has(id)) {
    return taskCache.get(id)!;
  }
  
  const task = await api.getTask(id);
  taskCache.set(id, task);
  return task;
}

function invalidateTaskCache(id?: number) {
  if (id) {
    taskCache.delete(id);
  } else {
    taskCache.clear();
  }
}
```

## Optimistic Updates

### Toggle Completion

```typescript
// Pseudocode
async function toggleComplete(task: Task) {
  // Optimistic update
  const optimisticTask = { ...task, is_completed: !task.is_completed };
  updateTaskInList(optimisticTask);
  
  try {
    await api.toggleComplete(task.id);
  } catch (error) {
    // Revert on error
    updateTaskInList(task);
    showError('Failed to update task');
  }
}
```

## Loading States

### Global Loading

```typescript
// Pseudocode
const [isLoading, setIsLoading] = useState(true);
const [tasks, setTasks] = useState<Task[]>([]);

useEffect(() => {
  async function loadTasks() {
    setIsLoading(true);
    try {
      const data = await api.getTasks(filters);
      setTasks(data);
    } finally {
      setIsLoading(false);
    }
  }
  loadTasks();
}, [filters]);
```

### Mutation Loading

```typescript
// Pseudocode
const [isCreating, setIsCreating] = useState(false);

async function createTask(data: CreateTaskInput) {
  setIsCreating(true);
  try {
    const newTask = await api.createTask(data);
    setTasks(prev => [newTask, ...prev]);
    clearForm();
  } finally {
    setIsCreating(false);
  }
}
```

## Retry Logic

### Automatic Retry

```typescript
// Pseudocode
async function apiRequestWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay(1000 * Math.pow(2, i)); // Exponential backoff
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Testing

### Mock API Client

```typescript
// Pseudocode
const mockApiClient: ApiClient = {
  getTasks: jest.fn(),
  getTask: jest.fn(),
  createTask: jest.fn(),
  updateTask: jest.fn(),
  deleteTask: jest.fn(),
  toggleComplete: jest.fn(),
};
```

### Test Scenarios

1. **Successful fetch**
   - Mock API response
   - Verify tasks displayed

2. **API error**
   - Mock 500 error
   - Verify error toast shown

3. **Unauthorized**
   - Mock 401 response
   - Verify redirect to sign-in

4. **Optimistic update**
   - Mock API delay
   - Verify immediate UI update
   - Verify revert on error

## Acceptance Criteria

- [ ] API client attaches JWT token to requests
- [ ] 401 responses redirect to sign-in
- [ ] Error messages display correctly
- [ ] Loading states show during operations
- [ ] Optimistic updates work for toggle
- [ ] Cache invalidation works
- [ ] Retry logic works for failures
- [ ] All endpoints integrated correctly
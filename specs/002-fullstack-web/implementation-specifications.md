# Phase II Implementation Specifications

## Overview

The Phase II implementation transforms the Phase I console-based todo app into a multi-user full-stack web application. This comprehensive specification outlines all requirements, architecture, and implementation guidance.

## Core Objectives

1. **Multi-user Support**: Implement user registration, authentication, and task isolation
2. **Persistent Storage**: Connect to cloud database (Neon PostgreSQL)
3. **Web Interface**: Build responsive Next.js frontend with Better Auth
4. **RESTful API**: Expose FastAPI backend with CRUD operations
5. **User Experience**: Provide efficient task management with search, filter, sort

## Technology Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Frontend | Next.js 16 | App Router | Modern, SEO-friendly, built-in routing |
| Frontend | TypeScript | 5.7 | Strong typing, better developer experience |
| Frontend | React 19 | Functional components | Industry standard |
| Frontend | Better Auth | ^1.2.0 | JWT-based auth, no shared secrets |
| Frontend | Tailwind CSS | ^4.0.0 | Utility-first styling, responsive |
| Backend | FastAPI | >=0.115.0 | Modern Python web framework |
| Backend | SQLModel | >=0.0.22 | Type-safe ORM |
| Backend | PostgreSQL | Neon Serverless | Cloud database, shared by auth |
| Backend | PyJWT | >=2.10.0 | JWT verification |
| Backend | Cryptography | >=44.0.0 | Crypto utilities |
| Database | Neon PostgreSQL | Serverless | Scalable cloud database |

## Architecture Overview

### Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEXT.JS 16 APP ROUTER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │     PUBLIC ROUTES       │  │      PROTECTED ROUTES       │  │
│  │                         │  │                             │  │
│  │ ┌─────────────────────┐ │  │ ┌─────────────────────────┐ │  │
│  │ │ /sign-in            │ │  │ │ /dashboard               │ │  │
│  │ │ /sign-up           │ │  │ │ (protected by auth-guard) │ │  │
│  │ └─────────────────────┘ │  │ └─────────────────────────┘ │  │
│  │                         │  │                             │  │
│  │ ┌─────────────────────┐ │  │ ┌─────────────────────────┐ │  │
│  │ │ /api/auth/[...all]  │ │  │ │ /api/tasks               │ │  │
│  │ └─────────────────────┘ │  │ └─────────────────────────┘ │  │
│  │                         │  │                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Backend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                          │
├─────────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │     AUTH MIDDLEWARE    │  │          REST API          │  │
│  │                         │  │                             │  │
│  │ ┌─────────────────────┐ │  │ ┌─────────────────────────┐ │  │
│  │ │ /api/tasks          │ │  │ │ GET /api/tasks            │ │  │
│  │ │ /api/tasks/:id      │ │  │ │ POST /api/tasks          │ │  │
│  │ │ /api/tasks/:id/complete │ │ │ PUT /api/tasks/:id        │ │  │
│  │ │ /api/tasks/:id      │ │  │ │ DELETE /api/tasks/:id    │ │  │
│  │ └─────────────────────┘ │  │ └─────────────────────────┘ │  │
│  │                         │  │                             │  │
│  │ ┌─────────────────────┐ │  │ ┌─────────────────────────┐ │  │
│  │ │     DATABASE        │ │  │ │    JWT VERIFICATION      │ │  │
│  │ │  POSTGRESQL + SQLMODEL│ │  │ │    (JWKS-based)          │ │  │
│  │ └─────────────────────┘ │  │ └─────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Implementation Guidelines

### 1. Authentication Flow

#### Better Auth Configuration

**Required Environment Variables:**
- `BETTER_AUTH_SECRET`: Secret for signing sessions
- `BETTER_AUTH_URL`: Base URL for auth callbacks
- `DATABASE_URL`: Neon PostgreSQL connection string for auth tables

**Implementation Steps:**

1. **Auth Server Setup**
   ```typescript
   import { betterAuth } from "better-auth";
   import { jwt } from "better-auth/plugins";

   export const auth = betterAuth({
     database: {
       provider: "postgresql",
       url: process.env.DATABASE_URL,
     },
     emailAndPassword: {
       enabled: true,
     },
     plugins: [
       jwt({
         jwks: {
           url: process.env.JWKS_URL || "http://localhost:3000/api/auth/jwks",
         },
       }),
     ],
     secret: process.env.BETTER_AUTH_SECRET,
     baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
   });
   ```

2. **Auth Client Setup**
   ```typescript
   import { createAuthClient } from "better-auth/react";

   export const authClient = createAuthClient({
     baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
   });
   ```

3. **Auth Middleware**
   - Use `PyJWKClient` to fetch JWKS from Better Auth
   - Verify EdDSA tokens with public keys from JWKS
   - Extract `user_id` from JWT payload
   - Attach to FastAPI request state

### 2. Database Design

#### Task Model
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(10) DEFAULT 'medium',
    category VARCHAR(10),
    due_date DATE,
    recurrence VARCHAR(10),
    due_time TIME,
    reminder_minutes INTEGER,
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_id_status ON tasks(user_id, is_completed);
CREATE INDEX idx_tasks_user_id_priority ON tasks(user_id, priority);
CREATE INDEX idx_tasks_user_id_category ON tasks(user_id, category);
```

#### Better Auth Tables
Better Auth automatically creates and manages:
- `users` table (ID, email, name, etc.)
- `session` table (session management)
- `account` table (OAuth accounts)
- `verification` table (email verification)

### 3. API Endpoints

#### Common Headers
```http
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

#### GET /api/tasks
**List all tasks for authenticated user**

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| status | string | No | "all" | Filter: "all", "active", "completed" |
| priority | string | No | null | Filter: "high", "medium", "low" |
| category | string | No | null | Filter: "work", "home", "personal", "health", "other" |
| search | string | No | null | Search title and description |
| sort_by | string | No | "created_at" | Sort field: "created_at", "due_date", "title", "priority" |
| sort_order | string | No | "desc" | Sort direction: "asc", "desc" |

**Response 200:**
```json
[
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
]
```

**Response 401:**
```json
{"detail": "Not authenticated"}
```

#### POST /api/tasks
**Create a new task**

**Request Body:**
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

**Response 201:** Created task object
**Response 401:** `{"detail": "Not authenticated"}`
**Response 422:** Validation errors

#### PUT /api/tasks/{task_id}
**Update a task**

**Response 200:** Updated task object
**Response 401:** `{"detail": "Not authenticated"}`
**Response 404:** `{"detail": "Task not found"}`

#### DELETE /api/tasks/{task_id}
**Delete a task**

**Response 204:** No content
**Response 401:** `{"detail": "Not authenticated"}`

#### PATCH /api/tasks/{task_id}/complete
**Toggle task completion**

**Response 200:** Updated task object (with new `is_completed` value)
**Response 401:** `{"detail": "Not authenticated"}`

## Frontend Implementation

### Component Architecture

#### Root Layout
- **Purpose**: HTML structure, metadata, Tailwind setup, providers
- **Location**: `frontend/src/app/layout.tsx`
- **Key Features**:
  - SEO optimization (metadata)
  - Tailwind CSS injection
  - Global error boundary
  - Theme providers if needed

#### Public Pages
- **Sign-in Page**: Email/password authentication
- **Sign-up Page**: User registration
- **Landing Page**: Redirect based on auth status

#### Protected Pages
- **Dashboard Page**: Main task management interface
- **Auth Guard**: Protect routes from unauthenticated access

#### UI Components
- **Task List**: Container for task cards with loading states
- **Task Card**: Individual task display with actions (edit, delete, toggle)
- **Task Form**: Create/edit task with validation
- **Task Filters**: Search, status, priority, category filters

### State Management Strategy

#### Auth State
- Better Auth session management
- Automatic token refresh
- Redirect flows

#### Task State
- Server-fetched data (no client-side caching initially)
- Optimistic updates for better UX
- Loading/error states

#### Filter State
- URL-based filters for shareability
- Local state for UI controls
- Debounced search input

## Testing Strategy

### Unit Tests
- **Backend**: Jest/Jest-based tests for services and repositories
- **Frontend**: Vitest/Jest-based tests for hooks and utilities

### Integration Tests
- **Backend**: Test API endpoints with actual database
- **Frontend**: Test component interactions

### E2E Tests
- **Backend**: FastAPI test client
- **Frontend**: Playwright/Cypress (future)

## Performance Considerations

### Backend Optimization
- Database connection pooling with `NullPool` for Neon compatibility
- JWT verification caching
- Request/response serialization efficiency

### Frontend Optimization
- Code splitting with Next.js App Router
- Image optimization
- Lazy loading of heavy components
- Client-side caching strategies

## Security Measures

### Authentication & Authorization
- JWKS-based JWT verification (no shared secrets)
- Request-scoped user ID from JWT
- Input validation server-side
- Rate limiting (Better Auth built-in)

### Data Protection
- All endpoints require authentication
- User isolation enforcement (only user's tasks)
- Input sanitization
- Error handling without information leakage

## Deployment Preparation

### Environment Variables

#### Backend (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection (pooled) | `postgresql+psycopg://...` |
| JWKS_URL | Better Auth JWKS endpoint | `http://localhost:3000/api/auth/jwks` |
| FRONTEND_URL | Frontend origin for CORS | `http://localhost:3000` |

#### Frontend (.env.local)
| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API base URL | `http://localhost:8000` |
| DATABASE_URL | Neon PostgreSQL connection (direct) | `postgresql://...` |
| BETTER_AUTH_SECRET | Secret for signing sessions | Random 32+ char string |
| BETTER_AUTH_URL | Base URL for auth callbacks | `http://localhost:3000` |

### Rollback Strategy

1. **Database Migration**
   - Version-controlled schema changes
   - Backup strategies
   - Migration testing

2. **Feature Flags**
   - Gradual rollout with feature flags
   - Quick rollback capability

3. **Monitoring & Alerting**
   - Health checks
   - Performance metrics
   - Error tracking

## Success Criteria

### Functional Requirements
- [ ] User registration and sign-in
- [ ] Task CRUD operations
- [ ] Task completion toggle with recurrence
- [ ] Search, filter, sort functionality
- [ ] Responsive web interface
- [ ] JWT-based authentication
- [ ] User isolation enforcement

### Non-Functional Requirements
- [ ] Performance: <2s task list load for 500 tasks
- [ ] Security: No hardcoded secrets, proper validation
- [ ] Reliability: Error handling and logging
- [ ] Usability: Accessible, responsive design
- [ ] Maintainability: Clean code, documentation

## Implementation Timeline

### Week 1: Setup & Foundations
- Monorepo structure establishment
- Environment configuration
- Database setup
- Auth integration

### Week 2: Core Functionality
- API endpoints implementation
- Task CRUD implementation
- Authentication flow

### Week 3: User Experience
- Frontend components
- Responsive design
- Search/filter/sort

### Week 4: Testing & Polish
- Test suite creation
- Bug fixes
- Documentation completion

## Risk Assessment & Mitigation

### High Risk Areas
1. **Database Integration**: Connection pool conflicts with Neon
   - **Mitigation**: Use `NullPool`, proper error handling

2. **Authentication Complexity**: JWT verification across services
   - **Mitigation**: Use JWKS, no shared secrets, thorough testing

3. **Frontend Performance**: Large task lists
   - **Mitigation**: Lazy loading, pagination, efficient rendering

### Medium Risk Areas
1. **Team Coordination**: Multiple components
   - **Mitigation**: Clear interfaces, well-defined APIs

2. **Time Constraints**: Full feature set
   - **Mitigation**: Prioritize MVP, incremental delivery

### Low Risk Areas
1. **Styling**: Visual consistency
   - **Mitigation**: Tailwind CSS utilities, design system

2. **Testing**: Coverage and maintenance
   - **Mitigation**: Automated test suites, CI integration

## Quality Gates

### Code Quality
- TypeScript strict mode
- Linting and formatting compliance
- Unit test coverage > 80%
- Code review process

### Security Review
- Secret management verification
- Authentication flow testing
- Input validation verification
- Error handling review

### Performance Validation
- Load time benchmarks
- Memory usage analysis
- Database query performance
- User experience testing

## Conclusion

This Phase II implementation provides a robust, secure, and scalable foundation for the todo application. By leveraging modern web technologies and following best practices, we create an application that:

- Supports multi-user access with proper isolation
- Provides efficient task management capabilities
- Delivers a responsive web experience
- Implements proper authentication and security
- Is maintainable and extensible for future phases

The specifications enable teams to implement incrementally while maintaining high quality and adhering to industry standards.
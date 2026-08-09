# Frontend Architecture Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification defines the Next.js 16 frontend architecture for the Phase II full-stack todo application.

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | Next.js (App Router) | 16+ |
| Language | TypeScript | 5.7+ |
| UI Library | React | 19+ |
| Styling | Tailwind CSS | 4+ |
| Auth | Better Auth | 1.2+ |
| Linting | Biome | 1.9+ |

## Project Structure

```
frontend/src/
├── app/
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Landing/redirect page
│   ├── (auth)/
│   │   ├── sign-in/page.tsx    # Sign-in page
│   │   └── sign-up/page.tsx    # Sign-up page
│   ├── dashboard/
│   │   └── page.tsx            # Main dashboard (protected)
│   └── api/
│       └── auth/
│           └── [...all]/route.ts  # Better Auth catch-all
├── components/
│   ├── ui/                     # Shared UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   ├── dialog.tsx
│   │   └── select.tsx
│   ├── auth/
│   │   ├── auth-guard.tsx      # Protected route wrapper
│   │   ├── sign-in-form.tsx    # Sign-in form component
│   │   └── sign-up-form.tsx    # Sign-up form component
│   └── tasks/
│       ├── task-list.tsx       # Task list container
│       ├── task-card.tsx       # Individual task display
│       ├── task-form.tsx       # Create/edit task form
│       ├── task-filters.tsx    # Search/filter controls
│       └── task-toggle.tsx     # Completion toggle
├── lib/
│   ├── auth.ts                 # Better Auth server config
│   ├── auth-client.ts          # Better Auth client config
│   ├── api.ts                  # Backend API client
│   └── utils.ts                # Utility functions
└── types/
    └── task.ts                 # TypeScript types
```

## Component Architecture

### Client vs Server Components

| Component | Type | Reason |
|-----------|------|--------|
| layout.tsx | Server | Metadata, providers |
| page.tsx (landing) | Server | Redirect logic |
| sign-in/page.tsx | Client | Form interaction |
| sign-up/page.tsx | Client | Form interaction |
| dashboard/page.tsx | Client | State management |
| task-list.tsx | Client | Dynamic updates |
| task-card.tsx | Client | User interactions |
| task-form.tsx | Client | Form handling |
| task-filters.tsx | Client | Filter state |
| auth-guard.tsx | Client | Session check |

### State Management

- **Server State**: Fetched via API client, cached in React state
- **Auth State**: Managed by Better Auth session
- **Form State**: Local component state (useState)
- **URL State**: Query params for filters/sort

### Data Flow

```
User Action → Component → API Client → Backend API → Database
    ↓
UI Update ← State Change ← Response ← JSON ← Query Result
```

## Routing Strategy

### Public Routes
- `/` - Landing page (redirects based on auth)
- `/sign-in` - Sign-in page
- `/sign-up` - Sign-up page

### Protected Routes
- `/dashboard` - Main task dashboard

### API Routes
- `/api/auth/[...all]` - Better Auth endpoints

## Error Handling

### Client-Side Errors
- Network errors: Show toast notification
- Validation errors: Inline form errors
- Auth errors: Redirect to sign-in

### Error Boundaries
- Global error boundary in layout.tsx
- Component-level error boundaries for complex components

## Performance Considerations

- **Code Splitting**: Automatic with App Router
- **Image Optimization**: Use Next.js Image component
- **Font Optimization**: Use next/font
- **Caching**: SWR pattern for data fetching

## Security

- **Auth Tokens**: HttpOnly cookies (Better Auth default)
- **API Calls**: Bearer token in Authorization header
- **XSS Prevention**: React's built-in escaping
- **CSRF**: SameSite cookies

## Testing Strategy

- **Unit Tests**: Vitest for utilities and hooks
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright (future)

## Acceptance Criteria

- [ ] All pages render without errors
- [ ] Auth flow works end-to-end
- [ ] Responsive on all screen sizes
- [ ] No console errors in production
- [ ] Lighthouse score > 90
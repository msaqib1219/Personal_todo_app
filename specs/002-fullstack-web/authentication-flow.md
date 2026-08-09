# Authentication Flow Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification defines the authentication flow for the Phase II full-stack todo application using Better Auth.

## Authentication Strategy

### Better Auth Configuration

Better Auth handles all authentication logic on the frontend. The backend verifies JWT tokens issued by Better Auth.

### JWT Flow

```
1. User signs up/in → Better Auth creates session
2. Better Auth issues JWT token (EdDSA/Ed25519)
3. Frontend stores token in HttpOnly cookie
4. Frontend sends JWT in Authorization header to backend
5. Backend verifies JWT via JWKS endpoint
6. Backend extracts user_id from token payload
```

## Pages

### Sign-Up Page (`/sign-up`)

**Purpose**: Allow new users to create an account

**Form Fields**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | text | Yes | Min 2 chars |
| email | email | Yes | Valid email format |
| password | password | Yes | Min 8 chars |
| confirmPassword | password | Yes | Must match password |

**Behavior**:
- On success: Redirect to `/dashboard`
- On error: Show error message below form
- Duplicate email: Show "Email already registered"

**UI Elements**:
- Card container centered on page
- Form with inputs and submit button
- Link to sign-in page
- Loading state during submission

### Sign-In Page (`/sign-in`)

**Purpose**: Allow existing users to sign in

**Form Fields**:
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| email | email | Yes | Valid email format |
| password | password | Yes | Not empty |

**Behavior**:
- On success: Redirect to `/dashboard`
- On error: Show "Invalid credentials"
- Remember me: Optional checkbox (Better Auth handles)

**UI Elements**:
- Card container centered on page
- Form with inputs and submit button
- Link to sign-up page
- Loading state during submission

## Components

### Auth Guard (`auth-guard.tsx`)

**Purpose**: Protect routes from unauthenticated access

**Props**:
```typescript
interface AuthGuardProps {
  children: React.ReactNode;
}
```

**Behavior**:
- Check session on mount
- If loading: Show spinner
- If authenticated: Render children
- If not authenticated: Redirect to `/sign-in`

**Implementation**:
```tsx
// Pseudocode
const session = useSession();
if (session.isLoading) return <Spinner />;
if (!session.data) {
  redirect('/sign-in');
  return null;
}
return <>{children}</>;
```

### Sign-In Form (`sign-in-form.tsx`)

**Purpose**: Reusable sign-in form component

**Props**:
```typescript
interface SignInFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}
```

**Features**:
- Email input with validation
- Password input with show/hide toggle
- Submit button with loading state
- Error message display
- Link to sign-up

### Sign-Up Form (`sign-up-form.tsx`)

**Purpose**: Reusable sign-up form component

**Props**:
```typescript
interface SignUpFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}
```

**Features**:
- Name input
- Email input with validation
- Password input with strength indicator
- Confirm password input
- Submit button with loading state
- Error message display
- Link to sign-in

## API Integration

### Better Auth Client (`auth-client.ts`)

```typescript
// Pseudocode
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### Better Auth Server (`auth.ts`)

```typescript
// Pseudocode
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
        url: process.env.JWKS_URL || "/api/auth/jwks",
      },
    }),
  ],
});
```

### API Route Handler (`[...all]/route.ts`)

```typescript
// Pseudocode
import { auth } from "@/lib/auth";

const handler = auth.handler;
export { handler as GET, handler as POST };
```

## Session Management

### Session Structure

```typescript
interface Session {
  user: {
    id: string;
    name: string;
    email: string;
  };
  session: {
    id: string;
    expiresAt: Date;
  };
}
```

### Session Hooks

| Hook | Purpose | Returns |
|------|---------|---------|
| `useSession()` | Get current session | `{ data, isLoading, error }` |

### Session Persistence

- Better Auth uses HttpOnly cookies by default
- Session expires after 7 days (configurable)
- Automatic refresh on activity

## Error Handling

### Error Types

| Error | Message | Action |
|-------|---------|--------|
| Invalid credentials | "Invalid email or password" | Show below form |
| Email exists | "Email already registered" | Show below form |
| Weak password | "Password must be at least 8 characters" | Show below form |
| Network error | "Connection failed. Please try again." | Show toast |
| Token expired | "Session expired. Please sign in again." | Redirect to /sign-in |

### Error Display

- Form errors: Below respective input field
- General errors: Alert banner above form
- Network errors: Toast notification

## Security Considerations

### Password Requirements

- Minimum 8 characters
- No maximum length (hashed before storage)
- Stored as bcrypt hash (Better Auth default)

### Token Security

- JWT signed with EdDSA (Ed25519)
- HttpOnly cookies prevent XSS
- SameSite=Lax prevents CSRF
- Secure flag in production

### Rate Limiting

- Better Auth has built-in rate limiting
- 5 failed attempts per minute per IP
- 10 sign-ups per hour per IP

## Testing Scenarios

### Sign-Up Flow

1. **New user registration**
   - Enter valid details
   - Submit form
   - Verify redirect to dashboard
   - Verify session exists

2. **Duplicate email**
   - Enter existing email
   - Submit form
   - Verify error message shown
   - Verify no redirect

3. **Password mismatch**
   - Enter different passwords
   - Submit form
   - Verify error message shown

### Sign-In Flow

1. **Valid credentials**
   - Enter correct email/password
   - Submit form
   - Verify redirect to dashboard
   - Verify session exists

2. **Invalid credentials**
   - Enter wrong password
   - Submit form
   - Verify error message shown
   - Verify no redirect

3. **Non-existent email**
   - Enter unregistered email
   - Submit form
   - Verify error message shown

### Session Flow

1. **Authenticated access**
   - Sign in
   - Navigate to /dashboard
   - Verify page loads

2. **Unauthenticated access**
   - Clear session
   - Navigate to /dashboard
   - Verify redirect to /sign-in

3. **Token expiry**
   - Wait for token to expire (or mock)
   - Make API call
   - Verify redirect to /sign-in

## Acceptance Criteria

- [ ] Sign-up form validates all fields
- [ ] Sign-in form validates email/password
- [ ] Auth guard protects dashboard
- [ ] Redirects work correctly
- [ ] Error messages display properly
- [ ] Loading states show during submission
- [ ] Session persists across page reloads
- [ ] Sign out clears session
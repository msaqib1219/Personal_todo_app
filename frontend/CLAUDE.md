# Frontend Development Guide

## Run Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Lint and format
npm run lint
npm run format
```

## Key File Locations

- `src/app/layout.tsx` — Root layout
- `src/app/page.tsx` — Landing/redirect page
- `src/app/(auth)/sign-in/page.tsx` — Sign-in page
- `src/app/(auth)/sign-up/page.tsx` — Sign-up page
- `src/app/dashboard/page.tsx` — Main task dashboard (protected)
- `src/app/api/auth/[...all]/route.ts` — Better Auth API route
- `src/components/` — Reusable UI components
- `src/lib/auth.ts` — Better Auth server instance
- `src/lib/auth-client.ts` — Better Auth client instance
- `src/lib/api.ts` — Backend API client (fetch wrapper)
- `src/types/task.ts` — Task TypeScript types

## Conventions

- **Commits**: Conventional Commits format — `type(scope): description`
  - Examples: `feat(auth): add sign-up page`, `fix(tasks): handle empty list`
- **Code Quality**: All code must pass Biome lint and format checks
- **TypeScript**: Strict mode, no `any` types unless unavoidable
- **Components**: Functional components with hooks
- **Styling**: Tailwind CSS utility classes, responsive-first

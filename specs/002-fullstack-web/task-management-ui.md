# Task Management UI Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification defines the task management user interface for the Phase II full-stack todo application.

## Dashboard Layout

### Page Structure

```
┌─────────────────────────────────────────────────────┐
│ Header (Logo, User Menu, Sign Out)                  │
├─────────────────────────────────────────────────────┤
│ Task Filters (Search, Status, Priority, Category)   │
├─────────────────────────────────────────────────────┤
│ Task Form (Create New Task)                         │
├─────────────────────────────────────────────────────┤
│ Task List                                           │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Task Card 1                                     │ │
│ ├─────────────────────────────────────────────────┤ │
│ │ Task Card 2                                     │ │
│ ├─────────────────────────────────────────────────┤ │
│ │ Task Card 3                                     │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 640px | Single column, stacked |
| Tablet | 640-1024px | Two columns |
| Desktop | > 1024px | Full width with max-width |

## Components

### Task List (`task-list.tsx`)

**Purpose**: Display and manage list of tasks

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: number, data: Partial<Task>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onToggle: (id: number) => Promise<void>;
  isLoading: boolean;
}
```

**Features**:
- Renders list of TaskCard components
- Shows empty state when no tasks
- Loading skeleton during fetch
- Sort indicator headers

**Empty State**:
```
┌─────────────────────────────────────┐
│                                     │
│         📝 No tasks yet            │
│                                     │
│    Create your first task above    │
│                                     │
└─────────────────────────────────────┘
```

### Task Card (`task-card.tsx`)

**Purpose**: Display individual task with actions

**Props**:
```typescript
interface TaskCardProps {
  task: Task;
  onUpdate: (data: Partial<Task>) => Promise<void>;
  onDelete: () => Promise<void>;
  onToggle: () => Promise<void>;
}
```

**Layout**:
```
┌─────────────────────────────────────────────────────┐
│ ☐ Buy groceries                    [High] [Home]   │
│ Description: Milk, eggs, bread                      │
│ Due: 2026-03-05 14:30  |  Recurring: Weekly         │
│                                 [Edit] [Delete]     │
└─────────────────────────────────────────────────────┘
```

**Elements**:
- Checkbox for completion toggle
- Title (strikethrough when completed)
- Priority badge (color-coded)
- Category badge
- Description (truncated)
- Due date/time display
- Recurrence indicator
- Action buttons (Edit, Delete)

**States**:
| State | Visual |
|-------|--------|
| Incomplete | Normal text, unchecked box |
| Completed | Strikethrough text, checked box |
| Overdue | Red due date text |
| Recurring | Recurrence icon |

### Task Form (`task-form.tsx`)

**Purpose**: Create or edit tasks

**Props**:
```typescript
interface TaskFormProps {
  task?: Task;  // If provided, edit mode
  onSubmit: (data: CreateTaskInput | UpdateTaskInput) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
}
```

**Form Fields**:

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| title | text | Yes | - | 1-500 chars |
| description | textarea | No | - | Max 2000 chars |
| priority | select | No | medium | high/medium/low |
| category | select | No | - | work/home/personal/health/other |
| due_date | date | No | - | Not in past |
| due_time | time | No | - | HH:MM format |
| recurrence | select | No | - | daily/weekly/monthly/yearly |
| reminder_minutes | number | No | - | Non-negative |

**Layout**:
```
┌─────────────────────────────────────────────────────┐
│ Create New Task                                      │
├─────────────────────────────────────────────────────┤
│ Title *                                               │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                       │
│ Description                                           │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                                 │ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                       │
│ ┌──────────────┐  ┌──────────────┐                   │
│ │ Priority ▼   │  │ Category ▼   │                   │
│ └──────────────┘  └──────────────┘                   │
│                                                       │
│ ┌──────────────┐  ┌──────────────┐                   │
│ │ Due Date     │  │ Due Time     │                   │
│ └──────────────┘  └──────────────┘                   │
│                                                       │
│ ┌──────────────┐  ┌──────────────┐                   │
│ │ Recurrence ▼ │  │ Reminder(min)│                   │
│ └──────────────┘  └──────────────┘                   │
│                                                       │
│              [Cancel]  [Create Task]                  │
└─────────────────────────────────────────────────────┘
```

**Behavior**:
- Collapsible form (click to expand)
- Validation on submit
- Clear form on successful creation
- Show loading state during submission
- Edit mode: Pre-fill with task data

### Task Filters (`task-filters.tsx`)

**Purpose**: Filter and search tasks

**Props**:
```typescript
interface TaskFiltersProps {
  filters: TaskFilters;
  onFilterChange: (filters: Partial<TaskFilters>) => void;
  totalCount: number;
  filteredCount: number;
}
```

**Filter Controls**:

| Filter | Type | Options | Default |
|--------|------|---------|---------|
| search | text | - | - |
| status | select | all/active/completed | all |
| priority | select | all/high/medium/low | all |
| category | select | all/work/home/personal/health/other | all |
| sort_by | select | created_at/due_date/title/priority | created_at |
| sort_order | select | asc/desc | desc |

**Layout**:
```
┌─────────────────────────────────────────────────────┐
│ 🔍 Search tasks...                    [12 tasks]    │
├─────────────────────────────────────────────────────┤
│ Status: [All ▼]  Priority: [All ▼]  Category: [All ▼]│
│ Sort: [Date ▼]   Order: [Newest ▼]                  │
└─────────────────────────────────────────────────────┘
```

**Behavior**:
- Debounced search (300ms)
- Filter changes update URL query params
- Clear filters button
- Task count display

### Task Toggle (`task-toggle.tsx`)

**Purpose**: Toggle task completion status

**Props**:
```typescript
interface TaskToggleProps {
  isCompleted: boolean;
  onToggle: () => Promise<void>;
  disabled?: boolean;
}
```

**States**:
| State | Visual | Behavior |
|-------|--------|----------|
| Incomplete | ☐ Empty checkbox | Click to complete |
| Completed | ☑ Checked checkbox | Click to mark incomplete |
| Loading | ⟳ Spinner | Disabled during toggle |

**Behavior**:
- Optimistic update (immediate visual反馈)
- Revert on API error
- Show loading state during toggle

## Task Data Model

### Task Type

```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  priority: 'high' | 'medium' | 'low';
  category?: 'work' | 'home' | 'personal' | 'health' | 'other';
  due_date?: string;  // YYYY-MM-DD
  recurrence?: 'daily' | 'weekly' | 'monthly' | 'yearly';
  due_time?: string;  // HH:MM
  reminder_minutes?: number;
  reminder_sent: boolean;
  created_at: string;  // ISO timestamp
  updated_at: string;  // ISO timestamp
}
```

### Create Task Input

```typescript
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
  category?: 'work' | 'home' | 'personal' | 'health' | 'other';
  due_date?: string;
  due_time?: string;
  recurrence?: 'daily' | 'weekly' | 'monthly' | 'yearly';
  reminder_minutes?: number;
}
```

### Update Task Input

```typescript
type UpdateTaskInput = Partial<CreateTaskInput>;
```

## User Interactions

### Create Task

1. Click "Create Task" button or expand form
2. Fill in required field (title)
3. Optionally fill other fields
4. Click "Create" or press Enter
5. Show loading state
6. On success: Clear form, add task to list
7. On error: Show error message

### Edit Task

1. Click "Edit" button on task card
2. Form expands with task data pre-filled
3. Modify fields
4. Click "Save" or press Enter
5. Show loading state
6. On success: Update task in list, collapse form
7. On error: Show error message

### Delete Task

1. Click "Delete" button on task card
2. Show confirmation dialog
3. Confirm deletion
4. Show loading state
5. On success: Remove task from list
6. On error: Show error message

### Toggle Completion

1. Click checkbox on task card
2. Optimistic update (immediate visual change)
3. API call in background
4. On error: Revert visual change, show error

### Search/Filter

1. Type in search box
2. Debounce 300ms
3. Update URL query params
4. Fetch filtered tasks
5. Update task list

## Empty States

### No Tasks

```
┌─────────────────────────────────────┐
│                                     │
│         📝 No tasks yet            │
│                                     │
│    Create your first task above    │
│                                     │
└─────────────────────────────────────┘
```

### No Search Results

```
┌─────────────────────────────────────┐
│                                     │
│         🔍 No results found        │
│                                     │
│    Try different search terms      │
│                                     │
└─────────────────────────────────────┘
```

### Loading State

```
┌─────────────────────────────────────┐
│ ┌─────────────────────────────────┐ │
│ │ ████████████████████████████████│ │
│ │ ████████████████████            │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ ████████████████████████████████│ │
│ │ ████████████████████            │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Accessibility

### Keyboard Navigation

- Tab through all interactive elements
- Enter/Space to toggle checkbox
- Escape to close dialogs
- Arrow keys in selects

### Screen Reader

- ARIA labels on all buttons
- Role attributes on interactive elements
- Live regions for dynamic updates
- Form field associations

### Visual

- Focus indicators on all interactive elements
- Color contrast ratio > 4.5:1
- Don't rely on color alone for information

## Performance

### Optimizations

- Virtual scrolling for large lists (future)
- Debounced search input
- Optimistic updates for toggles
- Lazy loading of form components
- Image lazy loading (if applicable)

### Loading States

- Skeleton screens for initial load
- Spinner for individual actions
- Disabled state during mutations

## Acceptance Criteria

- [ ] Task list displays all user tasks
- [ ] Create task form works correctly
- [ ] Edit task pre-fills form
- [ ] Delete task shows confirmation
- [ ] Toggle completion works immediately
- [ ] Search filters tasks in real-time
- [ ] All filters work correctly
- [ ] Empty states display properly
- [ ] Loading states show during operations
- [ ] Error messages display on failures
- [ ] Responsive on all screen sizes
- [ ] Keyboard navigation works
- [ ] Screen reader accessible
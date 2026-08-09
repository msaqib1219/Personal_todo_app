# Responsive Design Specification

**Feature**: 002-fullstack-web  
**Date**: 2026-07-18  
**Status**: Draft

## Overview

This specification defines the responsive design requirements for the Phase II full-stack todo application.

## Design Principles

### Mobile-First Approach

- Design for smallest screen first
- Add complexity for larger screens
- Touch-friendly on mobile
- Pointer-friendly on desktop

### Breakpoints

| Name | Width | Target |
|------|-------|--------|
| xs | 0-639px | Mobile phones |
| sm | 640-767px | Large phones |
| md | 768-1023px | Tablets |
| lg | 1024-1279px | Small desktops |
| xl | 1280px+ | Large desktops |

## Layout System

### Grid Structure

```css
/* Mobile: Single column */
.container {
  padding: 16px;
  max-width: 100%;
}

/* Tablet: Two columns */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 768px;
    margin: 0 auto;
  }
}

/* Desktop: Max width container */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1024px;
  }
}
```

### Dashboard Layout

#### Mobile (< 640px)

```
┌─────────────────────┐
│ Header              │
├─────────────────────┤
│ Search              │
├─────────────────────┤
│ Filters (Stacked)   │
├─────────────────────┤
│ Create Task Button  │
├─────────────────────┤
│ Task Card           │
├─────────────────────┤
│ Task Card           │
├─────────────────────┤
│ Task Card           │
└─────────────────────┘
```

#### Tablet (640-1023px)

```
┌───────────────────────────────────────┐
│ Header                                │
├───────────────────────────────────────┤
│ Search                                │
├───────────────────────────────────────┤
│ Filters (Inline)                      │
├───────────────────────────────────────┤
│ Create Task Button                    │
├───────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────┐     │
│ │ Task Card   │  │ Task Card   │     │
│ └─────────────┘  └─────────────┘     │
│ ┌─────────────┐  ┌─────────────┐     │
│ │ Task Card   │  │ Task Card   │     │
│ └─────────────┘  └─────────────┘     │
└───────────────────────────────────────┘
```

#### Desktop (1024px+)

```
┌─────────────────────────────────────────────────────┐
│ Header                                              │
├─────────────────────────────────────────────────────┤
│ Search                              [12 tasks]      │
├─────────────────────────────────────────────────────┤
│ Filters: [Status] [Priority] [Category] [Sort]      │
├─────────────────────────────────────────────────────┤
│ Create Task Button                                  │
├─────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│ │ Task Card   │  │ Task Card   │  │ Task Card   │ │
│ └─────────────┘  └─────────────┘  └─────────────┘ │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│ │ Task Card   │  │ Task Card   │  │ Task Card   │ │
│ └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Component Responsive Behavior

### Header

| Breakpoint | Behavior |
|------------|----------|
| Mobile | Logo + hamburger menu |
| Tablet | Logo + user menu |
| Desktop | Logo + full nav + user menu |

### Task Card

| Breakpoint | Layout |
|------------|--------|
| Mobile | Full width, stacked content |
| Tablet | Half width grid item |
| Desktop | Third width grid item |

#### Mobile Task Card

```
┌─────────────────────────────────────┐
│ ☐ Buy groceries          [High]    │
│ Description: Milk, eggs, bread      │
│ Due: 2026-03-05 14:30              │
│ Recurring: Weekly                   │
│                   [Edit] [Delete]  │
└─────────────────────────────────────┘
```

#### Desktop Task Card

```
┌─────────────────────────────────────┐
│ ☐ Buy groceries    [High] [Home]   │
│ Description: Milk, eggs, bread      │
│ Due: 2026-03-05 14:30 | Weekly     │
│                   [Edit] [Delete]  │
└─────────────────────────────────────┘
```

### Task Form

| Breakpoint | Layout |
|------------|--------|
| Mobile | Full width, stacked fields |
| Tablet | Two columns for fields |
| Desktop | Full width with inline fields |

#### Mobile Task Form

```
┌─────────────────────────────────────┐
│ Title *                             │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ Description                         │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ Priority                            │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ Category                            │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ Due Date                            │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ Due Time                            │
│ ┌─────────────────────────────────┐ │
│ └─────────────────────────────────┘ │
│ [Cancel]  [Create]                  │
└─────────────────────────────────────┘
```

#### Desktop Task Form

```
┌─────────────────────────────────────────────────────┐
│ Title *                                               │
│ ┌─────────────────────────────────────────────────┐ │
│ └─────────────────────────────────────────────────┘ │
│ Description                                           │
│ ┌─────────────────────────────────────────────────┐ │
│ └─────────────────────────────────────────────────┘ │
│ ┌──────────────┐  ┌──────────────┐                   │
│ │ Priority     │  │ Category     │                   │
│ └──────────────┘  └──────────────┘                   │
│ ┌──────────────┐  ┌──────────────┐                   │
│ │ Due Date     │  │ Due Time     │                   │
│ └──────────────┘  └──────────────┘                   │
│ [Cancel]  [Create]                                    │
└─────────────────────────────────────────────────────┘
```

### Task Filters

| Breakpoint | Layout |
|------------|--------|
| Mobile | Stacked vertically |
| Tablet | Inline with wrapping |
| Desktop | Full inline row |

#### Mobile Task Filters

```
┌─────────────────────────────────────┐
│ 🔍 Search tasks...                 │
├─────────────────────────────────────┤
│ Status: [All ▼]                    │
├─────────────────────────────────────┤
│ Priority: [All ▼]                  │
├─────────────────────────────────────┤
│ Category: [All ▼]                  │
├─────────────────────────────────────┤
│ Sort: [Date ▼]  Order: [Newest ▼] │
└─────────────────────────────────────┘
```

#### Desktop Task Filters

```
┌─────────────────────────────────────────────────────┐
│ 🔍 Search tasks...    Status [All ▼] Priority [All ▼]│
│ Category [All ▼] Sort [Date ▼] Order [Newest ▼]    │
└─────────────────────────────────────────────────────┘
```

## Touch Interactions

### Mobile Touch Targets

- Minimum touch target: 44x44px
- Button height: 48px
- Checkbox size: 24x24px
- Input height: 48px

### Touch Gestures

| Gesture | Action |
|---------|--------|
| Tap | Select/activate |
| Long press | Show context menu (future) |
| Swipe left | Delete task (future) |
| Swipe right | Complete task (future) |

## Typography

### Font Sizes

| Element | Mobile | Tablet | Desktop |
|---------|--------|--------|---------|
| H1 | 24px | 30px | 36px |
| H2 | 20px | 24px | 30px |
| H3 | 18px | 20px | 24px |
| Body | 14px | 16px | 16px |
| Small | 12px | 14px | 14px |

### Line Heights

- Headings: 1.3
- Body: 1.5
- Small: 1.4

## Spacing

### Mobile Spacing

- Page padding: 16px
- Component gap: 12px
- Element gap: 8px

### Tablet Spacing

- Page padding: 24px
- Component gap: 16px
- Element gap: 12px

### Desktop Spacing

- Page padding: 32px
- Component gap: 24px
- Element gap: 16px

## Colors

### Priority Colors

| Priority | Color | Background |
|----------|-------|------------|
| High | #EF4444 | #FEE2E2 |
| Medium | #F59E0B | #FEF3C7 |
| Low | #10B981 | #D1FAE5 |

### Category Colors

| Category | Color |
|----------|-------|
| Work | #3B82F6 |
| Home | #8B5CF6 |
| Personal | #EC4899 |
| Health | #10B981 |
| Other | #6B7280 |

## Animations

### Transitions

- Button hover: 150ms ease
- Card hover: 200ms ease
- Form expand: 300ms ease
- Page transitions: 200ms ease

### Loading Animations

- Spinner: 1s linear infinite
- Skeleton pulse: 1.5s ease-in-out infinite

## Accessibility

### Focus Indicators

- Visible focus ring on all interactive elements
- 2px solid blue outline
- 2px offset

### Screen Reader

- ARIA labels on all buttons
- Role attributes on interactive elements
- Live regions for dynamic updates

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Testing

### Device Testing

| Device | Width | Height |
|--------|-------|--------|
| iPhone SE | 375px | 667px |
| iPhone 14 | 390px | 844px |
| iPad | 768px | 1024px |
| iPad Pro | 1024px | 1366px |
| Desktop | 1920px | 1080px |

### Browser Testing

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Acceptance Criteria

- [ ] All pages responsive on mobile (375px)
- [ ] All pages responsive on tablet (768px)
- [ ] All pages responsive on desktop (1280px)
- [ ] Touch targets minimum 44x44px
- [ ] Text readable without zoom
- [ ] No horizontal scroll on mobile
- [ ] Forms usable on mobile
- [ ] Buttons tap-friendly on mobile
- [ ] Keyboard navigation works
- [ ] Screen reader accessible
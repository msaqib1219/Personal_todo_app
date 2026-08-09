export type Priority = 'high' | 'medium' | 'low';

export type Category = 'work' | 'home' | 'personal' | 'health' | 'other';

export type Recurrence = 'daily' | 'weekly' | 'monthly' | 'yearly';

export type SortField = 'created_at' | 'due_date' | 'title' | 'priority';

export type SortOrder = 'asc' | 'desc';

export type TaskStatus = 'all' | 'active' | 'completed';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  priority: Priority;
  category?: Category;
  due_date?: string;
  recurrence?: Recurrence;
  due_time?: string;
  reminder_minutes?: number;
  reminder_sent: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: Priority;
  category?: Category;
  due_date?: string;
  due_time?: string;
  recurrence?: Recurrence;
  reminder_minutes?: number;
}

export type UpdateTaskInput = Partial<CreateTaskInput>;

export interface TaskFilters {
  status: TaskStatus;
  priority?: Priority;
  category?: Category;
  search?: string;
  sort_by: SortField;
  sort_order: SortOrder;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface ApiError {
  detail: string | Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}
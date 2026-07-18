"use client";

import { TaskFilters as TaskFiltersType } from "@/types/task";

interface TaskFiltersProps {
  filters: TaskFiltersType;
  onFilterChange: (filters: Partial<TaskFiltersType>) => void;
  totalCount: number;
  filteredCount: number;
}

export function TaskFilters({
  filters,
  onFilterChange,
  totalCount,
  filteredCount,
}: TaskFiltersProps) {
  return (
    <div className="mb-6 space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <input
            type="text"
            placeholder="Search tasks..."
            value={filters.search || ""}
            onChange={(e) => onFilterChange({ search: e.target.value || undefined })}
            className="input-field pl-10"
          />
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>

        <div className="text-sm text-gray-500">
          {filteredCount === totalCount
            ? `${totalCount} tasks`
            : `${filteredCount} of ${totalCount} tasks`}
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <div>
          <label htmlFor="status-filter" className="sr-only">
            Status
          </label>
          <select
            id="status-filter"
            value={filters.status}
            onChange={(e) =>
              onFilterChange({
                status: e.target.value as TaskFiltersType["status"],
              })
            }
            className="input-field w-auto"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div>
          <label htmlFor="priority-filter" className="sr-only">
            Priority
          </label>
          <select
            id="priority-filter"
            value={filters.priority || ""}
            onChange={(e) =>
              onFilterChange({
                priority: (e.target.value as TaskFiltersType["priority"]) || undefined,
              })
            }
            className="input-field w-auto"
          >
            <option value="">All Priority</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div>
          <label htmlFor="category-filter" className="sr-only">
            Category
          </label>
          <select
            id="category-filter"
            value={filters.category || ""}
            onChange={(e) =>
              onFilterChange({
                category: (e.target.value as TaskFiltersType["category"]) || undefined,
              })
            }
            className="input-field w-auto"
          >
            <option value="">All Category</option>
            <option value="work">Work</option>
            <option value="home">Home</option>
            <option value="personal">Personal</option>
            <option value="health">Health</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label htmlFor="sort-by" className="sr-only">
            Sort by
          </label>
          <select
            id="sort-by"
            value={filters.sort_by}
            onChange={(e) =>
              onFilterChange({
                sort_by: e.target.value as TaskFiltersType["sort_by"],
              })
            }
            className="input-field w-auto"
          >
            <option value="created_at">Created Date</option>
            <option value="due_date">Due Date</option>
            <option value="title">Title</option>
            <option value="priority">Priority</option>
          </select>
        </div>

        <div>
          <label htmlFor="sort-order" className="sr-only">
            Sort order
          </label>
          <select
            id="sort-order"
            value={filters.sort_order}
            onChange={(e) =>
              onFilterChange({
                sort_order: e.target.value as TaskFiltersType["sort_order"],
              })
            }
            className="input-field w-auto"
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>
        </div>

        {(filters.search ||
          filters.status !== "all" ||
          filters.priority ||
          filters.category) && (
          <button
            onClick={() =>
              onFilterChange({
                search: undefined,
                status: "all",
                priority: undefined,
                category: undefined,
              })
            }
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
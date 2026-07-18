"use client";

import { useState } from "react";
import { CreateTaskInput, Task } from "@/types/task";
import { api } from "@/lib/api";

interface TaskFormProps {
  onTaskCreated: (task: Task) => void;
  editTask?: Task;
  onTaskUpdated?: (task: Task) => void;
  onCancel?: () => void;
}

export function TaskForm({
  onTaskCreated,
  editTask,
  onTaskUpdated,
  onCancel,
}: TaskFormProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const [title, setTitle] = useState(editTask?.title || "");
  const [description, setDescription] = useState(editTask?.description || "");
  const [priority, setPriority] = useState<"high" | "medium" | "low">(
    editTask?.priority || "medium"
  );
  const [category, setCategory] = useState<
    "work" | "home" | "personal" | "health" | "other" | undefined
  >(editTask?.category);
  const [dueDate, setDueDate] = useState(editTask?.due_date || "");
  const [dueTime, setDueTime] = useState(editTask?.due_time || "");
  const [recurrence, setRecurrence] = useState<
    "daily" | "weekly" | "monthly" | "yearly" | undefined
  >(editTask?.recurrence);
  const [reminderMinutes, setReminderMinutes] = useState(
    editTask?.reminder_minutes?.toString() || ""
  );

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setPriority("medium");
    setCategory(undefined);
    setDueDate("");
    setDueTime("");
    setRecurrence(undefined);
    setReminderMinutes("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    setIsLoading(true);

    try {
      const taskData: CreateTaskInput = {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        category,
        due_date: dueDate || undefined,
        due_time: dueTime || undefined,
        recurrence,
        reminder_minutes: reminderMinutes ? parseInt(reminderMinutes) : undefined,
      };

      if (editTask && onTaskUpdated) {
        const updatedTask = await api.updateTask(editTask.id, taskData);
        onTaskUpdated(updatedTask);
        onCancel?.();
      } else {
        const newTask = await api.createTask(taskData);
        onTaskCreated(newTask);
        resetForm();
        setIsExpanded(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    resetForm();
    setIsExpanded(false);
    onCancel?.();
  };

  return (
    <div className="mb-6">
      {!isExpanded && !editTask ? (
        <button
          onClick={() => setIsExpanded(true)}
          className="w-full card text-left hover:border-blue-300 transition-colors duration-150"
        >
          <span className="text-gray-500">+ Create new task</span>
        </button>
      ) : (
        <div className="card animate-slide-in">
          <h3 className="text-lg font-semibold mb-4">
            {editTask ? "Edit Task" : "Create New Task"}
          </h3>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="title" className="label">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="input-field"
                placeholder="Task title"
                required
                maxLength={500}
              />
            </div>

            <div>
              <label htmlFor="description" className="label">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="input-field"
                placeholder="Optional description"
                rows={3}
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="priority" className="label">
                  Priority
                </label>
                <select
                  id="priority"
                  value={priority}
                  onChange={(e) =>
                    setPriority(e.target.value as "high" | "medium" | "low")
                  }
                  className="input-field"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label htmlFor="category" className="label">
                  Category
                </label>
                <select
                  id="category"
                  value={category || ""}
                  onChange={(e) =>
                    setCategory(
                      (e.target.value as typeof category) || undefined
                    )
                  }
                  className="input-field"
                >
                  <option value="">None</option>
                  <option value="work">Work</option>
                  <option value="home">Home</option>
                  <option value="personal">Personal</option>
                  <option value="health">Health</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label htmlFor="dueDate" className="label">
                  Due Date
                </label>
                <input
                  id="dueDate"
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="input-field"
                />
              </div>

              <div>
                <label htmlFor="dueTime" className="label">
                  Due Time
                </label>
                <input
                  id="dueTime"
                  type="time"
                  value={dueTime}
                  onChange={(e) => setDueTime(e.target.value)}
                  className="input-field"
                />
              </div>

              <div>
                <label htmlFor="recurrence" className="label">
                  Recurrence
                </label>
                <select
                  id="recurrence"
                  value={recurrence || ""}
                  onChange={(e) =>
                    setRecurrence(
                      (e.target.value as typeof recurrence) || undefined
                    )
                  }
                  className="input-field"
                >
                  <option value="">None</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>

              <div>
                <label htmlFor="reminder" className="label">
                  Reminder (minutes before)
                </label>
                <input
                  id="reminder"
                  type="number"
                  min="0"
                  value={reminderMinutes}
                  onChange={(e) => setReminderMinutes(e.target.value)}
                  className="input-field"
                  placeholder="0"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={handleCancel}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary"
              >
                {isLoading
                  ? "Saving..."
                  : editTask
                  ? "Save Changes"
                  : "Create Task"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
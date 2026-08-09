"use client";

import { useState } from "react";
import { Task } from "@/types/task";
import { api } from "@/lib/api";
import { TaskForm } from "./task-form";

interface TaskCardProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

export function TaskCard({ task, onTaskUpdated, onTaskDeleted }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      const updatedTask = await api.toggleComplete(task.id);
      onTaskUpdated(updatedTask);
    } catch (error) {
      console.error("Failed to toggle task:", error);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await api.deleteTask(task.id);
      onTaskDeleted(task.id);
    } catch (error) {
      console.error("Failed to delete task:", error);
    } finally {
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const getPriorityBadgeClass = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-800";
      case "medium":
        return "bg-yellow-100 text-yellow-800";
      case "low":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getCategoryBadgeClass = (category: string) => {
    switch (category) {
      case "work":
        return "bg-blue-100 text-blue-800";
      case "home":
        return "bg-purple-100 text-purple-800";
      case "personal":
        return "bg-pink-100 text-pink-800";
      case "health":
        return "bg-green-100 text-green-800";
      case "other":
        return "bg-gray-100 text-gray-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  if (isEditing) {
    return (
      <TaskForm
        editTask={task}
        onTaskUpdated={(updatedTask) => {
          onTaskUpdated(updatedTask);
          setIsEditing(false);
        }}
        onCancel={() => setIsEditing(false)}
        onTaskCreated={() => {}}
      />
    );
  }

  return (
    <div
      className={`card transition-all duration-200 ${
        task.is_completed ? "opacity-75" : ""
      }`}
    >
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 pt-1">
          <input
            type="checkbox"
            checked={task.is_completed}
            onChange={handleToggle}
            disabled={isToggling}
            className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer disabled:cursor-not-allowed"
          />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 flex-wrap">
            <h3
              className={`text-lg font-medium ${
                task.is_completed ? "line-through text-gray-500" : "text-gray-900"
              }`}
            >
              {task.title}
            </h3>
            <span
              className={`px-2 py-0.5 rounded-full text-xs font-medium ${getPriorityBadgeClass(
                task.priority
              )}`}
            >
              {task.priority}
            </span>
            {task.category && (
              <span
                className={`px-2 py-0.5 rounded-full text-xs font-medium ${getCategoryBadgeClass(
                  task.category
                )}`}
              >
                {task.category}
              </span>
            )}
          </div>

          {task.description && (
            <p className="mt-1 text-sm text-gray-600 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
            {task.due_date && (
              <span>
                Due: {formatDate(task.due_date)}
                {task.due_time && ` ${task.due_time}`}
              </span>
            )}
            {task.recurrence && (
              <span className="capitalize">Recurs: {task.recurrence}</span>
            )}
          </div>
        </div>

        <div className="flex-shrink-0 flex items-center space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            className="text-gray-500 hover:text-blue-600 transition-colors"
            disabled={isDeleting || isToggling}
          >
            Edit
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="text-gray-500 hover:text-red-600 transition-colors"
            disabled={isDeleting || isToggling}
          >
            Delete
          </button>
        </div>
      </div>

      {showDeleteConfirm && (
        <div className="mt-4 p-3 bg-red-50 rounded-lg border border-red-200">
          <p className="text-sm text-red-700 mb-3">
            Are you sure you want to delete this task?
          </p>
          <div className="flex justify-end space-x-2">
            <button
              onClick={() => setShowDeleteConfirm(false)}
              className="px-3 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded"
              disabled={isDeleting}
            >
              Cancel
            </button>
            <button
              onClick={handleDelete}
              className="px-3 py-1 text-sm text-white bg-red-600 hover:bg-red-700 rounded disabled:opacity-50"
              disabled={isDeleting}
            >
              {isDeleting ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
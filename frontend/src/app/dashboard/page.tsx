"use client";

import { AuthGuard } from "@/components/auth-guard";
import { useSession, signOut } from "@/lib/auth-client";
import { TaskList } from "@/components/task-list";
import { TaskForm } from "@/components/task-form";
import { TaskFilters } from "@/components/task-filters";
import { useState } from "react";
import { Task, TaskFilters as TaskFiltersType } from "@/types/task";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const { data: session } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filters, setFilters] = useState<TaskFiltersType>({
    status: "all",
    sort_by: "created_at",
    sort_order: "desc",
  });
  const [isLoading, setIsLoading] = useState(true);

  const fetchTasks = async () => {
    setIsLoading(true);
    try {
      const fetchedTasks = await api.getTasks(filters);
      setTasks(fetchedTasks);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks((prev) => [newTask, ...prev]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === updatedTask.id ? updatedTask : task))
    );
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  const handleFilterChange = (newFilters: Partial<TaskFiltersType>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const handleSignOut = async () => {
    await signOut();
    window.location.href = "/sign-in";
  };

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  {session?.user?.email}
                </span>
                <button
                  onClick={handleSignOut}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <TaskFilters
            filters={filters}
            onFilterChange={handleFilterChange}
            totalCount={tasks.length}
            filteredCount={tasks.length}
          />

          <TaskForm onTaskCreated={handleTaskCreated} />

          <TaskList
            tasks={tasks}
            isLoading={isLoading}
            onTaskUpdated={handleTaskUpdated}
            onTaskDeleted={handleTaskDeleted}
            onRefresh={fetchTasks}
          />
        </main>
      </div>
    </AuthGuard>
  );
}
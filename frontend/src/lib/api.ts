import { Task, CreateTaskInput, UpdateTaskInput, TaskFilters, ApiError } from "@/types/task";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string | null> {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    // /token issues the EdDSA JWT the backend verifies against JWKS.
    // session.token is an opaque session id and will not pass verification.
    const response = await fetch("/api/auth/token", {
      credentials: "include",
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data.token || null;
  } catch {
    return null;
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...options.headers as Record<string, string>,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const fetchOptions: RequestInit = {
    ...options,
    headers,
    credentials: "include",
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, fetchOptions);

  if (response.status === 401) {
    if (typeof window !== "undefined") {
      window.location.href = "/sign-in";
    }
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(
      typeof error.detail === "string"
        ? error.detail
        : error.detail.map((d) => d.msg).join(", ")
    );
  }

  if (response.status === 204) {
    return null as T;
  }

  return response.json();
}

export const api = {
  async getTasks(filters?: Partial<TaskFilters>): Promise<Task[]> {
    const params = new URLSearchParams();

    if (filters?.status && filters.status !== "all") {
      params.set("status", filters.status);
    }
    if (filters?.priority) {
      params.set("priority", filters.priority);
    }
    if (filters?.category) {
      params.set("category", filters.category);
    }
    if (filters?.search) {
      params.set("search", filters.search);
    }
    if (filters?.sort_by) {
      params.set("sort_by", filters.sort_by);
    }
    if (filters?.sort_order) {
      params.set("sort_order", filters.sort_order);
    }

    const queryString = params.toString();
    const endpoint = `/api/tasks${queryString ? `?${queryString}` : ""}`;

    return apiRequest<Task[]>(endpoint);
  },

  async getTask(id: number): Promise<Task> {
    return apiRequest<Task>(`/api/tasks/${id}`);
  },

  async createTask(data: CreateTaskInput): Promise<Task> {
    return apiRequest<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async updateTask(id: number, data: UpdateTaskInput): Promise<Task> {
    return apiRequest<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async deleteTask(id: number): Promise<void> {
    return apiRequest<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    });
  },

  async toggleComplete(id: number): Promise<Task> {
    return apiRequest<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    });
  },
};
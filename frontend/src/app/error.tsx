"use client";

import { useEffect } from "react";

function friendlyMessage(error: Error): { title: string; detail: string } {
  const message = error.message.toLowerCase();

  if (message.includes("failed to fetch") || message.includes("networkerror")) {
    return {
      title: "Can't reach the server",
      detail:
        "The task service isn't responding. Check that the backend is running, then try again.",
    };
  }

  if (
    message.includes("econnrefused") ||
    message.includes("database") ||
    message.includes("connection")
  ) {
    return {
      title: "Database unavailable",
      detail:
        "We couldn't connect to the database. This is usually temporary — please try again in a moment.",
    };
  }

  return {
    title: "Something went wrong",
    detail: "An unexpected error occurred. Try again, or reload the page.",
  };
}

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  const { title, detail } = friendlyMessage(error);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="card max-w-md w-full text-center">
        <div className="text-4xl mb-4">⚠️</div>
        <h1 className="text-lg font-medium text-gray-900 mb-2">{title}</h1>
        <p className="text-gray-500 mb-6">{detail}</p>
        <button type="button" onClick={reset} className="btn-primary">
          Try again
        </button>
      </div>
    </div>
  );
}

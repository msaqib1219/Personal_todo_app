"use client";

import "./globals.css";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="card max-w-md w-full text-center">
            <div className="text-4xl mb-4">⚠️</div>
            <h1 className="text-lg font-medium text-gray-900 mb-2">
              The app failed to load
            </h1>
            <p className="text-gray-500 mb-6">
              Something went wrong while starting the application. Reload the
              page, and if the problem continues check that the backend and
              database are reachable.
            </p>
            <button type="button" onClick={reset} className="btn-primary">
              Reload
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}

import { useState } from "react";

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery || loading) {
      return;
    }

    onSearch(trimmedQuery);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full"
    >
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          type="text"
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          placeholder="Try: person near a car"
          className="flex-1 rounded-xl border border-gray-300 bg-white px-5 py-4 text-gray-900 shadow-sm outline-none transition focus:border-gray-900 focus:ring-2 focus:ring-gray-200"
        />

        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-gray-900 px-7 py-4 font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
    </form>
  );
}

export default SearchBar;


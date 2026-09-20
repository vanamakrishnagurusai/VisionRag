import { useState } from "react";

import SearchBar from "./components/SearchBar";
import ResultGrid from "./components/ResultGrid";

import { API_BASE_URL } from "./config";


function App() {

  const [results, setResults] = useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [query, setQuery] =
    useState("");


  const searchImages = async (
    searchQuery
  ) => {

    setLoading(true);
    setError("");
    setQuery(searchQuery);

    try {

      const response = await fetch(
        `${API_BASE_URL}/search`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            query: searchQuery,
            top_k: 6,
          }),
        }
      );

      if (!response.ok) {

        const errorData =
          await response.json();

        throw new Error(
          errorData.detail ||
          "Search request failed."
        );
      }

      const data =
        await response.json();

      setResults(
        data.results || []
      );

    } catch (err) {

      setError(
        err.message ||
        "Unable to connect to the VisionRAG API."
      );

      setResults([]);

    } finally {

      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-slate-50">

      {/* Header */}

      <header className="border-b border-gray-200 bg-white">

        <div className="mx-auto max-w-7xl px-6 py-5">

          <div className="flex items-center justify-between">

            <div>

              <h1 className="text-xl font-bold tracking-tight text-gray-900">
                VisionRAG
              </h1>

              <p className="text-sm text-gray-500">
                Multimodal visual search
              </p>

            </div>

            <div className="rounded-full bg-gray-100 px-4 py-2 text-xs font-medium text-gray-600">
              AI Vision Search
            </div>

          </div>

        </div>

      </header>


      {/* Main */}

      <main className="mx-auto max-w-7xl px-6 py-12">

        {/* Hero */}

        <section className="mx-auto max-w-3xl text-center">

          <div className="mb-4 inline-flex rounded-full bg-gray-900 px-4 py-2 text-xs font-medium text-white">
            YOLO + BLIP + FAISS
          </div>

          <h2 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Search your images
            <span className="block text-gray-500">
              using natural language.
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-gray-600">
            Describe what you're looking for and
            VisionRAG retrieves visually relevant
            images from your collection.
          </p>

          <div className="mt-8">

            <SearchBar
              onSearch={searchImages}
              loading={loading}
            />

          </div>

        </section>


        {/* Error */}

        {error && (

          <div className="mx-auto mt-8 max-w-3xl rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>

        )}


        {/* Results */}

        <section className="mt-14">

          {query && !loading && (

            <div className="mb-6">

              <h2 className="text-xl font-semibold text-gray-900">
                Search results
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Results for "{query}"
              </p>

            </div>

          )}

          {loading ? (

            <div className="py-20 text-center">

              <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-gray-900" />

              <p className="mt-4 text-sm text-gray-500">
                Searching your visual library...
              </p>

            </div>

          ) : (

            <ResultGrid
              results={results}
            />

          )}

        </section>

      </main>

    </div>
  );
}

export default App;
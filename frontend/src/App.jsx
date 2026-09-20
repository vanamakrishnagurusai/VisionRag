import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultGrid from "./components/ResultGrid";
import { API_BASE_URL } from "./config";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [minScore, setMinScore] = useState(0.20);
  const [objectFilter, setObjectFilter] = useState("");

  const searchImages = async (searchQuery) => {
    if (!searchQuery.trim()) {
      return;
    }

    setQuery(searchQuery);
    setLoading(true);
    setError("");
    setAnswer("");
    setResults([]);

    try {
      const response = await fetch(
        `${API_BASE_URL}/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: searchQuery,
            top_k: 6,
            min_score: minScore,
            object_filter: objectFilter || null,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Search failed."
        );
      }

      const data = await response.json();

      setAnswer(data.answer || "");
      setResults(data.results || []);

    } catch (err) {
      console.error(err);
      setError(
        err.message ||
        "Unable to connect to VisionRAG API."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">

      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

          <div>
            <h1 className="text-xl font-bold text-slate-900">
              VisionRAG
            </h1>

            <p className="text-sm text-slate-500">
              Multimodal Visual Search
            </p>
          </div>

          <div className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
            AI + Computer Vision
          </div>

        </div>
      </header>


      {/* Main */}
      <main className="mx-auto max-w-7xl px-6 py-12">

        {/* Hero */}
        <section className="mx-auto max-w-3xl text-center">

          <div className="mb-4 inline-flex rounded-full bg-blue-50 px-4 py-2 text-sm font-medium text-blue-600">
            Semantic Image Search
          </div>

          <h2 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
            Search your images
            <span className="block text-blue-600">
              using natural language
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-slate-500">
            Find visually relevant images using AI-powered
            object detection, image understanding and
            semantic search.
          </p>

        </section>


        {/* Search */}
        <section className="mx-auto mt-10 max-w-3xl">

          <SearchBar
            onSearch={searchImages}
            loading={loading}
          />

          <p className="mt-3 text-center text-sm text-slate-400">
            Try: "person near a car", "people outdoors",
            or "animals on grass"
          </p>

        </section>
        <div className="mx-auto mt-5 flex max-w-3xl flex-wrap items-center justify-center gap-3">

  <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2">

    <label className="text-sm text-slate-500">
      Object
    </label>

    <input
      type="text"
      value={objectFilter}
      onChange={(event) =>
        setObjectFilter(event.target.value)
      }
      placeholder="e.g. person"
      className="w-32 bg-transparent text-sm text-slate-700 outline-none"
    />

  </div>


  <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-2">

    <label className="text-sm text-slate-500">
      Min similarity
    </label>

    <input
      type="range"
      min="0"
      max="1"
      step="0.05"
      value={minScore}
      onChange={(event) =>
        setMinScore(
          Number(event.target.value)
        )
      }
    />

    <span className="w-12 text-sm font-medium text-slate-700">
      {minScore.toFixed(2)}
    </span>

  </div>

</div>

        {/* Error */}
        {error && (
          <div className="mx-auto mt-8 max-w-3xl rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
            <p className="font-medium">
              Search Error
            </p>

            <p className="mt-1 text-sm">
              {error}
            </p>
          </div>
        )}


        {/* AI Answer */}
        {answer && !loading && (
          <section className="mx-auto mt-10 max-w-4xl">

            <div className="rounded-2xl border border-blue-100 bg-white p-6 shadow-sm">

              <div className="flex items-start gap-4">

                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-xl">
                  ✦
                </div>

                <div className="flex-1">

                  <div className="flex items-center gap-3">

                    <h3 className="font-semibold text-slate-900">
                      VisionRAG Answer
                    </h3>

                    <span className="rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-600">
                      Grounded
                    </span>

                  </div>

                  <p className="mt-3 leading-7 text-slate-600">
                    {answer}
                  </p>

                </div>

              </div>

            </div>

          </section>
        )}


        {/* Loading */}
        {loading && (
          <div className="mt-12 flex flex-col items-center justify-center">

            <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />

            <p className="mt-4 text-sm text-slate-500">
              Searching images and generating answer...
            </p>

          </div>
        )}


        {/* Results */}
        {!loading && results.length > 0 && (
          <section className="mt-12">

            <div className="mb-6 flex items-center justify-between">

              <div>
                <h3 className="text-xl font-semibold text-slate-900">
                  Relevant Images
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  {results.length} visually relevant images
                  found for "{query}"
                </p>
              </div>

            </div>

            <ResultGrid results={results} />

          </section>
        )}


        {/* No results */}
        {!loading &&
          !error &&
          query &&
          results.length === 0 && (
            <div className="mt-12 text-center">

              <div className="text-4xl">
                🔍
              </div>

              <h3 className="mt-4 font-semibold text-slate-900">
                No matching images found
              </h3>

              <p className="mt-2 text-sm text-slate-500">
                Try using a different description.
              </p>

            </div>
          )}

      </main>


      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6">

        <p className="text-center text-sm text-slate-400">
          VisionRAG • YOLO + BLIP + FAISS + Gemini
        </p>

      </footer>

    </div>
  );
}

export default App;
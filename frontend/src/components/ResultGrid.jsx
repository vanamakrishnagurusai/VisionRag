import ResultCard from "./ResultCard";

function ResultGrid({ results }) {
  if (!results.length) {
    return (
      <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-12 text-center">
        <h3 className="text-lg font-semibold text-gray-900">
          No results found
        </h3>

        <p className="mt-2 text-sm text-gray-500">
          Try a different natural-language query.
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {results.map((result) => (
        <ResultCard
          key={`${result.filename}-${result.rank}`}
          result={result}
        />
      ))}
    </div>
  );
}

export default ResultGrid;
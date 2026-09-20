import { API_BASE_URL } from "../config";

function ResultCard({ result }) {
  const imageUrl =
    `${API_BASE_URL}${result.image_url}`;

  const percentage =
    Math.max(
      0,
      Math.min(
        100,
        result.score * 100
      )
    );

  return (
    <article className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg">

      <div className="relative aspect-video overflow-hidden bg-gray-100">

        <img
          src={imageUrl}
          alt={result.caption || result.filename}
          className="h-full w-full object-cover"
        />

        <div className="absolute right-3 top-3 rounded-full bg-black/75 px-3 py-1 text-sm font-medium text-white">
          {result.score.toFixed(3)}%
        </div>

      </div>

      <div className="p-5">

        <div className="mb-3 flex items-center justify-between">

          <h3 className="font-semibold text-gray-900">
            {result.filename}
          </h3>

          <span className="text-sm text-gray-500">
            #{result.rank}
          </span>

        </div>

        {result.caption && (
          <p className="mb-4 text-sm leading-6 text-gray-600">
            {result.caption}
          </p>
        )}

        <div className="flex flex-wrap gap-2">

          {result.objects?.map(
            (object, index) => (
              <span
                key={`${object.class}-${index}`}
                className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700"
              >
                {object.class}
              </span>
            )
          )}

        </div>

      </div>

    </article>
  );
}

export default ResultCard;
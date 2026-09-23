import { useEffect, useState } from "react";
import { API_BASE_URL } from "../config";

function MetricCard({ title, value, description }) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-gray-500">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold text-gray-900">
        {value}
      </p>

      <p className="mt-2 text-xs text-gray-500">
        {description}
      </p>
    </div>
  );
}

function EvaluationDashboard() {
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadEvaluation = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/evaluation`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Failed to load evaluation."
          );
        }

        setEvaluation(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadEvaluation();
  }, []);

  if (loading) {
    return (
      <div className="py-10 text-center text-gray-500">
        Loading evaluation results...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-red-50 p-4 text-sm text-red-700">
        {error}
      </div>
    );
  }

  if (!evaluation) {
    return null;
  }

  const metrics = evaluation.overall;
  const queries = evaluation.queries || [];

  return (
    <section className="mt-12">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Retrieval Evaluation
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Performance of VisionRAG across {metrics.queries} evaluation queries.
        </p>
      </div>

      {/* Metric cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">

        <MetricCard
          title="Precision@1"
          value={`${(metrics.precision_at_1 * 100).toFixed(1)}%`}
          description="Top result relevance"
        />

        <MetricCard
          title="Precision@3"
          value={`${(metrics.precision_at_3 * 100).toFixed(1)}%`}
          description="Top 3 result relevance"
        />

        <MetricCard
          title="Precision@5"
          value={`${(metrics.precision_at_5 * 100).toFixed(1)}%`}
          description="Top 5 result relevance"
        />

        <MetricCard
          title="Recall@5"
          value={`${(metrics.recall_at_5 * 100).toFixed(1)}%`}
          description="Relevant images retrieved"
        />

        <MetricCard
          title="Avg. Similarity"
          value={metrics.average_similarity.toFixed(3)}
          description="Average retrieval score"
        />

      </div>

      {/* Query table */}
      <div className="mt-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">

        <div className="border-b border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Query-Level Performance
          </h3>

          <p className="mt-1 text-sm text-gray-500">
            Retrieval metrics for each evaluation query.
          </p>
        </div>

        <div className="overflow-x-auto">

          <table className="w-full text-left text-sm">

            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-6 py-4 font-semibold text-gray-700">
                  Query
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  Relevant
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  P@1
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  P@3
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  P@5
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  R@5
                </th>

                <th className="px-6 py-4 font-semibold text-gray-700">
                  Similarity
                </th>
              </tr>
            </thead>

            <tbody>

              {queries.map((item, index) => (
                <tr
                  key={`${item.query}-${index}`}
                  className="border-b border-gray-100 last:border-b-0 hover:bg-gray-50"
                >

                  <td className="px-6 py-4 font-medium text-gray-900">
                    {item.query}
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {item.relevant_count}
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {(item.precision_at_1 * 100).toFixed(0)}%
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {(item.precision_at_3 * 100).toFixed(0)}%
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {(item.precision_at_5 * 100).toFixed(0)}%
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {(item.recall_at_5 * 100).toFixed(1)}%
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {item.average_similarity.toFixed(3)}
                  </td>

                </tr>
              ))}

            </tbody>

          </table>

        </div>
      </div>
    </section>
  );
}

export default EvaluationDashboard;
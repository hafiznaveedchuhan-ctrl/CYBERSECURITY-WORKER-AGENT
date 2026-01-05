'use client';

interface Citation {
  id: string;
  content: string;
  source: string;
  page?: string;
}

interface CitationsPanelProps {
  citations: Citation[];
  onClose: () => void;
}

export function CitationsPanel({ citations, onClose }: CitationsPanelProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg w-full max-w-2xl max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Sources & Citations</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Citations List */}
        <div className="p-4 overflow-y-auto max-h-[60vh] space-y-4">
          {citations.map((citation, index) => (
            <div
              key={citation.id}
              className="bg-gray-700/50 rounded-lg p-4 border border-gray-600"
            >
              <div className="flex items-start justify-between mb-2">
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-blue-600 text-white text-xs font-medium">
                  {index + 1}
                </span>
                <div className="flex items-center text-sm text-gray-400">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4 mr-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  {citation.source}
                  {citation.page && <span className="ml-2">p. {citation.page}</span>}
                </div>
              </div>

              <p className="text-gray-300 text-sm leading-relaxed">{citation.content}</p>

              <div className="mt-3">
                <a
                  href={`/docs/${citation.source}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-400 hover:text-blue-300 flex items-center"
                >
                  <span>View in textbook</span>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-3 w-3 ml-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                    />
                  </svg>
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-700 bg-gray-800/50">
          <p className="text-xs text-gray-500 text-center">
            Citations are from the AI-SOC Textbook. Click to view full context.
          </p>
        </div>
      </div>
    </div>
  );
}

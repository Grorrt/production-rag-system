interface CitationCardProps {
  source: string;
  page: string | null;
  reference: string;
  index: number;
}

function CitationCard({ source, page, reference, index }: CitationCardProps) {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 hover:shadow-sm transition-shadow">
      <div className="flex items-start gap-3">
        <span className="bg-blue-100 text-blue-700 text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center shrink-0">
          {index + 1}
        </span>

        <div className="min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate">{source}</p>

          {page && (
            <p className="text-xs text-gray-500 mt-0.5">Page {page}</p>
          )}

          <p className="text-xs text-gray-400 mt-1 truncate">{reference}</p>
        </div>
      </div>
    </div>
  );
}

export default CitationCard;

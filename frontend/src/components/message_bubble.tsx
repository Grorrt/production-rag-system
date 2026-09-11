import ReactMarkdown from "react-markdown";

interface Source { source: string; page: string | null; chunk_id: string | null; reference: string }

interface MessageBubbleProps { text: string; isUser: boolean; sources?: Source[] }

function MessageBubble({ text, isUser, sources }: MessageBubbleProps) {
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} message-enter`}>
      <div className={`max-w-[85%] lg:max-w-[75%] ${isUser
        ? "bg-primary-600 text-white rounded-2xl rounded-br-md"
        : "bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-2xl rounded-bl-md shadow-sm"
      }`}>
        {isUser ? (
          <p className="px-5 py-3 text-sm leading-relaxed">{text}</p>
        ) : (
          <div className="px-5 py-3">
            <div className="prose prose-sm max-w-none dark:prose-invert prose-headings:text-surface-900 dark:prose-headings:text-surface-100 prose-a:text-primary-600 dark:prose-a:text-primary-400">
              <ReactMarkdown>{text}</ReactMarkdown>
            </div>

            {sources && sources.length > 0 && (
              <div className="mt-4 pt-3 border-t border-surface-200 dark:border-surface-700">
                <p className="text-xs font-semibold text-surface-400 dark:text-surface-500 mb-2 flex items-center gap-1.5">
                  <FileIcon /> Sources ({sources.length})
                </p>
                <div className="space-y-1.5">
                  {sources.map((source, idx) => (
                    <div key={idx}
                      className="flex items-center gap-2.5 bg-surface-50 dark:bg-surface-900/50 rounded-lg px-3 py-2 text-xs">
                      <span className="shrink-0 w-5 h-5 rounded-md bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 flex items-center justify-center text-[10px] font-bold">
                        {idx + 1}
                      </span>
                      <div className="min-w-0">
                        <p className="font-medium text-surface-700 dark:text-surface-300 truncate">{source.source}</p>
                        {source.page && <p className="text-surface-400">Page {source.page}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function FileIcon() { return <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>; }

export default MessageBubble;

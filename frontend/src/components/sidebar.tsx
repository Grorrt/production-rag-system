import { useTheme } from "../App";

type Page = "chat" | "dashboard";

interface SidebarProps {
  currentPage: Page;
  onPageChange: (page: Page) => void;
  username: string;
  onLogout: () => void;
}

function Sidebar({ currentPage, onPageChange, username, onLogout }: SidebarProps) {
  const { dark, toggle } = useTheme();

  const navItems: { id: Page; label: string; icon: JSX.Element }[] = [
    { id: "chat", label: "Chat", icon: <ChatIcon /> },
    { id: "dashboard", label: "Dashboard", icon: <DashboardIcon /> },
  ];

  return (
    <aside className="w-64 lg:w-72 flex-shrink-0 glass border-r border-surface-200 dark:border-surface-700/50 flex flex-col h-full transition-colors duration-200">
      <div className="p-5 border-b border-surface-200 dark:border-surface-700/50">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 gradient-bg rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
            <span className="text-sm font-bold text-white">R</span>
          </div>
          <div className="min-w-0">
            <h1 className="text-sm font-bold text-surface-900 dark:text-surface-50">RAG System</h1>
            <p className="text-[10px] text-surface-400 dark:text-surface-500">Knowledge Assistant</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ id, label, icon }) => (
          <button key={id} onClick={() => onPageChange(id)}
            className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
              currentPage === id
                ? "bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 shadow-sm"
                : "text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 hover:text-surface-900 dark:hover:text-surface-200"
            }`}>
            {icon}
            {label}
          </button>
        ))}
      </nav>

      <div className="p-3 border-t border-surface-200 dark:border-surface-700/50 space-y-1">
        <button onClick={toggle}
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 transition-all duration-200">
          {dark ? <SunSmallIcon /> : <MoonSmallIcon />}
          {dark ? "Light Mode" : "Dark Mode"}
        </button>

        <div className="flex items-center gap-3 px-3.5 py-2.5">
          <div className="w-7 h-7 rounded-lg gradient-bg flex items-center justify-center text-[10px] font-bold text-white shrink-0">
            {username.charAt(0).toUpperCase()}
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-medium text-surface-700 dark:text-surface-300 truncate">{username}</p>
          </div>
          <button onClick={onLogout}
            className="p-1.5 rounded-lg text-surface-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200"
            title="Sign Out">
            <LogoutIcon />
          </button>
        </div>
      </div>
    </aside>
  );
}

function ChatIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>; }
function DashboardIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>; }
function SunSmallIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>; }
function MoonSmallIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>; }
function LogoutIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>; }

export default Sidebar;

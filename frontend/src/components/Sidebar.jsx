import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/app", label: "Home", icon: "🏠", end: true },
  { to: "/app/chat", label: "Case Canvas & Chat", icon: "🧭" },
  { to: "/app/pressure", label: "Pressure Map", icon: "🔥" },
  { to: "/app/profile", label: "Officer Profile", icon: "👤" },
];

export default function Sidebar({ officer, onLogout }) {
  return (
    <aside className="w-56 flex-shrink-0 bg-gray-900 border-r border-gray-800 flex flex-col h-full">
      <div className="px-4 py-4 border-b border-gray-800">
        <h1 className="font-bold text-lg leading-tight">
          PRAJNA
          <span className="block text-xs font-normal text-blue-400">
            Crime Intelligence
          </span>
        </h1>
      </div>

      <nav className="flex-1 py-3 px-2 space-y-1">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded text-sm transition ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white"
              }`
            }
          >
            <span>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="px-4 py-3 border-t border-gray-800">
        <p className="text-xs text-gray-300 truncate">{officer?.name}</p>
        <p className="text-[11px] text-gray-600 truncate mb-2">
          {officer?.officerId}
        </p>
        <button
          onClick={onLogout}
          className="text-xs text-red-400 hover:text-red-300"
        >
          Log out
        </button>
      </div>
    </aside>
  );
}

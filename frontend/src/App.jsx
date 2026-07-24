import { useState, useCallback } from "react";
import CaseCanvas from "./components/CaseCanvas";
import ChatPanel from "./components/ChatPanel";

const OFFICER_ID = "OFF001";
const SESSION_ID = `session-${Date.now()}`;

export default function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  const handleNodesReceived = useCallback((newNodes, newEdges) => {
    setNodes((prev) => {
      const existingIds = new Set(prev.map((n) => n.id));
      const merged = [...prev, ...newNodes.filter((n) => !existingIds.has(n.id))];
      return merged;
    });
    setEdges((prev) => {
      const key = (e) => `${e.source}-${e.target}`;
      const existingKeys = new Set(prev.map(key));
      const merged = [...prev, ...newEdges.filter((e) => !existingKeys.has(key(e)))];
      return merged;
    });
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col">
      <header className="bg-gray-900 border-b border-gray-800 px-4 py-2 flex items-center justify-between">
        <h1 className="font-bold text-lg">
          PRAJNA <span className="text-blue-400">| Case Canvas</span>
        </h1>
        <span className="text-xs text-gray-500">Officer: {OFFICER_ID}</span>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="w-96 flex-shrink-0">
          <ChatPanel
            officerId={OFFICER_ID}
            sessionId={SESSION_ID}
            onNodesReceived={handleNodesReceived}
          />
        </div>
        <div className="flex-1 relative">
          <CaseCanvas nodes={nodes} edges={edges} onNodeClick={setSelectedNode} />
          {selectedNode && (
            <div className="absolute top-4 right-4 bg-gray-900 border border-gray-700 rounded-lg p-4 w-72 shadow-xl">
              <button
                onClick={() => setSelectedNode(null)}
                className="float-right text-gray-500 hover:text-white"
              >
                ✕
              </button>
              <h3 className="font-semibold text-sm">{selectedNode.label}</h3>
              <p className="text-xs text-gray-400 capitalize">{selectedNode.type}</p>
              <pre className="text-xs mt-2 text-gray-300 whitespace-pre-wrap">
                {JSON.stringify(selectedNode, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
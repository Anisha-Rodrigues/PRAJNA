import { useState, useCallback } from "react";
import CaseCanvas from "./components/CaseCanvas";
import ChatPanel from "./components/ChatPanel";
import PressureMap from "./components/PressureMap";
import IntelligenceBrief from "./components/IntelligenceBrief";

const OFFICER_ID = "OFF001";
const SESSION_ID = `session-${Date.now()}`;

export default function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [view, setView] = useState("canvas");
  const [citedFIRs, setCitedFIRs] = useState([]);
  const [aiFindings, setAiFindings] = useState("");

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

  const handleAiReply = useCallback((text, firs) => {
    setAiFindings(text);
    if (firs?.length) setCitedFIRs((prev) => [...new Set([...prev, ...firs])]);
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col">
      <header className="bg-gray-900 border-b border-gray-800 px-4 py-2 flex items-center justify-between">
        <h1 className="font-bold text-lg">
          PRAJNA <span className="text-blue-400">| Case Canvas</span>
        </h1>
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500 whitespace-nowrap">Officer: {OFFICER_ID}</span>
          <button
            onClick={() => setView(view === "canvas" ? "pressure" : "canvas")}
            className="text-xs text-blue-400 whitespace-nowrap"
          >
            {view === "canvas" ? "Pressure Map →" : "← Case Canvas"}
          </button>
        </div>

        {/* FIXED: was `absolute top-10 right-0` inside a `relative` div that only
            fit its own small content — pushed this off-screen. Now `fixed` to the
            viewport with `right-4`, so it always fits regardless of screen size. */}
        <div className="fixed top-14 right-4 w-72 max-w-[90vw] max-h-[80vh] overflow-y-auto z-50">
          <IntelligenceBrief
            officerName={OFFICER_ID}
            officerId={OFFICER_ID}
            sessionId={SESSION_ID}
            canvasNodes={nodes}
            citedFIRs={citedFIRs}
            aiFindings={aiFindings}
            alerts={[]}
          />
        </div>
      </header>

      {view === "canvas" ? (
        <div className="flex flex-1 overflow-hidden">
          <div className="w-96 flex-shrink-0">
            <ChatPanel
              officerId={OFFICER_ID}
              sessionId={SESSION_ID}
              onNodesReceived={handleNodesReceived}
              onAiReply={handleAiReply}
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
      ) : (
        <div className="flex-1">
          <PressureMap />
        </div>
      )}
    </div>
  );
}
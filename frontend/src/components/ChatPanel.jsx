import { useState, useRef, useEffect } from "react";
import VoiceInput from "./VoiceInput";
import { sendQuery, saveMemory } from "../utils/api";

export default function ChatPanel({ officerId, sessionId, onNodesReceived, onAiReply }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Namaskara, Officer. Ask me about a suspect, FIR, location, or crime pattern." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [messages]);

  const handleSend = async (text, language = "en-IN") => {
    if (!text.trim()) return;
    setMessages((prev) => [...prev, { role: "officer", text }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendQuery(text, language, officerId, sessionId);
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.answer, citedFirs: data.cited_firs },
      ]);
      onNodesReceived(data.nodes || [], data.edges || []);
      onAiReply?.(data.answer, data.cited_firs);
      await saveMemory(
  officerId,
  text,
  data.answer,
  "logged",
  sessionId
);
    } catch (err) {
  console.error("PRAJNA request error:", err);

  setMessages((prev) => [
    ...prev,
    {
      role: "ai",
      text: `Error: ${err.message}`,
    },
  ]);
} finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 border-r border-gray-800">
      <div className="p-3 border-b border-gray-800 font-semibold text-blue-400">
        AI Investigator Chat
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "officer" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                m.role === "officer" ? "bg-blue-600" : "bg-gray-800"
              }`}
            >
              <p>{m.text}</p>
              {m.citedFirs?.length > 0 && (
                <p className="mt-1 text-xs text-gray-400">
                  Cited: {m.citedFirs.join(", ")}
                </p>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="text-xs text-gray-500">AI is thinking...</div>}
      </div>

      <div className="p-3 border-t border-gray-800 space-y-2">
        <VoiceInput onResult={(text, lang) => handleSend(text, lang)} />
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend(input)}
            placeholder="Ask about a suspect, FIR, or location..."
            className="flex-1 bg-gray-800 rounded px-3 py-2 text-sm border border-gray-700 focus:outline-none focus:border-blue-500"
          />
          <button
            onClick={() => handleSend(input)}
            className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded text-sm font-medium"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

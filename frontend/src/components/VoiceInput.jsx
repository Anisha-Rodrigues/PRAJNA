import { useState, useRef } from "react";

export default function VoiceInput({ onResult }) {
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState("en-IN");
  const [error, setError] = useState("");
  const recognitionRef = useRef(null);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const isSupported = !!SpeechRecognition;

  const startListening = () => {
    if (!isSupported) {
      setError("Voice input not supported in this browser. Use Chrome.");
      return;
    }
    setError("");
    const recognition = new SpeechRecognition();
    recognition.lang = language;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (e) => {
      setError(`Voice error: ${e.error}`);
      setIsListening(false);
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript, language);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setIsListening(false);
  };

  return (
    <div className="flex items-center gap-2">
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="bg-gray-800 text-white text-sm rounded px-2 py-1 border border-gray-700"
      >
        <option value="en-IN">English</option>
        <option value="kn-IN">ಕನ್ನಡ (Kannada)</option>
      </select>

      <button
        onClick={isListening ? stopListening : startListening}
        className={`px-3 py-1 rounded-full text-sm font-medium transition ${
          isListening ? "bg-red-600 animate-pulse" : "bg-blue-600 hover:bg-blue-500"
        }`}
      >
        {isListening ? "● Listening..." : "🎤 Speak"}
      </button>

      {error && <span className="text-red-400 text-xs">{error}</span>}
    </div>
  );
}

import { useState } from "react";
import { jsPDF } from "jspdf";
import { saveMemory } from "../utils/api";

const PAGE_MARGIN = 14;

function formatTimestamp(date) {
  return date.toISOString().replace(/[:.]/g, "-");
}

function buildPdf({ officerName, officerId, sessionId, canvasNodes, citedFIRs, aiFindings, alerts, dissent }) {
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  const pageWidth = doc.internal.pageSize.getWidth();
  let y = PAGE_MARGIN;

  const line = (text, opts = {}) => {
    const { size = 10, bold = false, gap = 6, color = [30, 30, 30] } = opts;
    doc.setFont("helvetica", bold ? "bold" : "normal");
    doc.setFontSize(size);
    doc.setTextColor(...color);
    const wrapped = doc.splitTextToSize(text, pageWidth - PAGE_MARGIN * 2);
    doc.text(wrapped, PAGE_MARGIN, y);
    y += gap * wrapped.length;
  };

  const rule = () => {
    doc.setDrawColor(180, 180, 180);
    doc.line(PAGE_MARGIN, y, pageWidth - PAGE_MARGIN, y);
    y += 5;
  };

  line("PRAJNA Intelligence Brief", { size: 18, bold: true, gap: 8, color: [15, 23, 42] });
  rule();

  line(`Officer: ${officerName || "Unknown"}`, { size: 10 });
  line(`Badge / ID: ${officerId || "Unknown"}`, { size: 10 });
  line(`Timestamp: ${new Date().toLocaleString("en-IN")}`, { size: 10 });
  if (sessionId) line(`Session ID: ${sessionId}`, { size: 10 });
  y += 2;
  rule();

  line("Case Canvas Summary", { size: 12, bold: true, gap: 7 });
  if (canvasNodes && canvasNodes.length > 0) {
    const counts = canvasNodes.reduce((acc, n) => {
      const type = n.type || "unknown";
      acc[type] = (acc[type] || 0) + 1;
      return acc;
    }, {});
    line(
      Object.entries(counts)
        .map(([type, count]) => `${count} ${type}`)
        .join("  ·  "),
      { size: 10 }
    );
  } else {
    line("No active canvas nodes for this session.", { size: 10, color: [120, 120, 120] });
  }
  y += 2;

  line("FIR Numbers Cited", { size: 12, bold: true, gap: 7 });
  if (citedFIRs && citedFIRs.length > 0) {
    line(citedFIRs.join(", "), { size: 10 });
  } else {
    line("None cited during this session.", { size: 10, color: [120, 120, 120] });
  }
  y += 2;

  line("AI Findings Summary", { size: 12, bold: true, gap: 7 });
  line(aiFindings || "No findings summary available.", { size: 10, gap: 5 });
  y += 2;

  line("Active Anomaly Alerts", { size: 12, bold: true, gap: 7 });
  if (alerts && alerts.length > 0) {
    alerts.forEach((a) => {
      line(`- ${a.district}: pressure score ${Math.round(a.pressure_score)}`, { size: 10, gap: 5 });
    });
  } else {
    line("No active alerts at time of export.", { size: 10, color: [120, 120, 120] });
  }
  y += 2;
  rule();

  line("Officer Dissent Flag", { size: 12, bold: true, gap: 7 });
  const boxSize = 4;
  doc.setDrawColor(30, 30, 30);
  doc.rect(PAGE_MARGIN, y - boxSize + 1, boxSize, boxSize, dissent ? "F" : "S");
  doc.setFontSize(10);
  doc.text(
    dissent
      ? "Checked — officer disagrees with AI findings above."
      : "Unchecked — officer concurs with AI findings above.",
    PAGE_MARGIN + boxSize + 3,
    y
  );

  return doc;
}

export default function IntelligenceBrief({
  officerName,
  officerId,
  sessionId,
  canvasNodes = [],
  citedFIRs = [],
  aiFindings = "",
  alerts = [],
}) {
  const [dissent, setDissent] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);
  const [saved, setSaved] = useState(false);

  async function handleExport() {
    setSaveError(null);
    setSaved(false);

    const doc = buildPdf({ officerName, officerId, sessionId, canvasNodes, citedFIRs, aiFindings, alerts, dissent });
    const filename = `PRAJNA_Intelligence_Brief_${formatTimestamp(new Date())}.pdf`;
    doc.save(filename);

    if (dissent) {
      setSaving(true);
      try {
        await saveMemory(
          officerId || "UNKNOWN",
          "Intelligence Brief Dissent",
          "Officer disagreed with AI findings in Intelligence Brief",
          "dissent"
        );
        setSaved(true);
      } catch (err) {
        setSaveError(err.message || "Failed to record dissent with backend.");
      } finally {
        setSaving(false);
      }
    }
  }

  return (
    <div className="prajna-intel-brief rounded-lg border border-slate-700 bg-slate-900 p-4 text-slate-100 shadow-lg">
      <h3 className="text-sm font-semibold text-slate-200">Intelligence Brief Export</h3>
      <p className="mt-1 text-xs text-slate-400">
        Exports a one-page PDF brief for {officerName || "the current officer"}.
      </p>

      <label className="mt-3 flex items-start gap-2 text-xs text-slate-300">
        <input
          type="checkbox"
          checked={dissent}
          onChange={(e) => setDissent(e.target.checked)}
          className="mt-0.5 h-4 w-4 accent-red-500"
        />
        <span>I disagree with the AI findings in this session (dissent flag)</span>
      </label>

      <button
        onClick={handleExport}
        disabled={saving}
        className="mt-4 w-full rounded-md bg-sky-600 px-3 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {saving ? "Recording dissent…" : "Export Intelligence Brief (PDF)"}
      </button>

      {saved && <p className="mt-2 text-xs text-emerald-400">Dissent recorded and PDF downloaded.</p>}
      {saveError && (
        <p className="mt-2 text-xs text-red-400">
          PDF downloaded, but dissent failed to save: {saveError}
        </p>
      )}
    </div>
  );
}
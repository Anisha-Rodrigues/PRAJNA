import { useEffect, useRef, useState, useCallback } from "react";
import { getPressure, getAlerts } from "../utils/api";
import "leaflet/dist/leaflet.css";

const KARNATAKA_CENTER = [15.3173, 75.7139];
const DEFAULT_ZOOM = 7;

function normalizeZone(raw) {
  return {
    zone_id: raw.zone_id ?? raw.id ?? raw.zoneId,
    district: raw.district ?? raw.district_name ?? "Unknown district",
    latitude: raw.latitude ?? raw.lat,
    longitude: raw.longitude ?? raw.lng ?? raw.lon,
    pressure_score: raw.pressure_score ?? raw.pressureScore ?? raw.score ?? 0,
    bail_release_factor: raw.bail_release_factor ?? raw.bailReleaseFactor ?? 0,
    festival_factor: raw.festival_factor ?? raw.festivalFactor ?? 0,
    economic_stress_factor: raw.economic_stress_factor ?? raw.economicStressFactor ?? 0,
    infrastructure_factor: raw.infrastructure_factor ?? raw.infrastructureFactor ?? 0,
    explanation: raw.explanation ?? "",
    patrol_recommendation: raw.patrol_recommendation ?? raw.patrolRecommendation ?? "",
  };
}

function pressureLevel(score) {
  if (score >= 70) return "high";
  if (score >= 40) return "medium";
  return "low";
}

const LEVEL_COLORS = {
  low: "#22c55e",
  medium: "#f59e0b",
  high: "#ef4444",
};

function hexIconHtml(color, pulse) {
  return `
    <div class="prajna-hex-marker ${pulse ? "prajna-hex-pulse" : ""}" style="--hex-color:${color}">
      <svg viewBox="0 0 100 100" width="34" height="34">
        <polygon
          points="50,3 95,26 95,74 50,97 5,74 5,26"
          fill="${color}"
          fill-opacity="0.85"
          stroke="#0f172a"
          stroke-width="4"
        />
      </svg>
    </div>
  `;
}

export default function PressureMap() {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markersRef = useRef([]);
  const leafletRef = useRef(null);

  const [zones, setZones] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedZone, setSelectedZone] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mapLoadError, setMapLoadError] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const [zoneData, alertData] = await Promise.all([
          getPressure(),
          getAlerts().catch(() => []),
        ]);
        if (cancelled) return;
        setZones(Array.isArray(zoneData) ? zoneData.map(normalizeZone) : []);
        setAlerts(
          Array.isArray(alertData)
            ? alertData.map((a) => ({
                alert_id: a.alert_id ?? a.id ?? `${a.zone_id ?? a.district}-alert`,
                zone_id: a.zone_id ?? a.id,
                district: a.district ?? a.district_name ?? "Unknown district",
                pressure_score: a.pressure_score ?? a.pressureScore ?? a.score ?? 0,
              }))
            : []
        );
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load pressure zones.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadData();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    async function initMap() {
      try {
        const L = await import("leaflet");
        if (!mounted) return;
        leafletRef.current = L.default || L;

        if (!mapContainerRef.current || mapRef.current) return;

        const map = leafletRef.current.map(mapContainerRef.current, {
          center: KARNATAKA_CENTER,
          zoom: DEFAULT_ZOOM,
          scrollWheelZoom: true,
        });

        leafletRef.current
          .tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: "&copy; OpenStreetMap contributors",
          })
          .addTo(map);

        mapRef.current = map;
      } catch (err) {
        console.error("Leaflet failed to load:", err);
        if (mounted) setMapLoadError(true);
      }
    }

    initMap();

    return () => {
      mounted = false;
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  const alertZoneIds = new Set(alerts.map((a) => a.zone_id));

  useEffect(() => {
    const L = leafletRef.current;
    const map = mapRef.current;
    if (!L || !map || mapLoadError) return;

    markersRef.current.forEach((m) => map.removeLayer(m));
    markersRef.current = [];

    zones.forEach((zone) => {
      if (typeof zone.latitude !== "number" || typeof zone.longitude !== "number") return;

      const level = pressureLevel(zone.pressure_score);
      const color = LEVEL_COLORS[level];
      const isAlert = alertZoneIds.has(zone.zone_id);

      const icon = L.divIcon({
        className: "prajna-hex-icon-wrapper",
        html: hexIconHtml(color, isAlert),
        iconSize: [34, 34],
        iconAnchor: [17, 17],
      });

      const marker = L.marker([zone.latitude, zone.longitude], { icon }).addTo(map);
      marker.on("click", () => setSelectedZone(zone));
      marker.bindTooltip(`${zone.district} · ${Math.round(zone.pressure_score)}`, {
        direction: "top",
        offset: [0, -14],
      });

      markersRef.current.push(marker);
    });
  }, [zones, alerts, mapLoadError]);

  const focusZone = useCallback(
    (zoneId) => {
      const zone = zones.find((z) => z.zone_id === zoneId);
      if (!zone || !mapRef.current) return;
      mapRef.current.setView([zone.latitude, zone.longitude], 10, { animate: true });
      setSelectedZone(zone);
    },
    [zones]
  );

  return (
    <div className="prajna-pressure-map flex h-full w-full bg-slate-950 text-slate-100">
      <div className="relative flex-1">
        <div className="absolute top-4 left-4 z-[500] rounded-lg bg-slate-900/90 border border-slate-700 px-4 py-3 shadow-lg backdrop-blur">
          <h2 className="text-sm font-semibold tracking-wide text-slate-200">
            Crime Pressure Surface — Karnataka
          </h2>
          <div className="mt-2 flex gap-4 text-xs text-slate-300">
            {Object.entries(LEVEL_COLORS).map(([level, color]) => (
              <div key={level} className="flex items-center gap-1.5">
                <span className="inline-block h-3 w-3 rounded-sm" style={{ backgroundColor: color }} />
                <span className="capitalize">{level}</span>
              </div>
            ))}
          </div>
        </div>

        {alerts.length > 0 && (
          <div className="absolute top-4 right-4 z-[500] w-72 rounded-lg border border-red-500/40 bg-red-950/90 px-4 py-3 shadow-lg backdrop-blur">
            <div className="flex items-center gap-2 text-sm font-semibold text-red-300">
              <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" />
              Active Anomaly Alerts ({alerts.length})
            </div>
            <ul className="mt-2 space-y-1.5 max-h-40 overflow-y-auto pr-1">
              {alerts.map((alert) => (
                <li key={alert.alert_id}>
                  <button
                    onClick={() => focusZone(alert.zone_id)}
                    className="w-full text-left text-xs rounded-md bg-slate-900/60 hover:bg-slate-800 px-2 py-1.5 transition-colors"
                  >
                    <span className="font-medium text-red-200">{alert.district}</span>
                    <span className="text-slate-400"> — score {Math.round(alert.pressure_score)}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {loading && (
          <div className="absolute inset-0 z-[400] flex items-center justify-center bg-slate-950/70">
            <span className="text-sm text-slate-300">Loading pressure zones…</span>
          </div>
        )}

        {error && !loading && (
          <div className="absolute inset-0 z-[400] flex items-center justify-center bg-slate-950/80">
            <div className="rounded-lg border border-red-500/40 bg-red-950/60 px-6 py-4 text-center">
              <p className="text-sm text-red-300">Failed to load pressure data.</p>
              <p className="mt-1 text-xs text-slate-400">{error}</p>
            </div>
          </div>
        )}

        {mapLoadError ? (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-sm rounded-lg border border-amber-500/40 bg-amber-950/40 px-6 py-4 text-center">
              <p className="text-sm text-amber-300">The map failed to load in this browser.</p>
              <p className="mt-1 text-xs text-slate-400">
                Leaflet could not initialize. Pressure zone data is still listed below.
              </p>
              <ul className="mt-3 space-y-1 text-left text-xs text-slate-300 max-h-64 overflow-y-auto">
                {zones.map((zone) => (
                  <li key={zone.zone_id}>
                    <button
                      onClick={() => setSelectedZone(zone)}
                      className="w-full text-left rounded px-2 py-1 hover:bg-slate-800"
                    >
                      {zone.district} — {Math.round(zone.pressure_score)}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div ref={mapContainerRef} className="h-full w-full" />
        )}
      </div>

      {selectedZone && (
        <aside className="w-96 shrink-0 overflow-y-auto border-l border-slate-800 bg-slate-900 p-5">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-100">{selectedZone.district}</h3>
              <p className="text-xs text-slate-400">Zone {selectedZone.zone_id}</p>
            </div>
            <button
              onClick={() => setSelectedZone(null)}
              className="text-slate-400 hover:text-slate-200"
              aria-label="Close panel"
            >
              ✕
            </button>
          </div>

          <div className="mt-4 flex items-center gap-3">
            <span
              className="inline-block h-3 w-3 rounded-full"
              style={{ backgroundColor: LEVEL_COLORS[pressureLevel(selectedZone.pressure_score)] }}
            />
            <span className="text-2xl font-bold text-slate-100">
              {Math.round(selectedZone.pressure_score)}
            </span>
            <span className="text-xs uppercase tracking-wide text-slate-400">
              {pressureLevel(selectedZone.pressure_score)} pressure
            </span>
          </div>

          <div className="mt-5 space-y-3">
            <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Score Breakdown</h4>
            <BreakdownBar label="Bail releases" value={selectedZone.bail_release_factor} weight="40%" />
            <BreakdownBar label="Festivals" value={selectedZone.festival_factor} weight="30%" />
            <BreakdownBar label="Economic stress" value={selectedZone.economic_stress_factor} weight="20%" />
            <BreakdownBar label="Infrastructure" value={selectedZone.infrastructure_factor} weight="10%" />
          </div>

          <div className="mt-5">
            <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-400">AI Explanation</h4>
            <p className="mt-1.5 text-sm leading-relaxed text-slate-200">
              {selectedZone.explanation || "No explanation provided by the backend."}
            </p>
          </div>

          <div className="mt-5">
            <h4 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Patrol Recommendation</h4>
            <p className="mt-1.5 rounded-md border border-sky-800 bg-sky-950/40 px-3 py-2 text-sm text-sky-200">
              {selectedZone.patrol_recommendation || "No recommendation provided."}
            </p>
          </div>
        </aside>
      )}

      <style>{`
        .prajna-hex-marker { display: flex; align-items: center; justify-content: center; }
        .prajna-hex-pulse svg { animation: prajna-pulse 1.4s ease-in-out infinite; }
        @keyframes prajna-pulse {
          0%, 100% { filter: drop-shadow(0 0 0 var(--hex-color)); }
          50% { filter: drop-shadow(0 0 6px var(--hex-color)); }
        }
        .leaflet-container { background: #0f172a; }
      `}</style>
    </div>
  );
}

function BreakdownBar({ label, value, weight }) {
  const pct = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div>
      <div className="flex items-center justify-between text-xs text-slate-300">
        <span>
          {label} <span className="text-slate-500">({weight})</span>
        </span>
        <span>{Math.round(pct)}</span>
      </div>
      <div className="mt-1 h-1.5 w-full rounded-full bg-slate-800">
        <div className="h-1.5 rounded-full bg-sky-500" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

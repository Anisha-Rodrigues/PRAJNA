# PRAJNA — KSP Crime Intelligence Platform
**Unified AI Platform built for KSP Datathon 2026 (Challenges 01 & 02)**
PRAJNA (Predictive Reasoning & Adaptive Justice Network for Action) is a unified AI platform that fuses conversational graph reasoning for investigators (Challenge 01) with predictive crime pressure analytics across Karnataka (Challenge 02) through a shared **Crime Intelligence Graph**.
---
## 🌟 Key Features
1. **Case Canvas (Spatial Node Graph)**: Full-screen zoomable D3.js force-directed graph with color-coded nodes:
   - 🔴 **Suspects** (Red)
   - 🔵 **FIRs** (Blue)
   - 🟢 **Locations / Jurisdictions** (Green)
   - 🟡 **Evidence Artifacts** (Yellow)
2. **Conversational AI & Voice Querying**: Text + Browser-native Web Speech API voice input with automatic language support for **English (`en-IN`)** and **Kannada (`kn-IN`)**.
3. **Memory Weaving Engine**: Captures every query, AI finding, and outcome tag as an immutable memory thread.
4. **Crime Pressure Map**: Leaflet.js heatmap & zone breakdown across Karnataka calculating risk score based on:
   $$\text{Pressure Score} = (\text{Bail Releases} \times 0.4) + (\text{Festivals} \times 0.3) + (\text{Economic Stress} \times 0.2) + (\text{New ATMs} \times 0.1)$$
5. **Bidirectional Anomaly Alerts**: High-pressure zones detected on the map trigger active alert banners on the Case Canvas chat.
6. **Intelligence Brief PDF Exporter**: Generates 1-page official PDF reports using jsPDF client-side, featuring an interactive **Officer Dissent Flag** feedback mechanism.
---
## 📁 Project Folder Structure
```
prajna/
├── backend/
│   ├── main.py              # FastAPI app with CORS & endpoints
│   ├── mock_db.py           # Suspects, FIRs, evidence & zone dataset
│   ├── query_engine.py      # Pattern-matching NLP query processor
│   ├── memory_weaving.py    # Memory thread logger & dissent tracker
│   ├── pressure_engine.py   # Crime pressure score calculator
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── package.json         # React 18, Vite, D3, Leaflet, jsPDF
│   ├── index.html           # Tailwind CSS CDN + Google Fonts

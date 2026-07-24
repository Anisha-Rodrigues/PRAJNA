"""
PRAJNA — Mock Database
======================

Centralized mock data layer for the PRAJNA Crime Intelligence Platform.

This module intentionally keeps data structures separate from the FastAPI
application so that the mock database can later be replaced by a real
database or Zoho Catalyst Data Store without changing the API layer.
"""

from copy import deepcopy


# ---------------------------------------------------------------------------
# SUSPECTS
# ---------------------------------------------------------------------------

SUSPECTS = {
    "S001": {
        "id": "S001",
        "name": "Raju Kumar",
        "aliases": ["Raju"],
        "risk_level": "high",
        "status": "active",
        "bail_status": "on_bail",
        "bail_release_date": "2024-11-15",
        "district": "Bengaluru Urban",
        "known_associates": ["S002", "S004"],
        "linked_firs": [
            "KA/BLR/2024/001",
            "KA/BLR/2024/002",
            "KA/BLR/2024/005",
        ],
        "crime_types": ["theft", "robbery", "ATM skimming"],
        "known_locations": [
            "Whitefield",
            "Marathahalli",
        ],
        "description": (
            "High-risk suspect linked to multiple theft and robbery cases. "
            "Known associates include Suresh Naik and Vikram Shetty."
        ),
    },
    "S002": {
        "id": "S002",
        "name": "Suresh Naik",
        "aliases": ["Suresh"],
        "risk_level": "medium",
        "status": "active",
        "bail_status": "not_on_bail",
        "bail_release_date": None,
        "district": "Bengaluru Urban",
        "known_associates": ["S001", "S003"],
        "linked_firs": [
            "KA/BLR/2024/001",
            "KA/BLR/2024/003",
        ],
        "crime_types": ["theft", "burglary"],
        "known_locations": [
            "Whitefield",
            "Indiranagar",
        ],
        "description": (
            "Medium-risk suspect associated with theft and burglary cases "
            "in Bengaluru."
        ),
    },
    "S003": {
        "id": "S003",
        "name": "Mohammed Irfan",
        "aliases": ["Irfan", "Mohammed"],
        "risk_level": "medium",
        "status": "active",
        "bail_status": "on_bail",
        "bail_release_date": "2024-12-01",
        "district": "Mysuru",
        "known_associates": ["S002"],
        "linked_firs": [
            "KA/BLR/2024/003",
            "KA/MYS/2024/001",
        ],
        "crime_types": ["burglary", "assault"],
        "known_locations": [
            "Indiranagar",
            "Mysuru",
        ],
        "description": (
            "Medium-risk suspect linked to burglary and assault cases "
            "across Bengaluru and Mysuru."
        ),
    },
    "S004": {
        "id": "S004",
        "name": "Vikram Shetty",
        "aliases": ["Vikram"],
        "risk_level": "high",
        "status": "absconding",
        "bail_status": "not_on_bail",
        "bail_release_date": None,
        "district": "Bengaluru Urban",
        "known_associates": ["S001"],
        "linked_firs": [
            "KA/BLR/2024/004",
            "KA/BLR/2024/005",
        ],
        "crime_types": ["fraud", "theft", "ATM skimming"],
        "known_locations": [
            "Electronic City",
            "Whitefield",
        ],
        "description": (
            "High-risk absconding suspect linked to fraud, theft, and "
            "ATM skimming cases."
        ),
    },
}


# ---------------------------------------------------------------------------
# FIR RECORDS
# ---------------------------------------------------------------------------

FIRS = {
    "KA/BLR/2024/001": {
        "fir_id": "KA/BLR/2024/001",
        "short_id": "001",
        "district": "Bengaluru Urban",
        "police_station": "Whitefield Police Station",
        "year": 2024,
        "crime_type": "theft",
        "crime_types": ["theft"],
        "location": "Whitefield",
        "date": "2024-03-15",
        "status": "under_investigation",
        "suspect_ids": ["S001", "S002"],
        "suspect_names": ["Raju Kumar", "Suresh Naik"],
        "evidence_ids": ["E001", "E002"],
        "description": (
            "Reported theft incident in the Whitefield area involving "
            "Raju Kumar and Suresh Naik."
        ),
    },
    "KA/BLR/2024/002": {
        "fir_id": "KA/BLR/2024/002",
        "short_id": "002",
        "district": "Bengaluru Urban",
        "police_station": "Marathahalli Police Station",
        "year": 2024,
        "crime_type": "robbery",
        "crime_types": ["robbery"],
        "location": "Marathahalli",
        "date": "2024-04-22",
        "status": "under_investigation",
        "suspect_ids": ["S001"],
        "suspect_names": ["Raju Kumar"],
        "evidence_ids": ["E003"],
        "description": (
            "Robbery case reported in Marathahalli with Raju Kumar "
            "identified as the primary suspect."
        ),
    },
    "KA/BLR/2024/003": {
        "fir_id": "KA/BLR/2024/003",
        "short_id": "003",
        "district": "Bengaluru Urban",
        "police_station": "Indiranagar Police Station",
        "year": 2024,
        "crime_type": "burglary",
        "crime_types": ["burglary"],
        "location": "Indiranagar",
        "date": "2024-05-10",
        "status": "under_investigation",
        "suspect_ids": ["S002", "S003"],
        "suspect_names": ["Suresh Naik", "Mohammed Irfan"],
        "evidence_ids": ["E004", "E005"],
        "description": (
            "Burglary case in Indiranagar linked to Suresh Naik and "
            "Mohammed Irfan."
        ),
    },
    "KA/MYS/2024/001": {
        "fir_id": "KA/MYS/2024/001",
        "short_id": "MYS001",
        "district": "Mysuru",
        "police_station": "Mysuru City Police Station",
        "year": 2024,
        "crime_type": "assault",
        "crime_types": ["assault"],
        "location": "Mysuru",
        "date": "2024-06-18",
        "status": "under_investigation",
        "suspect_ids": ["S003"],
        "suspect_names": ["Mohammed Irfan"],
        "evidence_ids": ["E006"],
        "description": (
            "Assault case reported in Mysuru involving Mohammed Irfan."
        ),
    },
    "KA/BLR/2024/004": {
        "fir_id": "KA/BLR/2024/004",
        "short_id": "004",
        "district": "Bengaluru Urban",
        "police_station": "Electronic City Police Station",
        "year": 2024,
        "crime_type": "fraud",
        "crime_types": ["fraud"],
        "location": "Electronic City",
        "date": "2024-07-05",
        "status": "under_investigation",
        "suspect_ids": ["S004"],
        "suspect_names": ["Vikram Shetty"],
        "evidence_ids": ["E007", "E008"],
        "description": (
            "Fraud investigation in Electronic City involving absconding "
            "suspect Vikram Shetty."
        ),
    },
    "KA/BLR/2024/005": {
        "fir_id": "KA/BLR/2024/005",
        "short_id": "005",
        "district": "Bengaluru Urban",
        "police_station": "Whitefield Police Station",
        "year": 2024,
        "crime_type": "theft",
        "crime_types": ["theft", "ATM skimming"],
        "location": "Whitefield",
        "date": "2024-08-12",
        "status": "under_investigation",
        "suspect_ids": ["S001", "S004"],
        "suspect_names": ["Raju Kumar", "Vikram Shetty"],
        "evidence_ids": ["E009", "E010"],
        "description": (
            "Theft and ATM skimming case in Whitefield linked to Raju Kumar "
            "and Vikram Shetty."
        ),
    },
}


# ---------------------------------------------------------------------------
# LOCATIONS
# ---------------------------------------------------------------------------

LOCATIONS = {
    "L001": {
        "id": "L001",
        "name": "Whitefield",
        "district": "Bengaluru Urban",
        "latitude": 12.9698,
        "longitude": 77.7500,
        "type": "crime_location",
    },
    "L002": {
        "id": "L002",
        "name": "Marathahalli",
        "district": "Bengaluru Urban",
        "latitude": 12.9591,
        "longitude": 77.6974,
        "type": "crime_location",
    },
    "L003": {
        "id": "L003",
        "name": "Indiranagar",
        "district": "Bengaluru Urban",
        "latitude": 12.9784,
        "longitude": 77.6408,
        "type": "crime_location",
    },
    "L004": {
        "id": "L004",
        "name": "Mysuru",
        "district": "Mysuru",
        "latitude": 12.2958,
        "longitude": 76.6394,
        "type": "crime_location",
    },
    "L005": {
        "id": "L005",
        "name": "Electronic City",
        "district": "Bengaluru Urban",
        "latitude": 12.8452,
        "longitude": 77.6602,
        "type": "crime_location",
    },
}


# ---------------------------------------------------------------------------
# EVIDENCE
# ---------------------------------------------------------------------------

EVIDENCE = {
    "E001": {
        "id": "E001",
        "type": "CCTV",
        "description": "CCTV footage from Whitefield commercial area",
        "linked_firs": ["KA/BLR/2024/001"],
    },
    "E002": {
        "id": "E002",
        "type": "fingerprint",
        "description": "Fingerprint evidence collected at the theft location",
        "linked_firs": ["KA/BLR/2024/001"],
    },
    "E003": {
        "id": "E003",
        "type": "vehicle",
        "description": "Vehicle identified near the Marathahalli robbery scene",
        "linked_firs": ["KA/BLR/2024/002"],
    },
    "E004": {
        "id": "E004",
        "type": "CCTV",
        "description": "CCTV footage from an Indiranagar residential building",
        "linked_firs": ["KA/BLR/2024/003"],
    },
    "E005": {
        "id": "E005",
        "type": "fingerprint",
        "description": "Fingerprint evidence from burglary entry point",
        "linked_firs": ["KA/BLR/2024/003"],
    },
    "E006": {
        "id": "E006",
        "type": "witness",
        "description": "Witness statement recorded in Mysuru assault investigation",
        "linked_firs": ["KA/MYS/2024/001"],
    },
    "E007": {
        "id": "E007",
        "type": "digital",
        "description": "Digital transaction records related to suspected fraud",
        "linked_firs": ["KA/BLR/2024/004"],
    },
    "E008": {
        "id": "E008",
        "type": "document",
        "description": "Financial documents collected during fraud investigation",
        "linked_firs": ["KA/BLR/2024/004"],
    },
    "E009": {
        "id": "E009",
        "type": "ATM",
        "description": "ATM transaction records showing suspicious activity",
        "linked_firs": ["KA/BLR/2024/005"],
    },
    "E010": {
        "id": "E010",
        "type": "CCTV",
        "description": "ATM surveillance footage from Whitefield",
        "linked_firs": ["KA/BLR/2024/005"],
    },
}


# ---------------------------------------------------------------------------
# CRIMINAL NETWORK RELATIONSHIPS
# ---------------------------------------------------------------------------

NETWORK_EDGES = [
    {
        "source": "S001",
        "target": "S002",
        "relationship": "co-accused",
        "confidence": 0.92,
        "linked_firs": ["KA/BLR/2024/001"],
    },
    {
        "source": "S001",
        "target": "S004",
        "relationship": "co-accused",
        "confidence": 0.94,
        "linked_firs": ["KA/BLR/2024/005"],
    },
    {
        "source": "S002",
        "target": "S003",
        "relationship": "co-accused",
        "confidence": 0.88,
        "linked_firs": ["KA/BLR/2024/003"],
    },
    {
        "source": "S001",
        "target": "L001",
        "relationship": "same location",
        "confidence": 0.96,
        "linked_firs": [
            "KA/BLR/2024/001",
            "KA/BLR/2024/005",
        ],
    },
    {
        "source": "S002",
        "target": "L001",
        "relationship": "same location",
        "confidence": 0.85,
        "linked_firs": ["KA/BLR/2024/001"],
    },
    {
        "source": "S001",
        "target": "L002",
        "relationship": "same location",
        "confidence": 0.82,
        "linked_firs": ["KA/BLR/2024/002"],
    },
    {
        "source": "S002",
        "target": "L003",
        "relationship": "same location",
        "confidence": 0.84,
        "linked_firs": ["KA/BLR/2024/003"],
    },
    {
        "source": "S003",
        "target": "L003",
        "relationship": "same location",
        "confidence": 0.84,
        "linked_firs": ["KA/BLR/2024/003"],
    },
    {
        "source": "S003",
        "target": "L004",
        "relationship": "same location",
        "confidence": 0.91,
        "linked_firs": ["KA/MYS/2024/001"],
    },
    {
        "source": "S004",
        "target": "L005",
        "relationship": "same location",
        "confidence": 0.90,
        "linked_firs": ["KA/BLR/2024/004"],
    },
    {
        "source": "S004",
        "target": "L001",
        "relationship": "same location",
        "confidence": 0.89,
        "linked_firs": ["KA/BLR/2024/005"],
    },
]


# ---------------------------------------------------------------------------
# BAIL RELEASE DATA
# ---------------------------------------------------------------------------

BAIL_RELEASES = [
    {
        "suspect_id": "S001",
        "suspect_name": "Raju Kumar",
        "district": "Bengaluru Urban",
        "release_date": "2024-11-15",
        "status": "on_bail",
    },
    {
        "suspect_id": "S003",
        "suspect_name": "Mohammed Irfan",
        "district": "Mysuru",
        "release_date": "2024-12-01",
        "status": "on_bail",
    },
]


# ---------------------------------------------------------------------------
# FESTIVAL / EVENT DATA
# ---------------------------------------------------------------------------

FESTIVAL_EVENTS = [
    {
        "id": "F001",
        "name": "Bengaluru Karaga",
        "district": "Bengaluru Urban",
        "zone": "Whitefield",
        "event_date": "2025-04-12",
        "activity_level": 0.85,
    },
    {
        "id": "F002",
        "name": "Dasara Festival",
        "district": "Mysuru",
        "zone": "Mysuru",
        "event_date": "2025-10-02",
        "activity_level": 0.95,
    },
    {
        "id": "F003",
        "name": "Local Cultural Festival",
        "district": "Bengaluru Urban",
        "zone": "Indiranagar",
        "event_date": "2025-03-20",
        "activity_level": 0.60,
    },
    {
        "id": "F004",
        "name": "Tech Corridor Event",
        "district": "Bengaluru Urban",
        "zone": "Electronic City",
        "event_date": "2025-06-15",
        "activity_level": 0.55,
    },
]


# ---------------------------------------------------------------------------
# ECONOMIC STRESS DATA
# ---------------------------------------------------------------------------

ECONOMIC_STRESS = {
    "Whitefield": {
        "district": "Bengaluru Urban",
        "index": 0.55,
        "trend": "stable",
    },
    "Marathahalli": {
        "district": "Bengaluru Urban",
        "index": 0.62,
        "trend": "rising",
    },
    "Indiranagar": {
        "district": "Bengaluru Urban",
        "index": 0.35,
        "trend": "stable",
    },
    "Mysuru": {
        "district": "Mysuru",
        "index": 0.48,
        "trend": "stable",
    },
    "Electronic City": {
        "district": "Bengaluru Urban",
        "index": 0.68,
        "trend": "rising",
    },
}


# ---------------------------------------------------------------------------
# INFRASTRUCTURE SIGNALS
# ---------------------------------------------------------------------------

INFRASTRUCTURE_SIGNALS = {
    "Whitefield": {
        "new_atms": 8,
        "new_commercial_units": 12,
        "infrastructure_index": 0.80,
    },
    "Marathahalli": {
        "new_atms": 5,
        "new_commercial_units": 8,
        "infrastructure_index": 0.55,
    },
    "Indiranagar": {
        "new_atms": 3,
        "new_commercial_units": 5,
        "infrastructure_index": 0.35,
    },
    "Mysuru": {
        "new_atms": 6,
        "new_commercial_units": 7,
        "infrastructure_index": 0.60,
    },
    "Electronic City": {
        "new_atms": 10,
        "new_commercial_units": 15,
        "infrastructure_index": 0.90,
    },
}


# ---------------------------------------------------------------------------
# PRESSURE ZONE BASE DATA
# ---------------------------------------------------------------------------

PRESSURE_ZONES = [
    {
        "zone_id": "Z001",
        "zone_name": "Whitefield",
        "district": "Bengaluru Urban",
        "latitude": 12.9698,
        "longitude": 77.7500,
    },
    {
        "zone_id": "Z002",
        "zone_name": "Marathahalli",
        "district": "Bengaluru Urban",
        "latitude": 12.9591,
        "longitude": 77.6974,
    },
    {
        "zone_id": "Z003",
        "zone_name": "Indiranagar",
        "district": "Bengaluru Urban",
        "latitude": 12.9784,
        "longitude": 77.6408,
    },
    {
        "zone_id": "Z004",
        "zone_name": "Mysuru",
        "district": "Mysuru",
        "latitude": 12.2958,
        "longitude": 76.6394,
    },
    {
        "zone_id": "Z005",
        "zone_name": "Electronic City",
        "district": "Bengaluru Urban",
        "latitude": 12.8452,
        "longitude": 77.6602,
    },
]


# ---------------------------------------------------------------------------
# INITIAL ALERTS
# ---------------------------------------------------------------------------

ALERTS = [
    {
        "alert_id": "A001",
        "zone_id": "Z001",
        "zone_name": "Whitefield",
        "alert_type": "high_pressure",
        "severity": "high",
        "message": (
            "Whitefield has elevated crime pressure based on combined "
            "bail, festival, economic, and infrastructure signals."
        ),
        "active": True,
    },
    {
        "alert_id": "A002",
        "zone_id": "Z005",
        "zone_name": "Electronic City",
        "alert_type": "high_pressure",
        "severity": "high",
        "message": (
            "Electronic City shows elevated pressure due to infrastructure "
            "growth and rising economic stress indicators."
        ),
        "active": True,
    },
]


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def get_all_suspects():
    """Return a copy of all suspect records."""
    return deepcopy(list(SUSPECTS.values()))


def get_all_firs():
    """Return a copy of all FIR records."""
    return deepcopy(list(FIRS.values()))


def get_suspect_by_id(suspect_id):
    """Return a suspect by ID or None if not found."""
    suspect = SUSPECTS.get(suspect_id)
    return deepcopy(suspect) if suspect else None


def get_fir_by_id(fir_id):
    """Return an FIR by full FIR number or None if not found."""
    fir = FIRS.get(fir_id)
    return deepcopy(fir) if fir else None


def get_active_alerts():
    """Return all currently active anomaly alerts."""
    return deepcopy([
        alert for alert in ALERTS
        if alert.get("active") is True
    ])


def get_network_data():
    """
    Return a graph-ready network containing suspects, FIRs,
    locations, evidence, and their relationships.
    """

    nodes = []
    edges = []

    for suspect in SUSPECTS.values():
        nodes.append({
            "id": suspect["id"],
            "label": suspect["name"],
            "type": "suspect",
            "risk_level": suspect["risk_level"],
            "status": suspect["status"],
            "data": deepcopy(suspect),
        })

    for fir in FIRS.values():
        nodes.append({
            "id": f"FIR:{fir['fir_id']}",
            "label": fir["short_id"],
            "type": "fir",
            "crime_type": fir["crime_type"],
            "data": deepcopy(fir),
        })

    for location in LOCATIONS.values():
        nodes.append({
            "id": location["id"],
            "label": location["name"],
            "type": "location",
            "data": deepcopy(location),
        })

    for evidence in EVIDENCE.values():
        nodes.append({
            "id": evidence["id"],
            "label": evidence["type"],
            "type": "evidence",
            "data": deepcopy(evidence),
        })

    edges.extend(deepcopy(NETWORK_EDGES))

    for fir in FIRS.values():
        fir_node_id = f"FIR:{fir['fir_id']}"

        for suspect_id in fir["suspect_ids"]:
            edges.append({
                "source": suspect_id,
                "target": fir_node_id,
                "relationship": "linked to FIR",
                "confidence": 1.0,
                "linked_firs": [fir["fir_id"]],
            })

        location_id = next(
            (
                location_id
                for location_id, location in LOCATIONS.items()
                if location["name"] == fir["location"]
            ),
            None,
        )

        if location_id:
            edges.append({
                "source": fir_node_id,
                "target": location_id,
                "relationship": "reported at",
                "confidence": 1.0,
                "linked_firs": [fir["fir_id"]],
            })

        for evidence_id in fir["evidence_ids"]:
            edges.append({
                "source": fir_node_id,
                "target": evidence_id,
                "relationship": "supported by evidence",
                "confidence": 1.0,
                "linked_firs": [fir["fir_id"]],
            })

    return {
        "nodes": nodes,
        "edges": edges,
    }
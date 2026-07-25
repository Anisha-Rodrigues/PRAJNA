"""
PRAJNA — Crime Pressure Engine
==============================

Calculates predictive crime pressure scores for geographic zones.

Formula:

Pressure Score =
    Bail Releases       * 0.40
    + Festivals         * 0.30
    + Economic Stress   * 0.20
    + Infrastructure    * 0.10

All component values are normalized between 0.0 and 1.0.
"""

from copy import deepcopy

from mock_db import (
    BAIL_RELEASES,
    ECONOMIC_STRESS,
    FESTIVAL_EVENTS,
    INFRASTRUCTURE_SIGNALS,
    PRESSURE_ZONES,
)


PRESSURE_WEIGHTS = {
    "bail_releases": 0.4,
    "festivals": 0.3,
    "economic_stress": 0.2,
    "infrastructure": 0.1,
}


def clamp(value):
    """Keep a numeric value between 0 and 1."""

    return max(
        0.0,
        min(
            1.0,
            float(value),
        ),
    )


def calculate_bail_score(zone_name, district):
    """
    Calculate bail-release pressure.

    A zone receives higher pressure when suspects from the same district
    are currently on bail.
    """

    releases = [
        release
        for release in BAIL_RELEASES
        if release.get("status") == "on_bail"
        and (
            release.get("district") == district
            or release.get("district") == zone_name
        )
    ]

    if not releases:
        return 0.0

    # Normalize the number of bail releases.
    # Two or more releases saturate this component at 1.0.
    return clamp(len(releases) / 2.0)


def calculate_festival_score(zone_name):
    """
    Calculate festival/event pressure for a zone.
    """

    events = [
        event
        for event in FESTIVAL_EVENTS
        if event.get("zone") == zone_name
    ]

    if not events:
        return 0.0

    return clamp(
        max(
            event.get("activity_level", 0.0)
            for event in events
        )
    )


def calculate_economic_score(zone_name):
    """
    Return normalized economic stress score.
    """

    data = ECONOMIC_STRESS.get(zone_name)

    if not data:
        return 0.0

    return clamp(
        data.get("index", 0.0)
    )


def calculate_infrastructure_score(zone_name):
    """
    Return normalized infrastructure activity score.
    """

    data = INFRASTRUCTURE_SIGNALS.get(zone_name)

    if not data:
        return 0.0

    return clamp(
        data.get("infrastructure_index", 0.0)
    )


def get_pressure_level(score):
    """
    Convert numeric pressure into a human-readable level.
    """

    if score >= 0.70:
        return "high"

    if score >= 0.40:
        return "medium"

    return "low"


def build_explanation(
    zone_name,
    score,
    bail_score,
    festival_score,
    economic_score,
    infrastructure_score,
):
    """
    Generate a natural-language explanation of the pressure score.
    """

    drivers = []

    if bail_score >= 0.50:
        drivers.append("recent bail-release activity")

    if festival_score >= 0.50:
        drivers.append("upcoming or significant public events")

    if economic_score >= 0.60:
        drivers.append("elevated economic stress")

    if infrastructure_score >= 0.70:
        drivers.append("rapid infrastructure and ATM growth")

    if not drivers:
        drivers.append("relatively limited risk signals")

    if len(drivers) == 1:
        driver_text = drivers[0]
    elif len(drivers) == 2:
        driver_text = f"{drivers[0]} and {drivers[1]}"
    else:
        driver_text = (
            ", ".join(drivers[:-1])
            + f", and {drivers[-1]}"
        )

    level = get_pressure_level(score)

    return (
        f"{zone_name} has a {level} predictive crime pressure score "
        f"of {score:.2f}. The primary contributing signals are "
        f"{driver_text}. This score is an analytical indicator for "
        f"prioritizing preventive policing and should be interpreted "
        f"alongside current field intelligence."
    )


def build_patrol_recommendation(
    zone_name,
    score,
    bail_score,
    festival_score,
    economic_score,
    infrastructure_score,
):
    """
    Generate a patrol recommendation based on pressure signals.
    """

    recommendations = []

    if score >= 0.70:
        recommendations.append(
            "Increase visible preventive patrol coverage."
        )

    if bail_score >= 0.50:
        recommendations.append(
            "Review recently released individuals and relevant "
            "bail conditions."
        )

    if festival_score >= 0.50:
        recommendations.append(
            "Increase patrol presence around event activity areas."
        )

    if infrastructure_score >= 0.70:
        recommendations.append(
            "Prioritize ATM and newly developed commercial locations."
        )

    if economic_score >= 0.60:
        recommendations.append(
            "Coordinate with local intelligence units to monitor "
            "emerging economic-stress indicators."
        )

    if not recommendations:
        recommendations.append(
            "Maintain routine patrol coverage and continue monitoring "
            "for changes in pressure signals."
        )

    return " ".join(recommendations)


def calculate_zone_pressure(zone):
    """
    Calculate all pressure metrics for a single zone.
    """

    zone_name = zone["zone_name"]
    district = zone["district"]

    bail_score = calculate_bail_score(
        zone_name,
        district,
    )

    festival_score = calculate_festival_score(
        zone_name
    )

    economic_score = calculate_economic_score(
        zone_name
    )

    infrastructure_score = calculate_infrastructure_score(
        zone_name
    )

    pressure_score = (
        bail_score * PRESSURE_WEIGHTS["bail_releases"]
        + festival_score * PRESSURE_WEIGHTS["festivals"]
        + economic_score * PRESSURE_WEIGHTS["economic_stress"]
        + infrastructure_score * PRESSURE_WEIGHTS["infrastructure"]
    )

    pressure_score = round(
        clamp(pressure_score),
        3,
    )

    pressure_level = get_pressure_level(
        pressure_score
    )

    explanation = build_explanation(
        zone_name,
        pressure_score,
        bail_score,
        festival_score,
        economic_score,
        infrastructure_score,
    )

    patrol_recommendation = build_patrol_recommendation(
        zone_name,
        pressure_score,
        bail_score,
        festival_score,
        economic_score,
        infrastructure_score,
    )

    return {
        **deepcopy(zone),
        "pressure_score": pressure_score,
        "pressure_level": pressure_level,
        "breakdown": {
            "bail_release_score": round(
                bail_score,
                3,
            ),
            "festival_score": round(
                festival_score,
                3,
            ),
            "economic_stress_score": round(
                economic_score,
                3,
            ),
            "infrastructure_score": round(
                infrastructure_score,
                3,
            ),
        },
        "explanation": explanation,
        "patrol_recommendation": patrol_recommendation,
    }


def calculate_all_pressure_zones():
    """
    Calculate pressure for every configured zone.
    """

    zones = [
        calculate_zone_pressure(zone)
        for zone in PRESSURE_ZONES
    ]

    zones.sort(
        key=lambda item: item["pressure_score"],
        reverse=True,
    )

    return zones


def get_top_pressure_zones(limit=3):
    """
    Return the highest-pressure zones.
    """

    zones = calculate_all_pressure_zones()

    return zones[:limit]


def generate_pressure_alerts(threshold=0.70):
    """
    Generate active anomaly alerts for zones at or above the threshold.
    """

    zones = calculate_all_pressure_zones()

    alerts = []

    for zone in zones:

        if zone["pressure_score"] < threshold:
            continue

        severity = "critical"

        if zone["pressure_score"] < 0.85:
            severity = "high"

        alerts.append({
            "alert_id": f"PRESSURE-{zone['zone_id']}",
            "zone_id": zone["zone_id"],
            "zone_name": zone["zone_name"],
            "district": zone["district"],
            "alert_type": "high_pressure",
            "severity": severity,
            "pressure_score": zone["pressure_score"],
            "message": (
                f"{zone['zone_name']} has a predictive crime pressure "
                f"score of {zone['pressure_score']:.2f}, exceeding the "
                f"anomaly threshold of {threshold:.2f}."
            ),
            "explanation": zone["explanation"],
            "active": True,
        })

    return alerts


def get_pressure_response():
    """
    Return the complete API-ready pressure response.
    """

    zones = calculate_all_pressure_zones()

    return {
        "zones": zones,
        "weights": deepcopy(
            PRESSURE_WEIGHTS
        ),
        "thresholds": {
            "medium": 0.40,
            "high": 0.70,
            "anomaly": 0.70,
        },
        "summary": {
            "total_zones": len(zones),
            "high_pressure_zones": len([
                zone
                for zone in zones
                if zone["pressure_level"] == "high"
            ]),
            "medium_pressure_zones": len([
                zone
                for zone in zones
                if zone["pressure_level"] == "medium"
            ]),
            "low_pressure_zones": len([
                zone
                for zone in zones
                if zone["pressure_level"] == "low"
            ]),
        },
    }
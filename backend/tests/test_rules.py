from app.schemas import FlightCase
from app.services.rules import validate_case


def test_demo_case_detects_missing_and_time_mismatch():
    case = FlightCase(
        flight_number="GB451",
        origin="MRA",
        destination="IST",
        departure_time="2026-10-15T14:25:00+02:00",
        aircraft_registration="5A-GBR",
        documents=[
            {
                "document_type": "ground_handling_confirmation",
                "present": True,
                "flight_number": "GB451",
                "departure_time": "2026-10-15T14:45:00+02:00",
                "aircraft_registration": "5A-GBR",
            },
            {"document_type": "fuel_confirmation", "present": True},
            {"document_type": "catering_confirmation", "present": False},
        ],
    )
    codes = [f.code for f in validate_case(case)]
    assert "MISSING_DOCUMENT" in codes
    assert "DEPARTURE_TIME_MISMATCH" in codes

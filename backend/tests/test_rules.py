from app.schemas import FlightCase
from app.services.rules import validate_case


def _base_case(**overrides):
    payload = {
        "flight_number": "GB451",
        "origin": "MRA",
        "destination": "IST",
        "departure_time": "2026-10-15T14:25:00+02:00",
        "aircraft_registration": "5A-GBR",
        "profile": {
            "required_documents": [
                "operational_flight_plan",
                "ground_handling_confirmation",
                "load_or_mass_balance",
                "fuel_confirmation",
            ]
        },
        "documents": [
            {"document_type": "operational_flight_plan", "flight_number": "GB451", "origin": "MRA", "destination": "IST", "departure_time": "2026-10-15T14:25:00+02:00", "aircraft_registration": "5A-GBR"},
            {"document_type": "ground_handling_confirmation", "flight_number": "GB451", "origin": "MRA", "destination": "IST", "departure_time": "2026-10-15T14:25:00+02:00", "aircraft_registration": "5A-GBR"},
            {"document_type": "load_or_mass_balance", "flight_number": "GB451", "aircraft_registration": "5A-GBR"},
            {"document_type": "fuel_confirmation", "flight_number": "GB451", "aircraft_registration": "5A-GBR", "service": "fuel", "confirmed": True},
        ],
    }
    payload.update(overrides)
    return FlightCase(**payload)


def _codes(case):
    return [finding.code for finding in validate_case(case)]


def test_detects_missing_required_document():
    case = _base_case()
    case.documents = [doc for doc in case.documents if doc.document_type != "load_or_mass_balance"]
    assert "MISSING_DOCUMENT" in _codes(case)


def test_detects_departure_time_mismatch():
    case = _base_case()
    case.documents[1].departure_time = "2026-10-15T14:45:00+02:00"
    assert "DEPARTURE_TIME_MISMATCH" in _codes(case)


def test_detects_aircraft_mismatch():
    case = _base_case()
    case.documents[2].aircraft_registration = "5A-XYZ"
    assert "AIRCRAFT_MISMATCH" in _codes(case)


def test_detects_stale_revision():
    case = _base_case()
    case.profile.latest_document_revisions = {"ground_handling_confirmation": 2}
    case.documents[1].revision = 1
    assert "STALE_DOCUMENT_REVISION" in _codes(case)


def test_detects_required_service_without_confirmation():
    case = _base_case()
    case.profile.required_services = ["fuel", "catering"]
    assert "MISSING_SERVICE_CONFIRMATION" in _codes(case)


def test_external_check_is_informational_only():
    case = _base_case()
    case.profile.external_checks = ["weather_context", "notam_context"]
    findings = validate_case(case)
    external = [f for f in findings if f.code == "EXTERNAL_CHECK_REQUIRED"]
    assert len(external) == 2
    assert all(f.severity == "info" for f in external)

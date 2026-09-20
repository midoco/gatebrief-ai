from app.schemas import FlightCase, Finding


REQUIRED_DOCUMENTS = {
    "ground_handling_confirmation",
    "fuel_confirmation",
    "catering_confirmation",
}


def validate_case(case: FlightCase) -> list[Finding]:
    findings: list[Finding] = []
    by_type = {doc.document_type: doc for doc in case.documents}

    for required in sorted(REQUIRED_DOCUMENTS):
        doc = by_type.get(required)
        if not doc or not doc.present:
            findings.append(
                Finding(
                    severity="warning",
                    code="MISSING_DOCUMENT",
                    message=f"Required demo document is missing: {required}",
                )
            )

    for doc in case.documents:
        if not doc.present:
            continue
        if doc.flight_number and doc.flight_number != case.flight_number:
            findings.append(
                Finding(
                    severity="critical",
                    code="FLIGHT_NUMBER_MISMATCH",
                    message=(
                        f"{doc.document_type} references flight {doc.flight_number}, "
                        f"but the case is {case.flight_number}."
                    ),
                )
            )
        if doc.aircraft_registration and doc.aircraft_registration != case.aircraft_registration:
            findings.append(
                Finding(
                    severity="critical",
                    code="AIRCRAFT_MISMATCH",
                    message=(
                        f"{doc.document_type} references aircraft {doc.aircraft_registration}, "
                        f"but the case is {case.aircraft_registration}."
                    ),
                )
            )
        if doc.departure_time and doc.departure_time != case.departure_time:
            findings.append(
                Finding(
                    severity="warning",
                    code="DEPARTURE_TIME_MISMATCH",
                    message=(
                        f"{doc.document_type} has departure time {doc.departure_time}, "
                        f"while the flight case has {case.departure_time}."
                    ),
                )
            )

    if not findings:
        findings.append(
            Finding(
                severity="info",
                code="RULE_CHECKS_CLEAR",
                message="No issues were detected by the deterministic demo rules.",
            )
        )

    return findings

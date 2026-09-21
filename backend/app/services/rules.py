from collections import defaultdict
from app.schemas import FlightCase, FlightDocument, Finding


def _norm(value: str | None) -> str | None:
    return value.strip().upper() if value else None


def _evidence(doc: FlightDocument) -> str:
    return doc.source_ref or doc.document_type


def _mismatch(
    findings: list[Finding],
    *,
    code: str,
    severity: str,
    doc: FlightDocument,
    label: str,
    expected: str,
    found: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            message=f"{doc.document_type} has {label} {found}, expected {expected}.",
            document_type=doc.document_type,
            expected_value=expected,
            found_value=found,
            evidence_ref=_evidence(doc),
        )
    )


def validate_case(case: FlightCase) -> list[Finding]:
    findings: list[Finding] = []
    present_documents = [doc for doc in case.documents if doc.present]
    by_type: dict[str, list[FlightDocument]] = defaultdict(list)
    for doc in present_documents:
        by_type[doc.document_type].append(doc)

    for required in sorted(set(case.profile.required_documents)):
        if not by_type.get(required):
            findings.append(
                Finding(
                    severity="warning",
                    code="MISSING_DOCUMENT",
                    message=f"Required flight document is missing: {required}.",
                    document_type=required,
                    expected_value="present",
                    found_value="missing",
                )
            )

    for service in sorted(set(case.profile.required_services)):
        confirmations = [
            doc
            for doc in present_documents
            if _norm(doc.service) == _norm(service) and doc.confirmed is not False
        ]
        if not confirmations:
            findings.append(
                Finding(
                    severity="warning",
                    code="MISSING_SERVICE_CONFIRMATION",
                    message=f"Required service has no positive confirmation: {service}.",
                    expected_value="confirmed",
                    found_value="missing or unconfirmed",
                )
            )

    for doc in present_documents:
        if doc.flight_number and _norm(doc.flight_number) != _norm(case.flight_number):
            _mismatch(
                findings,
                code="FLIGHT_NUMBER_MISMATCH",
                severity="critical",
                doc=doc,
                label="flight number",
                expected=case.flight_number,
                found=doc.flight_number,
            )

        if doc.aircraft_registration and _norm(doc.aircraft_registration) != _norm(case.aircraft_registration):
            _mismatch(
                findings,
                code="AIRCRAFT_MISMATCH",
                severity="critical",
                doc=doc,
                label="aircraft registration",
                expected=case.aircraft_registration,
                found=doc.aircraft_registration,
            )

        if doc.origin and _norm(doc.origin) != _norm(case.origin):
            _mismatch(
                findings,
                code="ORIGIN_MISMATCH",
                severity="critical",
                doc=doc,
                label="origin",
                expected=case.origin,
                found=doc.origin,
            )

        if doc.destination and _norm(doc.destination) != _norm(case.destination):
            _mismatch(
                findings,
                code="DESTINATION_MISMATCH",
                severity="critical",
                doc=doc,
                label="destination",
                expected=case.destination,
                found=doc.destination,
            )

        if doc.departure_time and doc.departure_time != case.departure_time:
            _mismatch(
                findings,
                code="DEPARTURE_TIME_MISMATCH",
                severity="warning",
                doc=doc,
                label="departure time",
                expected=case.departure_time,
                found=doc.departure_time,
            )

        expected_revision = case.profile.latest_document_revisions.get(doc.document_type)
        if expected_revision is not None and doc.revision is not None and doc.revision < expected_revision:
            findings.append(
                Finding(
                    severity="warning",
                    code="STALE_DOCUMENT_REVISION",
                    message=(
                        f"{doc.document_type} is revision {doc.revision}; "
                        f"revision {expected_revision} is expected."
                    ),
                    document_type=doc.document_type,
                    expected_value=str(expected_revision),
                    found_value=str(doc.revision),
                    evidence_ref=_evidence(doc),
                )
            )

    for document_type, docs in by_type.items():
        if len(docs) < 2:
            continue
        signatures = {
            (
                _norm(doc.flight_number),
                _norm(doc.origin),
                _norm(doc.destination),
                doc.departure_time,
                _norm(doc.aircraft_registration),
                doc.revision,
            )
            for doc in docs
        }
        if len(signatures) > 1:
            findings.append(
                Finding(
                    severity="warning",
                    code="DUPLICATE_DOCUMENT_CONFLICT",
                    message=f"Multiple {document_type} documents contain conflicting operational data.",
                    document_type=document_type,
                    evidence_ref=", ".join(_evidence(doc) for doc in docs),
                )
            )

    for check in sorted(set(case.profile.external_checks)):
        findings.append(
            Finding(
                severity="info",
                code="EXTERNAL_CHECK_REQUIRED",
                message=f"Fresh external verification is requested for: {check}.",
                source="workflow",
                expected_value="fresh external evidence",
                found_value="pending research",
            )
        )

    if not findings:
        findings.append(
            Finding(
                severity="info",
                code="RULE_CHECKS_CLEAR",
                message="No issues were detected by the deterministic rules engine.",
            )
        )

    return findings

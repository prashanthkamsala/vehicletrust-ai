import re

from app.generation.llm_contracts import LLMExplanation
from app.schemas.contracts import AIRequest


class SemanticGroundingError(ValueError):
    """Raised when an LLM explanation violates vehicle intelligence facts."""


def validate_semantic_grounding(
    explanation: LLMExplanation,
    request: AIRequest,
) -> None:
    """Validate semantic consistency between an LLM explanation and AIRequest."""

    _validate_decision(
        summary=explanation.summary,
        reasoning=explanation.reasoning,
        recommendation=explanation.recommendation,
        request=request,
    )
    _validate_unsupported_claims(
        summary=explanation.summary,
        reasoning=explanation.reasoning,
        recommendation=explanation.recommendation,
    )
    _validate_evidence_statuses(
        summary=explanation.summary,
        reasoning=explanation.reasoning,
        recommendation=explanation.recommendation,
        request=request,
    )
    _validate_risk_severities(
        summary=explanation.summary,
        reasoning=explanation.reasoning,
        recommendation=explanation.recommendation,
        request=request,
    )


def _validate_evidence_statuses(
    *,
    summary: str,
    reasoning: str,
    recommendation: str,
    request: AIRequest,
) -> None:
    clauses = _sentences(
        summary=summary,
        reasoning=reasoning,
        recommendation=recommendation,
    )

    for evidence in request.evidence:
        subject_terms = _evidence_terms(evidence)

        for clause in clauses:
            if not _contains_any(clause, subject_terms):
                continue

            evidence_scoped_clause = _scope_clause_to_evidence(
                clause=clause,
                evidence=evidence,
                all_evidence=request.evidence,
            )

            if evidence.status == "verified":
                if _contains_any(
                    evidence_scoped_clause,
                    {
                        "conflicting",
                        "inconsistent",
                    },
                ):
                    raise SemanticGroundingError(
                        f"{evidence.id} is verified but was described "
                        "as conflicting or inconsistent."
                    )

            elif evidence.status == "conflicting":
                if _contains_asserted_status(
                    evidence_scoped_clause,
                    {
                        "verified",
                        "consistent",
                        "confirmed",
                    },
                ):
                    raise SemanticGroundingError(
                        f"{evidence.id} is conflicting but was described "
                        "as verified or consistent."
                    )


def _scope_clause_to_evidence(
    *,
    clause: str,
    evidence,
    all_evidence,
) -> str:
    """
    Remove subject terms belonging to other evidence items before
    validating the status of the current evidence.

    This prevents claims about one evidence item from being
    incorrectly attributed to another evidence item in the same
    sentence or clause.
    """

    scoped = clause

    for other_evidence in all_evidence:
        if other_evidence.id == evidence.id:
            continue

        for term in _evidence_terms(other_evidence):
            if not term:
                continue

            scoped = scoped.replace(
                term,
                " ",
            )

    return _normalize(scoped)


def _validate_risk_severities(
    *,
    summary: str,
    reasoning: str,
    recommendation: str,
    request: AIRequest,
) -> None:
    sentences = _sentences(
        summary=summary,
        reasoning=reasoning,
        recommendation=recommendation,
    )

    for risk in request.risks:
        if risk.severity not in {"high", "critical"}:
            continue

        subject_terms = _risk_terms(risk)

        for sentence in sentences:
            if not _contains_any(sentence, subject_terms):
                continue

            if _contains_any(
                sentence,
                {
                    "low severity",
                    "low-severity",
                    "minor issue",
                    "minor risk",
                    "only a low",
                },
            ):
                raise SemanticGroundingError(
                    f"{risk.id} has {risk.severity} severity but was "
                    "described as low severity."
                )


def _validate_decision(
    *,
    summary: str,
    reasoning: str,
    recommendation: str,
    request: AIRequest,
) -> None:
    text = _normalize(
        " ".join(
            [
                summary,
                reasoning,
                recommendation,
            ]
        )
    )

    recommendation = request.decision.recommendation

    contradictory_claims = {
        "avoid": {
            "suitable for purchase",
            "safe to purchase",
            "safe purchase",
            "can proceed with the purchase",
            "can proceed with purchase",
            "proceed with the purchase",
            "proceed with purchase",
            "good purchase",
        },
        "buy": {
            "avoid the purchase",
            "avoid purchasing",
            "do not purchase",
            "should not purchase",
            "not suitable for purchase",
        },
        "review": {
            "safe to purchase",
            "suitable for purchase",
            "proceed with the purchase",
            "proceed with purchase",
            "avoid the purchase",
            "do not purchase",
        },
        "insufficient_evidence": {
            "safe to purchase",
            "suitable for purchase",
            "proceed with the purchase",
            "proceed with purchase",
            "avoid the purchase",
            "do not purchase",
        },
    }

    contradictory_terms = contradictory_claims.get(
        recommendation,
        set(),
    )

    if _contains_any(text, contradictory_terms):
        raise SemanticGroundingError(
            f"The deterministic decision is {recommendation} but "
            "the explanation contradicts that decision."
        )


def _validate_unsupported_claims(
    *,
    summary: str,
    reasoning: str,
    recommendation: str,
) -> None:
    text = _normalize(
        " ".join(
            [
                summary,
                reasoning,
                recommendation,
            ]
        )
    )

    unsupported_claims = {
        "tampering": {
            "tampered",
            "tampering",
            "deliberately altered",
            "deliberately changed",
            "rolled back intentionally",
            "intentionally rolled back",
        },
        "mechanical": {
            "mechanical failure",
            "engine failure",
            "transmission failure",
            "brake failure",
            "engine damage",
            "transmission damage",
        },
    }

    for claim_type, terms in unsupported_claims.items():
        if _contains_any(text, terms):
            raise SemanticGroundingError(
                f"unsupported {claim_type} claim detected in " "vehicle explanation."
            )


def _evidence_terms(evidence) -> set[str]:
    terms = {
        _normalize(evidence.id),
        _normalize(evidence.category),
        _normalize(evidence.title),
    }

    if evidence.id == "insurance-status":
        terms.update(
            {
                "insurance",
                "insurance record",
                "insurance status",
            }
        )

    elif evidence.id == "mileage-consistency":
        terms.update(
            {
                "odometer",
                "odometer history",
                "mileage",
                "mileage history",
            }
        )

    elif evidence.id == "accident-history":
        terms.update(
            {
                "accident",
                "accident history",
            }
        )

    elif evidence.id == "finance-status":
        terms.update(
            {
                "finance",
                "finance status",
                "finance record",
            }
        )

    return terms


def _risk_terms(risk) -> set[str]:
    terms = {
        _normalize(risk.id),
        _normalize(risk.category),
        _normalize(risk.title),
    }

    if risk.id == "odometer-inconsistency":
        terms.update(
            {
                "odometer",
                "odometer inconsistency",
                "mileage",
                "mileage inconsistency",
            }
        )

    elif risk.id == "major-accident-history":
        terms.update(
            {
                "accident",
                "accident history",
                "major accident",
            }
        )

    elif risk.id == "active-finance":
        terms.update(
            {
                "finance",
                "active finance",
            }
        )

    return terms


def _sentences(
    *,
    summary: str,
    reasoning: str,
    recommendation: str,
) -> list[str]:
    text = " ".join(
        [
            summary,
            reasoning,
            recommendation,
        ]
    )

    clauses: list[str] = []

    for sentence in re.split(r"[.!?]+", text):
        sentence = sentence.strip()

        if not sentence:
            continue

        # First split explicit contrast/concession clauses.
        parts = re.split(
            r"\b(?:while|although|whereas|but)\b",
            sentence,
            flags=re.IGNORECASE,
        )

        for part in parts:
            part = part.strip()

            if not part:
                continue

            # Split independent claims introduced after a comma.
            #
            # Example:
            #
            #   "odometer requires verification,
            #    the major accident is confirmed"
            #
            # becomes:
            #
            #   "odometer requires verification"
            #   "the major accident is confirmed"
            #
            # We intentionally require the new clause to start with
            # an article/pronoun so normal comma-separated wording
            # remains intact.
            subclauses = re.split(
                r",\s+(?=(?:the|this|that|an|a)\b)"
                r"|\s+\band\b\s+(?=(?:the|this|that|an|a)\b)",
                part,
                flags=re.IGNORECASE,
            )
            for subclause in subclauses:
                normalized = _normalize(subclause)

                if normalized:
                    clauses.append(normalized)

    return clauses


def _contains_any(
    text: str,
    terms: set[str],
) -> bool:
    return any(term in text for term in terms)


def _contains_asserted_status(
    text: str,
    terms: set[str],
) -> bool:
    """
    Return True when a status term is asserted as a current fact.

    Conditional or future verification language is not treated as a
    contradiction. For example:

    - "the record is verified" -> contradiction
    - "the record is consistent" -> contradiction
    - "verify the record" -> allowed
    - "requires verification" -> allowed
    - "until the record is verified" -> allowed
    - "cannot be treated as consistent" -> allowed
    """

    for term in terms:
        if term not in text:
            continue

        if _is_negated_status(text, term):
            continue

        if _is_future_or_conditional_status(text, term):
            continue

        return True

    return False


def _is_negated_status(
    text: str,
    term: str,
) -> bool:
    negated_patterns = {
        f"not {term}",
        f"not be {term}",
        f"cannot be {term}",
        f"cannot be treated as {term}",
        f"cannot be considered {term}",
        f"should not be considered {term}",
        f"should not be treated as {term}",
        f"not considered {term}",
        f"not treated as {term}",
    }

    return any(pattern in text for pattern in negated_patterns)


def _is_future_or_conditional_status(
    text: str,
    term: str,
) -> bool:
    future_patterns = {
        f"verify the {term}",
        f"verify this {term}",
        f"verify {term}",
        f"requires verification",
        f"requires {term} verification",
        f"needs verification",
        f"needs to be {term}",
        f"needs to be verified",
        f"should be verified",
        f"should be {term}",
        f"until {term}",
        f"until the {term}",
        f"before {term}",
        f"before the {term}",
        f"pending {term}",
        f"pending verification",
    }

    if any(pattern in text for pattern in future_patterns):
        return True

    conditional_patterns = {
        f"until the mileage history is {term}",
        f"until the odometer history is {term}",
        f"until the record is {term}",
        f"before the record is {term}",
        f"before the mileage history is {term}",
        f"before the odometer history is {term}",
    }

    return any(pattern in text for pattern in conditional_patterns)


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())

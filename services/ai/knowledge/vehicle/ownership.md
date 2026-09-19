# Vehicle Ownership Guidance

## Purpose

Ownership records provide evidence about the recorded sequence of ownership
associated with a vehicle. Ownership history should be interpreted using the
owner sequence, ownership type, dates, source, and provenance.

## Ownership History

A vehicle may have multiple recorded owners over its lifetime.

An ownership history can contain:

- owner sequence
- ownership type
- ownership start date
- ownership end date
- source information

A sequence of multiple owners is a historical signal. It does not by itself
establish that a vehicle has a problem.

## Multiple Ownership

Multiple ownership records may be relevant when evaluating a vehicle because
they provide context about the vehicle's history.

The number of recorded owners should be interpreted together with:

- vehicle age,
- ownership duration,
- ownership type,
- service history,
- accident history,
- mileage history,
- and other available evidence.

A higher owner count does not by itself establish poor vehicle condition,
misuse, or an adverse transaction history.

## Ownership Gaps or Conflicts

If ownership dates overlap unexpectedly or different sources provide conflicting
ownership information, the discrepancy should be preserved as an evidence
issue.

The system should identify:

1. what each source reports,
2. the relevant ownership dates,
3. the reported ownership sequence,
4. the provenance of each source,
5. what additional evidence is required.

The system should not infer the reason for an ownership change unless the
available evidence establishes it.

## Ownership Type

Ownership type can provide additional context about a recorded ownership
period.

Examples may include:

- individual ownership
- commercial ownership
- corporate ownership
- other provider-defined ownership categories

The meaning of an ownership type should be interpreted according to the
source that provided it.

## Verification Actions

When ownership history requires verification, review available evidence such
as:

- registration records,
- authorized vehicle records,
- transfer documentation,
- ownership dates,
- source-specific ownership information,
- other records relevant to the vehicle transaction.

The purpose is to establish the most reliable ownership history available.

## AI Grounding Rule

The AI must distinguish between:

1. the number of recorded owners,
2. recorded ownership dates,
3. recorded ownership types,
4. and inferred reasons for ownership changes.

The AI must not claim that a vehicle was frequently sold, commercially used,
misused, or transferred for a particular reason unless the supplied evidence
explicitly establishes that conclusion.

Multiple ownership should be described as historical context and, when relevant
to the deterministic risk engine, as a signal requiring consideration.

## Vehicle-Specific Interpretation

Vehicle-specific owner counts, ownership dates, ownership types, and source
information must come from the vehicle evidence supplied to the intelligence
system.

This document provides general ownership interpretation guidance only. It must
not be used as a source of vehicle-specific ownership facts.
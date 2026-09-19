# Vehicle PUC Guidance

## Purpose

Pollution Under Control (PUC) records provide evidence about the reported
emission-compliance status of a vehicle. PUC information should be interpreted
using the reported status, certificate details, dates, emission norm, source,
and provenance.

## PUC Status

The available PUC record may indicate:

- valid
- expired
- not available
- unknown

A valid status indicates that the available record reports a current PUC
certificate.

An expired status indicates that the recorded certificate has passed its
reported expiry date.

Not available means that a PUC certificate was not available in the supplied
records.

Unknown means that the available records do not establish the current PUC
status.

## Expired PUC

An expired PUC record is a compliance signal that requires attention.

The available record should be reviewed for:

- certificate number,
- issue date,
- expiry date,
- emission norm,
- source,
- retrieval information.

An expired record does not by itself establish the vehicle's current
emissions or mechanical condition.

## PUC Conflicts

PUC information may differ between sources or may become outdated when a
vehicle receives a newer certificate.

If different sources provide conflicting PUC information, preserve the
discrepancy as an evidence issue.

The system should identify:

1. what each source reports,
2. the relevant certificate dates,
3. the emission norm where available,
4. the provenance of each source,
5. what additional evidence is required.

The system should not automatically assume that one source is incorrect.

## Verification Actions

When PUC status requires verification, review available evidence such as:

- current PUC certificate,
- certificate number,
- issue and expiry dates,
- authorized vehicle records,
- emission-test records,
- other current records relevant to the vehicle.

The purpose is to establish the most reliable current PUC status available.

## AI Grounding Rule

The AI must distinguish between:

1. a reported valid PUC certificate,
2. a reported expired certificate,
3. a missing certificate,
4. an unknown status,
5. and a confirmed current emissions condition.

The AI must not claim that a vehicle fails an emissions test or has an emissions
problem unless the supplied evidence explicitly establishes that conclusion.

If the available record reports an expired PUC, the AI should state that the
available evidence indicates an expired certificate and recommend verification
of current PUC status.

## Vehicle-Specific Interpretation

Vehicle-specific certificate numbers, dates, emission norms, and PUC statuses
must come from the vehicle evidence supplied to the intelligence system.

This document provides general PUC interpretation guidance only. It must not be
used as a source of vehicle-specific PUC facts.
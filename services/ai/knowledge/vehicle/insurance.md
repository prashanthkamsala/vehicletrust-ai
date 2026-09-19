# Vehicle Insurance Guidance

## Purpose

Insurance records provide evidence about the reported insurance status of a
vehicle. Insurance information should be interpreted using the reported
status, policy details, dates, provider, and source.

## Insurance Status

The available vehicle insurance record may indicate:

- active
- expired
- unknown

An active status indicates that the available record reports current insurance
coverage.

An expired status indicates that the available record reports that the policy
has passed its recorded expiry date.

An unknown status means the available records do not establish the current
insurance status.

## Expired Insurance

An expired insurance record is a signal that requires attention.

The available record should be reviewed for:

- policy provider,
- policy type,
- policy number,
- policy start date,
- policy expiry date,
- source and retrieval information.

An expired record does not by itself establish why coverage ended or whether
a newer policy exists outside the available dataset.

## Insurance Conflicts

Insurance information may differ between sources or may become outdated as
policies change.

If one source reports expired insurance while another source reports active
coverage, the system should preserve the discrepancy as an evidence issue.

The system should identify:

1. what each source reports,
2. the relevant policy dates,
3. the provenance of each source,
4. whether the records may refer to different policies,
5. what additional evidence is needed.

The system should not automatically assume that one source is incorrect.

## Verification Actions

When insurance status requires verification, review available evidence such
as:

- current policy documentation,
- insurer records,
- policy number,
- policy start and expiry dates,
- authorized insurance databases,
- other current records relevant to the vehicle.

The purpose is to establish the most reliable current insurance status
available.

## AI Grounding Rule

The AI must distinguish between:

1. reported active insurance,
2. reported expired insurance,
3. unknown insurance status,
4. and confirmed current coverage.

The AI must not claim that a vehicle is uninsured unless the supplied evidence
explicitly establishes that conclusion.

If the available record reports expired insurance but does not contain a newer
policy record, the AI should state that the available evidence indicates
expired coverage and recommend verification of current coverage.

## Vehicle-Specific Interpretation

Vehicle-specific insurance providers, policy numbers, dates, and statuses must
come from the vehicle evidence supplied to the intelligence system.

This document provides general insurance interpretation guidance only. It must
not be used as a source of vehicle-specific insurance facts.
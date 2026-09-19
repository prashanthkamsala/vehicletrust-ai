# Vehicle Finance Guidance

## Purpose

Finance records indicate whether a vehicle has an associated financing
arrangement in the available records. Finance status should be interpreted
using the reported status, financier information, dates, and source.

## Finance Status

A vehicle finance record may indicate:

- active
- closed
- unknown

An active finance record means the available data reports an ongoing financing
arrangement.

A closed finance record indicates that the available data reports that the
financing arrangement has been closed.

An unknown status means the available records do not establish the current
finance status.

## Active Finance

An active finance record is a transaction or ownership-related signal that
requires attention during a vehicle purchase.

The record should be reviewed to determine:

- the reported financier,
- the financing start date,
- whether closure information exists,
- whether the record is current,
- whether additional verification is required before transfer.

An active finance record does not by itself establish that a sale or transfer
is impossible. It indicates that the finance status should be verified before
proceeding.

## Finance Conflicts

If different sources provide conflicting finance information, preserve the
conflict as an evidence issue.

For example, one source may report active finance while another source reports
closure.

The system should identify:

1. what each source reports,
2. the dates associated with each record,
3. the provenance of each source,
4. what additional evidence is needed to establish the current status.

The conflict should not automatically be resolved by assuming one source is
incorrect.

## Verification Actions

When finance status requires verification, review available evidence such as:

- financier records,
- finance closure documentation,
- loan closure confirmation,
- vehicle registration records,
- transfer-related documentation,
- other authorized records relevant to the transaction.

The purpose is to establish the most reliable current finance status available.

## AI Grounding Rule

The AI must distinguish between:

1. a reported active finance record,
2. a reported closed finance record,
3. an unknown finance status,
4. and a confirmed legal or transaction outcome.

The AI must not claim that a vehicle cannot be sold, transferred, or purchased
unless the supplied evidence explicitly establishes that conclusion.

An active finance record should be described as a signal requiring verification
when the available evidence does not establish the complete transaction status.

## Vehicle-Specific Interpretation

Vehicle-specific financier names, finance dates, closure dates, and statuses
must come from the vehicle evidence supplied to the intelligence system.

This document provides general finance interpretation guidance only. It must
not be used as a source of vehicle-specific finance facts.
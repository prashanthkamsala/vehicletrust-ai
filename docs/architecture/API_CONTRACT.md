# VehicleTrust AI API Contract

## Purpose

This document defines the initial HTTP API contract between the VehicleTrust AI frontend and backend.

The contract is intentionally small and focused on the first vehicle intelligence vertical slice.

---

## API Version

Current API version:

`v1`

Base path:

`/api/v1`

---

## Vehicle Intelligence

### Get Vehicle Intelligence

`GET /api/v1/vehicles/{vehicle_id}`

Returns the available vehicle intelligence for a vehicle.

### Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| vehicle_id | string | Yes | Unique vehicle identifier |

---

## Successful Response

Status:

`200 OK`

The response contains:

- `id`
- `identity`
- `evidence`
- `risks`
- `trust`
- `ai`

---

## JSON Naming Convention

The public JSON API uses `camelCase`.

Examples:

- `baseScore`
- `evidenceIds`
- `observedAt`

Python backend models use `snake_case`.

Examples:

- `base_score`
- `evidence_ids`
- `observed_at`

Pydantic serialization aliases provide the translation between the internal Python representation and the public API representation.

---

## Not Found

If the requested vehicle does not exist:

Status:

`404 Not Found`

Example response:

`{"detail": "Vehicle \"unknown-vehicle\" not found."}`

---

## Design Principles

1. API contracts are versioned.
2. Public JSON uses camelCase.
3. Backend Python uses snake_case.
4. API routes remain thin.
5. Business logic belongs outside the API route layer.
6. Vehicle intelligence must remain evidence-backed.
7. Trust calculations must remain deterministic.
8. AI interpretation must remain distinguishable from evidence.
9. API responses should be testable independently of UI implementation.
10. Breaking API changes require a new API version or an explicit migration strategy.

---

## Initial Architecture

Next.js
   |
   | HTTP
   v
FastAPI
   |
   v
Vehicle Service
   |
   v
Vehicle Intelligence

Future architecture:

Next.js
   |
   v
FastAPI
   |
   v
Vehicle Intelligence Service
   |
   +---- Evidence Layer
   |
   +---- Risk Engine
   |
   +---- Trust Engine
   |
   +---- AI / RAG Layer

# Device integration contract

Matria Care is currently a **simulated-data portfolio demo**. It accepts no real device connection by default.

## Adapter responsibility

Each future vendor adapter must authenticate with the vendor, validate consent, normalize vendor data, record provenance, and submit a `MonitoringReadingRequest` to the backend. Adapters must never send an alert directly from a raw device reading.

## Normalized fields

| Domain | Fields |
| --- | --- |
| Maternal wearable | `maternal_heart_rate`, `systolic_bp`, `diastolic_bp`, `oxygen_saturation` |
| CTG/fetal monitor | `fetal_heart_rate`, `uterine_activity` |
| Provenance | `source`, `observed_at`, `data_quality`, `raw_payload` |

## Required device-gateway checks

1. Confirm patient identity and recorded consent.
2. Verify source authenticity and replay protection.
3. Validate timestamp, units, plausible ranges, and device data quality.
4. Preserve source metadata and an audit trail.
5. Route only validated readings to a clinically governed risk engine.

No vendor, device, or synthetic stream is approved for clinical monitoring in this repository.

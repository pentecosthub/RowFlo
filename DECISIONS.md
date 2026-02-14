# Architecture Decision Records

## 2026-02-10: Abandon FTMS, Return to WaterRower BLE Protocol

**Decision:** Abandon FTMS (Fitness Machine Service) implementation and return to WaterRower's native Bluetooth protocol.

**Context:**
- Implemented complete FTMS protocol on ftms-conversion branch
- FTMS broadcasts successfully and apps can discover/connect
- **Critical failure:** Apps connect but receive no data
- Peloton app fails to connect entirely
- FTMS complexity not worth the compatibility issues

**Consequences:**
- Return to WaterRower's proven BLE protocol
- Focus on device-neutral Linux installation (removing Pi-specific dependencies)
- Keep ftms-conversion branch as historical record, but abandon development
- Primary goal: stable, device-neutral WaterRower BLE broadcaster

**Alternatives Considered:**
- Debug FTMS data flow issues
- Rejected: Too complex, app compatibility uncertain

**Status:** Decided

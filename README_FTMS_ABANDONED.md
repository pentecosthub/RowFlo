# ⚠️ THIS BRANCH IS ABANDONED ⚠️

**Date Abandoned:** 2026-02-10

## Why This Branch Exists

This branch contains a complete implementation of the FTMS (Fitness Machine Service) Bluetooth protocol for WaterRower data broadcasting.

## Why It Was Abandoned

While FTMS implementation was technically successful (broadcasting, app discovery, connection), **it failed to transmit actual rowing data to connected fitness apps.**

- ✅ FTMS service broadcasts successfully
- ✅ Apps can discover and connect
- ❌ No rowing data flows to apps
- ❌ Peloton app connection fails entirely

## Lessons Learned

See `DECISIONS.md` in master branch for full analysis.

## Current Direction

RowFlo development continues on **master branch** using WaterRower's native BLE protocol, with focus on:
- Device-neutral Linux installation
- Removing Raspberry Pi-specific dependencies  
- Stable, reliable WaterRower data broadcasting

## Historical Value

This branch is preserved as a reference for:
- Future FTMS implementation attempts
- Understanding FTMS protocol structure
- Documenting what didn't work and why

**Do not develop on this branch. Use master branch.**

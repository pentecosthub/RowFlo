# TODO.md – RoFlo Roadmap

This file tracks work required to stabilize and complete RoFlo as a
device-neutral fork of PiRowFlo.

---

## Phase 1: Baseline Stability

- [x] Verify project starts without syntax or indentation errors
- [x] Confirm `waterrowerthreads.py -h` runs successfully
- [ ] Identify files that fail on modern Python versions
- [ ] Create `KNOWN_ISSUES.md`
- [ ] Tag initial fork state (v0.1)

---

## Phase 2: Device Neutrality

- [ ] Identify Raspberry Pi–specific assumptions
- [ ] Make OLED/screen support optional
- [ ] Make ANT+ support optional
- [ ] Remove hard-coded GPIO dependencies
- [ ] Allow Bluetooth adapter selection
- [ ] Document required Bluetooth capabilities

---

## Phase 3: Installation Cleanup

- [ ] Review `install.sh` for Pi-only packages
- [ ] Separate generic Linux vs Raspberry Pi steps
- [ ] Document required system libraries
- [ ] Pin supported Python versions
- [ ] Add install verification steps

---

## Phase 4: Cross-Platform Testing

- [ ] Test on Raspberry Pi
- [ ] Test on thin client with built-in Bluetooth
- [ ] Test on thin client with USB Bluetooth
- [ ] Test in VM and document limitations
- [ ] Update README with support matrix

---

## Phase 5: Maintenance Decisions

- [ ] Decide long-term scope of RoFlo
- [ ] Determine which legacy features remain supported
- [ ] Evaluate upstream contribution options

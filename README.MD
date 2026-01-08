# RoFlo

RoFlo is a device-neutral fork of PiRowFlo.

This fork focuses on maintaining existing functionality while reducing hard-coded Raspberry Pi assumptions, improving installation documentation, and increasing portability across Linux-based systems.

## Project History (Inherited from PiRowFlo)

31.03.2025: Merged with elp3dr0 to fix compatibility with modern Raspberry Pi OS  
14.11.2021: Fixed pip install issue with pyusb in requirements.txt

<img src="docs/logo/PIROWFLO2.png" width="36%" height="36%">

---

<img src="docs/Hardware/IMG_20210104_155432.jpg" width="36%" height="36%"> <img src="docs/Hardware/Selection_015.png" width="30%" height="30%"> <img src="docs/Hardware/SmartRow.png" width="30%" height="30%">

<img src="docs/Screen/screenPiRowFlo.gif" width="36%" height="36%">

Read the LICENCE first. By using this software you agree to the licence.

## News (13.02.2021)

- Case is still in prototype stage

## Supported Apps S4 Monitor (23.02.2021)

|         | Kinomap (BLE) | Cityrowgo (BLE) | WaterRower Connect (BLE) | Coxswain (BLE) 7.9 or higher | Holofit |
| :-----: | :-----------: | :-------------: | :----------------------: | :--------------------------: | :-----: |
| Android |  test pending |        ✓        |    dev update required   |               ✓              |    ✓    |
|   iOS   |       ✓       |        ✓        |             ✓            |               –              |    ✓    |

## Supported Apps SmartRow (23.02.2021)

|         | Kinomap (BLE) | Cityrowgo (BLE) | WaterRower Connect (BLE) | Coxswain (BLE) 7.9 or higher | Holofit |
| :-----: | :-----------: | :-------------: | :----------------------: | :--------------------------: | :-----: |
| Android |  test pending |   test pending  |    dev update required   |               ✓              |    ✓    |
|   iOS   |       ✓       |        ✓        |             ✓            |               –              |    ✓    |

## Supported Watches (14.01.2021)

| Watch model | Native rowing app | ErgIQ |
| :---------: | :---------------: | :---: |
|   Fenix 6   |         ✓         |   –   |

## Features

- Read serial WaterRower data via USB
- Read SmartRow data via Bluetooth Low Energy
- Broadcast rowing data over Bluetooth Low Energy
- Broadcast rowing data over ANT+ using compatible dongles

## Bluetooth Requirements

RoFlo requires a working Bluetooth Low Energy (BLE) adapter.  
This may be provided by built-in Bluetooth hardware or a compatible USB Bluetooth adapter.

Multiple Bluetooth adapters may be required depending on usage and hardware configuration, particularly when using SmartRow and BLE broadcasting simultaneously.

## Motivation

The original motivation of PiRowFlo was to enable compatibility between WaterRower hardware, third-party training applications, and fitness devices such as Garmin watches. RoFlo preserves this goal while working toward broader Linux compatibility and clearer installation processes.

## Target Architecture

<img src="docs/Project-overview.png" width="100%">

## Requirements

### Hardware

RoFlo does not require Raspberry Pi hardware specifically.  
Any Linux-based system capable of USB, Bluetooth Low Energy, and optional ANT+ support may be used, including Raspberry Pi devices, thin clients, mini PCs, or other microcomputers.

### Software

### Installation

On a fresh Linux installation, ensure git is installed:

```bash
sudo apt-get install git

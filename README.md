# Beamline Intensity Calculator — DESY Hamburg 🔬

Built during the **DESY Summer Student Program 2019** (Hamburg, Germany) — a competitive scholarship awarded to physics students across Europe to work at one of the world's leading particle physics research centres.

> **For non-physicists:** A particle accelerator fires electrons near the speed of light. This produces extremely powerful X-ray light (a "Free Electron Laser"). That light travels down a pipe called a *beamline*, bouncing off a series of precision mirrors before reaching experiments. Every mirror absorbs a tiny fraction of the beam. This tool calculates exactly how much light survives to the end — something researchers need to know before designing experiments.

---

## What it does

**ICS (Intensity Calculation Support)** is a Python tool that calculates the final photon intensity at the end of a Free Electron Laser beamline, accounting for:

- Mirror reflectivity (varies by coating material and wavelength)
- Beam geometry and optical element dimensions
- Aperture clipping effects at different beam divergences

It was built as a complement to [WavePropaGator (WPG)](https://github.com/samoylv/WPG), an existing X-ray optics simulation framework, which calculates beam *shape* but not absolute *intensity*. ICS fills that gap.

Tested on **Beamline FL24** at FLASH2, DESY — a real operational beamline serving experiments in the Extreme Ultraviolet range (4–90 nm).

---

## Technical approach

The intensity at the end of the beamline is calculated as:

```
I = ∏ ρᵢ · Iᵢ
```

Where `ρᵢ` is the reflectivity of each mirror coating and `Iᵢ` is the partial beam intensity at each optical element. Mirror reflectivities are fetched automatically from the [CXRO X-Ray database](http://henke.lbl.gov/optical_constants/) using Selenium web automation.

The tool reads beamline configuration directly from WPG's `beamline.py` output files, parsing optical element distances, incidence angles, and dimensions into a Pandas DataFrame for calculation.

---

## Stack

- **Python** — core calculation logic
- **Pandas / NumPy** — data processing and DataFrame pipelines  
- **Tkinter** — desktop GUI for parameter input
- **Selenium** — automated data retrieval from the CXRO reflectivity database
- **Matplotlib** — results visualisation

---

## Key results

Tested across multiple scenarios on Beamline FL24:

| Scenario | Beam Divergence | Aperture | Final Intensity |
|---|---|---|---|
| Nominal conditions | 125 µrad | 14 mm | ~99.97% |
| High divergence | 200 µrad | 14 mm | ~68% |
| Small aperture | 125 µrad | 7 mm | ~29% |

A separate diffraction analysis (using WPG wavefront propagation) found that ray-tracing alone overestimates intensity by up to 30% for small apertures — validating the need for a more complete model.

---

## How to run

**Prerequisites:** Python 3, Chrome browser

```bash
pip install pandas numpy selenium webdriver-manager
```

```bash
python src/GUI.py
```

The GUI will prompt you to:
1. Select the number and type of optical elements (mirrors, apertures)
2. Choose mirror coating material (Nickel, Carbon, Platinum)
3. Load a `beamline.py` file exported from WPG
4. Enter beam divergence (µrad) and wavelength (nm)

Hit **Run** — the tool fetches live reflectivity data and outputs intensity at each optical element.

---

## Context

This project was completed in **6 weeks** as part of the DESY Summer Student Programme, under the supervision of Dr. Mabel Ruiz-Lopez (Photon Diagnostics group). The full technical report is included in this repo as [`report.pdf`](./report.pdf).

The DESY Summer Student Programme receives hundreds of applications annually from physics and engineering students across Europe. Selected students are embedded in active research groups working on particle accelerators, photon science, and detector development.

---

## What I'd do differently now

*Written in 2024, looking back at code from 2019:*

- Replace Selenium scraping with a direct API call or cached reflectivity data — the live scraping is brittle
- Add unit tests for the core intensity calculation functions
- Separate configuration (beamline parameters) from code using a YAML/JSON config file
- Package as a proper Python module with `pip install` support
- The GUI would be better as a web app (React + a FastAPI backend) — much more portable than Tkinter
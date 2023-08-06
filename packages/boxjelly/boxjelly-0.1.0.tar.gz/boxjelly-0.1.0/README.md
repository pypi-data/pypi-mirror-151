# BoxJelly

**BoxJelly** is a tool for viewing and editing object tracks in video.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
<!-- [![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/) -->
[![PyPI version](https://pypip.in/v/boxjelly/badge.png)](https://crate.io/packages/boxjelly/)
[![PyPI downloads](https://pypip.in/d/boxjelly/badge.png)](https://crate.io/packages/boxjelly/)

![BoxJelly logo](boxjelly/assets/images/boxjelly_logo_128.png)

Author: Kevin Barnard, [kbarnard@mbari.org](mailto:kbarnard@mbari.org)

---

## Cthulhu Integration

This branch is for the [Cthulhu](https://github.com/mbari-media-management/cthulhu) integration. This integration is still in development. Currently, the integration has some limitations:

- Cthulhu does not report video framerate, so a default of 29.97 is assumed.
- BoxJelly assumes the default interface configuration for Cthulhu:
    - Control port: `5005`
    - Incoming port: `5561`
    - Incoming topic: `localization`
    - Outgoing port: `5562`
    - Outgoing topic: `localization`
- Cthulhu must be running before you load a video/track file in BoxJelly.
- On initial load, tracks take some time to sync with Cthulhu.

Relevant TODOs:
- Detect video framerate
- Create settings dialog for interface config
- Better error handling on IPC failures

## Install

### From PyPI

BoxJelly is available on PyPI as `boxjelly`. To install, run:

```bash
pip install boxjelly
```

### From source

This project is build with Poetry. To install from source, run (in the project root):

```bash
poetry install
```

## Run

Once BoxJelly is installed, you can run it from the command line:

```bash
boxjelly
```

---

Copyright &copy; 2021&ndash;2022 [Monterey Bay Aquarium Research Institute](https://www.mbari.org)

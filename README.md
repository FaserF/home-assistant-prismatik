<p align="center">
  <img src="https://raw.githubusercontent.com/zomfg/Lightpack/749b592dd033cc96240a75f16d85f170640fab50/Software/res/icons/Prismatik.png" width="80" />
  &nbsp;
  &nbsp;
  &nbsp;
  <img src="https://raw.githubusercontent.com/home-assistant/assets/1e19f0dca208f0876b274c68345fcf989de7377a/logo/logo-pretty.svg" width="80" />
</p>

# Prismatik for Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/zomfg/home-assistant-prismatik?style=flat-square)](https://github.com/zomfg/home-assistant-prismatik/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/github/license/zomfg/home-assistant-prismatik?style=flat-square)](LICENSE)

A modern Home Assistant integration to control **Prismatik** (and compatible clones like Lightpack). Control your ambient lighting, adjust gamma, smoothness, and toggle various modes directly from Home Assistant.

---

## 🚀 Installation

### Option 1: HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click on **Integrations**.
3. Click the three dots in the top right corner and select **Custom repositories**.
4. Paste the URL of this repository: `https://github.com/zomfg/home-assistant-prismatik`
5. Select **Integration** as the category and click **Add**.
6. Find the **Prismatik** integration and click **Download**.
7. Restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=zomfg&repository=home-assistant-prismatik&category=integration)

### Option 2: Manual Installation

1. Download the latest release.
2. Copy the `custom_components/prismatik` folder into your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.

---

## ⚙️ Configuration

### 1. Prismatik Client Setup

Before configuring the integration in Home Assistant, ensure the Prismatik API is accessible:

1. Open the **Prismatik** settings on your PC.
2. Navigate to the **Experimental** or **API** section.
3. **CRITICAL:** Uncheck `Listen only on local interface` (allows HA to connect to your PC).
4. (Optional) Set an **API Key**.
5. Note the **Port** (default is `3636`).

### 2. Home Assistant Setup

1. Go to **Settings** > **Devices & Services**.
2. Click **+ Add Integration**.
3. Search for **Prismatik**.
4. Enter your PC's IP address, the port, and the API key (if set).
5. Specify a **Profile Name** (recommended: `hass`) to prevent HA from overriding your main PC profile settings permanently.

---

## 🧩 Entities & Features

The following entities are created for each Prismatik instance:

| Entity | Icon | Description |
| :--- | :--- | :--- |
| **Light** | `mdi:led-strip-variant` | Main control for toggling the lights and changing colors/brightness. |
| **API Busy** | `mdi:progress-clock` | Binary sensor showing if the Prismatik API is currently locked by another process. |
| **Moodlight Mode** | `mdi:lightbulb-multiple` | Switch to toggle between Screen Mirroring and Moodlight mode. |
| **Gamma** | `mdi:gamma` | Number entity to adjust the color gamma correction (0.1 - 10.0). |
| **Smoothness** | `mdi:Blur` | Number entity to adjust the transition smoothness (0 - 255). |
| **Lock API** | `mdi:lock-outline` | Button to manually lock the Prismatik API for HA exclusive use. |
| **Unlock API** | `mdi:lock-open-variant` | Button to release the API lock. |

---

## 📝 Notes

- **API Locking:** The integration automatically manages API locking/unlocking to ensure responsiveness while allowing the desktop client to resume control.
- **Profiles:** Using a dedicated profile in Prismatik helps in isolating Home Assistant changes from your desktop usage.

---

*Initially tested on HA 0.105.4 and Prismatik 5.2.11.21.*

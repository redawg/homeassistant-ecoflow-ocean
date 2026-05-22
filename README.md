# Ecoflow Ocean USA - full system (Panel, Inverter, Batteries, EV charger, Power insight)

Home Assistant custom integration for the **EcoFlow OCEAN USA** ecosystem using the official [EcoFlow Developer API](https://developer.ecoflow.com/us/document/introduction).

Polls `GET /iot-open/sign/device/quota/all` per device. Add **one config entry per device** (inverter, panel, EV charger, PowerInsight, etc.). No EcoFlow app password required—only Developer Portal Access Key and Secret Key.

## Supported devices

| Device | Config entry type | Sensors |
|--------|-------------------|---------|
| **OCEAN Pro** | Inverter + batteries | Solar, home, grid, battery, energy totals |
| **PowerOcean / OCEAN** | Inverter + batteries | Same as above |
| **Smart Electrical Panel** | Panel | System power + panel/circuit loads |
| **OCEAN EV Charger (11.5 kW)** | EV charger | EV power, state, session energy + shared system power when exposed |
| **PowerInsight** | Hub / monitor | System-level power and energy |
| **Other bound devices** | Auto-detected | Best-effort via generic quota parser |

Device type is detected from the product name and serial prefix during setup.

## Prerequisites

1. Register at the [EcoFlow Developer Portal](https://developer.ecoflow.com).
2. Create an application and copy the **Access Key** and **Secret Key**.
3. **Bind your PowerOcean serial number** to that application (required—otherwise API returns error `1006`).
4. Pick the correct **region** during setup:
   - **United States** → `https://api-a.ecoflow.com`
   - **Europe** → `https://api-e.ecoflow.com`

## Installation

### HACS (recommended)

1. HACS → Integrations → Custom repositories
2. Add `https://github.com/redawg/homeassistant-ecoflow-ocean` (category: Integration)
3. Install **Ecoflow Ocean USA - full system (...)** and restart Home Assistant

### Manual

Copy `custom_components/ecoflow_ocean` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

1. **Settings → Devices & Services → Add Integration**
2. Search for **Ecoflow Ocean USA**
3. Enter Access Key, Secret Key, and region (United States for `api-a.ecoflow.com`)
4. Select each device (Panel, Inverter, EV charger, PowerInsight, …) — repeat **Add Integration** for every device in your system

Optional: **Configure** the integration to change the poll interval (default 15 seconds, minimum 10).

## Dashboard (EcoFlow app style)

An optional Lovelace dashboard with animated power flows (Solar / Home / Grid / Battery) and a dark theme is included:

- [`dashboards/ecoflow_ocean.yaml`](dashboards/ecoflow_ocean.yaml) — main dashboard
- [`themes/ecoflow_ocean.yaml`](themes/ecoflow_ocean.yaml) — dark EcoFlow-like theme
- Setup guide: [`dashboards/README.md`](dashboards/README.md)

Requires the HACS card **[Power Flow Card Plus](https://github.com/flixlix/power-flow-card-plus)**.

### Ansible install

To push the dashboard and theme to Home Assistant over SSH (or locally):

```bash
cd ansible
cp inventory.example.yml inventory.yml
cp group_vars/homeassistant.yml.example group_vars/homeassistant.yml
# edit ecoflow_entity_prefix and ha_config_dir
ansible-playbook playbooks/install_dashboard.yml
```

See [`ansible/README.md`](ansible/README.md) for inventory examples (including HA OS at `/config`).

## Sensors

| Sensor | Description |
|--------|-------------|
| Battery SOC / power / charge & discharge power | Battery state |
| Solar / home / grid power | Live power flow |
| Grid import & export power | Derived from signed grid power |
| Grid frequency | PCS report |
| Battery voltage, current, SOH, max cell temp | Pack diagnostics |
| Solar / home / grid / battery energy totals | Lifetime kWh (Energy Dashboard compatible) |

## Energy Dashboard

Map entities in **Settings → Dashboards → Energy**:

- **Solar production** → `sensor.*_solar_energy_total`
- **Grid consumption** → `sensor.*_grid_import_energy_total`
- **Grid export** → `sensor.*_grid_export_energy_total`
- **Battery** → charge/discharge total sensors

## Troubleshooting

| API code | Message | What to do |
|----------|---------|------------|
| **1006** | Device not bound | Add serial number `HR51…` (your SN) in the [Developer Portal](https://developer.ecoflow.com) under your application |
| **8513** | `accessKey is invalid` | Keys do not match the selected **region** (US → United States / `api-a`, EU → Europe / `api-e`), or keys were rotated. Delete the config entry, create new keys in the portal, and set up the integration again |
| **8521** | Signature wrong | Report on GitHub — signing bug or API change |

If setup succeeds but polling fails with **8513**, you almost always have the **wrong region** saved in the entry or **old keys** after regenerating them in the portal.

## Security

Store API keys only in Home Assistant’s encrypted config entry—never commit them to git or share them in chat. Rotate keys in the developer portal if they are exposed.

## Related projects

- [homeassistant-ecoflow-ocean-mqtt](https://github.com/redawg/homeassistant-ecoflow-ocean-mqtt) — real-time MQTT push (same sensors, lower latency; runs alongside this integration)
- [shuette42/ecoflow-energy-ha](https://github.com/shuette42/ecoflow-energy-ha) — broader EcoFlow device support
- [MaxGrmm/EF-PowerOcean-TcpModbus](https://github.com/MaxGrmm/EF-PowerOcean-TcpModbus) — local Modbus TCP (no cloud)

## License

MIT

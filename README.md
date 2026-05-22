# EcoFlow Ocean for Home Assistant

Home Assistant custom integration for **EcoFlow PowerOcean** systems using the official [EcoFlow Developer API](https://developer.ecoflow.com/us/document/introduction).

Polls `GET /iot-open/sign/device/quota/all` for power, battery, grid, solar, and lifetime energy sensors. No EcoFlow cloud app password required—only Developer Portal Access Key and Secret Key.

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
3. Install **EcoFlow Ocean** and restart Home Assistant

### Manual

Copy `custom_components/ecoflow_ocean` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

1. **Settings → Devices & Services → Add Integration**
2. Search for **EcoFlow Ocean**
3. Enter Access Key, Secret Key, and region
4. Select your PowerOcean device from the list

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

## Security

Store API keys only in Home Assistant’s encrypted config entry—never commit them to git or share them in chat. Rotate keys in the developer portal if they are exposed.

## Related projects

- [shuette42/ecoflow-energy-ha](https://github.com/shuette42/ecoflow-energy-ha) — broader EcoFlow device support
- [MaxGrmm/EF-PowerOcean-TcpModbus](https://github.com/MaxGrmm/EF-PowerOcean-TcpModbus) — local Modbus TCP (no cloud)

## License

MIT

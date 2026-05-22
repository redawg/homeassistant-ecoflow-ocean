# EcoFlow Ocean dashboard

Lovelace dashboard styled like the **EcoFlow app** live power screen: animated flows between **Solar**, **Home**, **Grid**, and **Battery**, with SOC in the center ring.

## Requirements (HACS)

| Component | HACS repository |
|-----------|-----------------|
| **Power Flow Card Plus** | `flixlix/power-flow-card-plus` (category: **Dashboard**) |
| **Auto Entities** (Details tab only) | `custom-cards/auto-entities` (category: **Frontend**) |

Install both, add their resources if prompted, then restart Home Assistant.

## 1. Find your entity prefix

After the integration is configured:

1. **Developer Tools** → **States**
2. Search `battery_soc`
3. Note the entity id, e.g. `sensor.ecoflow_powerocean_battery_soc`
4. Your prefix is `ecoflow_powerocean` (the part before `_battery_soc`)

Open `dashboards/ecoflow_ocean.yaml` and replace every `ecoflow_powerocean` with your prefix (search & replace).

## 2. Install the theme (optional)

Copy `themes/ecoflow_ocean.yaml` to your HA `config/themes/` folder.

```yaml
# configuration.yaml
frontend:
  themes: !include_dir_merge_named themes
```

Restart HA, then **Profile** → **Theme** → **ecoflow_ocean**.

## 3. Add the dashboard

### Option A — YAML mode (recommended)

1. Copy `dashboards/ecoflow_ocean.yaml` to `config/dashboards/ecoflow_ocean.yaml`
2. Add to `configuration.yaml`:

```yaml
lovelace:
  mode: storage
  dashboards:
    ecoflow-ocean:
      mode: yaml
      title: EcoFlow Ocean
      icon: mdi:solar-power-variant
      show_in_sidebar: true
      filename: dashboards/ecoflow_ocean.yaml
```

3. Restart Home Assistant

### Option B — UI import

1. **Settings** → **Dashboards** → **Add dashboard**
2. Open the new dashboard → **⋮** → **Edit dashboard** (YAML mode)
3. Paste the contents of `ecoflow_ocean.yaml` (after updating entity prefixes)
4. Save

## Views

| Tab | Content |
|-----|---------|
| **Live** | Power Flow Card Plus (EcoFlow-style diagram) + SOC gauge + live watts |
| **Energy** | Built-in energy distribution + lifetime kWh sensors |
| **Details** | All integration sensors (auto-entities by label) |

## Energy tab

For the **Energy distribution** card to show data, map the integration’s kWh sensors in **Settings** → **Dashboards** → **Energy** (once). The card links to that configuration.

## Troubleshooting

- **Wrong flows or zero watts** — Check entity prefix matches; confirm sensors update in Developer Tools.
- **Card not found** — Install Power Flow Card Plus and add `/hacsfiles/power-flow-card-plus/power-flow-card-plus.js` under **Dashboard resources**.
- **Grid direction looks inverted** — Swap `grid_import_power` / `grid_export_power` in the YAML if your install uses the opposite sign convention.

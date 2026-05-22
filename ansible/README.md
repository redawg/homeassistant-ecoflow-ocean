# Ansible — Install EcoFlow Ocean dashboard

Deploys the Lovelace dashboard, dark theme, and `configuration.yaml` package snippet to a Home Assistant config directory.

## What it installs

| File | Destination |
|------|-------------|
| `themes/ecoflow_ocean.yaml` | `{{ ha_config_dir }}/themes/` |
| Dashboard (templated entity IDs) | `{{ ha_config_dir }}/dashboards/ecoflow_ocean.yaml` |
| Package | `{{ ha_config_dir }}/packages/ecoflow_ocean_dashboard.yaml` |

When `ecoflow_enable_packages: true` (default), it also adds this line under `homeassistant:` if missing:

```yaml
  packages: !include_dir_named packages
```

## Prerequisites

- Ansible 2.14+
- SSH or local access to the machine that holds the HA **config** folder (`/config` on HA OS)
- EcoFlow Ocean **integration** already configured in HA
- HACS cards (install manually in HA):
  - [Power Flow Card Plus](https://github.com/flixlix/power-flow-card-plus)
  - [Auto Entities](https://github.com/custom-cards/auto-entities)

## Quick start

```bash
cd ansible
cp inventory.example.yml inventory.yml
cp group_vars/homeassistant.yml.example group_vars/homeassistant.yml
```

Edit `inventory.yml` (host, user, `ha_config_dir`) and `group_vars/homeassistant.yml` (`ecoflow_entity_prefix`).

Run:

```bash
ansible-playbook playbooks/install_dashboard.yml
```

### Your Home Assistant (`172.16.255.250`)

Example `inventory.yml`:

```yaml
all:
  children:
    homeassistant:
      hosts:
        ha:
          ansible_host: 172.16.255.250
          ansible_user: root
          ha_config_dir: /config
```

Example `group_vars/homeassistant.yml`:

```yaml
ecoflow_entity_prefix: ecoflow_powerocean   # change to match your entities
ecoflow_restart_ha: true                    # HA OS only (`ha` CLI)
```

## Entity prefix

Find in HA: **Developer Tools** → **States** → search `battery_soc`.

| Entity id | Prefix |
|-----------|--------|
| `sensor.ecoflow_powerocean_battery_soc` | `ecoflow_powerocean` |

Override at runtime:

```bash
ansible-playbook playbooks/install_dashboard.yml -e ecoflow_entity_prefix=your_prefix
```

## Install methods

### Remote SSH (Home Assistant OS)

Enable the **Terminal & SSH** add-on, set password/key, use `ansible_user: root` and `ha_config_dir: /config`.

### Local config folder (Docker / Core on same machine)

```yaml
# inventory.yml
all:
  children:
    homeassistant:
      hosts:
        ha:
          ansible_connection: local
          ha_config_dir: /home/you/homeassistant/config
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ha_config_dir` | `/config` | Home Assistant configuration directory |
| `ecoflow_entity_prefix` | `ecoflow_powerocean` | Sensor name slug |
| `ecoflow_enable_packages` | `true` | Write `packages/ecoflow_ocean_dashboard.yaml` |
| `ecoflow_restart_ha` | `false` | Run `ha core restart` after changes |
| `ecoflow_dashboard_title` | `EcoFlow Ocean` | Sidebar title |

## Files-only mode

Skip package + `configuration.yaml` changes:

```bash
ansible-playbook playbooks/install_dashboard.yml -e ecoflow_enable_packages=false
```

Merge the printed `lovelace:` / `frontend:` snippet into `configuration.yaml` yourself.

## Troubleshooting

- **`configuration directory not found`** — Fix `ha_config_dir` or mount path.
- **`homeassistant:` not in configuration.yaml** — Add a minimal `homeassistant:` block first, or use `ecoflow_enable_packages=false`.
- **`ha core restart` failed** — Set `ecoflow_restart_ha: false` and restart from the HA UI.
- **Empty dashboard / unknown card** — Install Power Flow Card Plus in HACS and restart HA.

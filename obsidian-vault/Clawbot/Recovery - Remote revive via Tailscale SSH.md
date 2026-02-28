# Recovery - Remote revive via Tailscale SSH

Goal: If OpenClaw stops responding but **Windows is still running**, recover it from a phone.

## Overview
- Use **Tailscale** to reach the laptop securely.
- SSH into **Windows** from the phone.
- Restart OpenClaw Gateway inside WSL (`Ubuntu-24.04`).

## Prereqs (one-time)
- Tailscale installed + logged in on:
  - Phone
  - Laptop (Windows)
- Windows **OpenSSH Server** installed and running (`sshd`).
- Windows firewall rule restricted to **Tailscale interface only** (recommended).
- SSH key auth working from phone (Termius key added to Windows authorized_keys).

## Fast recovery (one-liner)
In the Windows SSH session (from phone):

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "systemctl --user restart openclaw-gateway.service && openclaw gateway status"
```

## Panic button script (recommended)
Script created on Windows:

- `C:\Users\allen\revive-openclaw.ps1`

Run:

```powershell
cd C:\Users\allen
.\revive-openclaw.ps1
```

If PowerShell blocks scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Notes
- If the laptop is asleep/offline, remote recovery won’t work. The machine must be awake and connected.

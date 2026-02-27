# WSL CUDA / GPU notes

## Quick checks
- `uname -a`
- `command -v nvidia-smi && nvidia-smi`
- `ls -la /usr/lib/wsl/lib`

## Reality check
On WSL, CUDA generally depends on Windows-side NVIDIA driver + WSL GPU support.

## If enabling WSL GPU
1) Install/update NVIDIA Windows driver (WSL-capable)
2) `wsl --shutdown`
3) Re-check `nvidia-smi` inside WSL

## Notes
- Installing `nvidia-cuda-toolkit` inside WSL is large and may not help unless the Windows driver exposes GPU.

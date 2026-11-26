import os
import platform
import shutil
import subprocess
import sys


def get_gpu_info():
    """Return GPU details via nvidia-smi if available."""
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader",
            ],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out.splitlines() if out else ["No GPU detected"]
    except Exception:
        return ["nvidia-smi not available"]


def get_torch_info():
    """Return PyTorch and CUDA availability if torch is installed."""
    try:
        import torch

        return {
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        }
    except ImportError:
        return {"torch_version": "not installed"}


def main():
    disk = shutil.disk_usage("/")
    ram_gb = None
    try:
        import psutil

        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
    except ImportError:
        pass

    print("=== TrainGrid System Report ===")
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python: {sys.version.split()[0]}")
    print(f"CPU cores: {os.cpu_count()}")
    if ram_gb is not None:
        print(f"RAM: {ram_gb} GB")
    print(f"Disk Total: {round(disk.total / (1024**3), 2)} GB | Free: {round(disk.free / (1024**3), 2)} GB")
    print("GPUs:")
    for gpu in get_gpu_info():
        print(f"  - {gpu}")
    print(f"PyTorch: {get_torch_info()}")


if __name__ == "__main__":
    main()

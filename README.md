# TrainGrid

A unified model training repository designed to run across Kaggle, Google Colab, and custom servers—starting with automated Kaggle system verification and ready to evolve into video diffusion model training.

## Setup

1. Copy `.env.example` to `.env` and add your Kaggle credentials:
   ```bash
   cp .env.example .env
   ```
2. Sync secrets to your GitHub repository:
   ```bash
   gh secret set -f .env
   ```
3. Push to GitHub or trigger **Kaggle System Report** from the **Actions** tab to inspect the Kaggle GPU, CPU, RAM, disk, and PyTorch environment.

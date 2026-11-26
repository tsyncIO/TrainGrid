# TrainGrid

A unified compute and training orchestration framework designed to run ML experiments, system verification, and video diffusion model training seamlessly across Kaggle, Google Colab, and custom compute.

TrainGrid includes its own native GitHub Action ([`.github/actions/traingrid-action`](.github/actions/traingrid-action/action.yml)) with modern Kaggle API token authentication and automatic status polling.

---

## Architecture Overview

```
TrainGrid/
├── .github/
│   ├── actions/
│   │   └── traingrid-action/     # Native Kaggle orchestration action
│   │       └── action.yml
│   └── workflows/
│       └── traingrid.yml         # CI/CD trigger workflow
├── src/
│   └── system_report.py          # Environment & hardware auditor script
├── .env.example                  # Template for credentials
├── requirements.txt              # Dependencies installed in the Kaggle environment
└── README.md
```

---

## Quickstart: Clone to Successful Reproduction

Follow these step-by-step instructions to clone, configure, and trigger a successful run on Kaggle.

### 1. Prerequisites

- **GitHub Account** & [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated:
  ```bash
  gh auth login
  ```
- **Kaggle Account** with phone verification (required by Kaggle for kernel internet & GPU/TPU access).
- [uv](https://docs.astral.sh/uv/) or Python 3.10+ installed locally.

---

### 2. Obtain Kaggle API Credentials

1. Go to [Kaggle](https://www.kaggle.com) and log in.
2. Click your profile picture (top right) → **Settings**.
3. Scroll down to the **API** section and click **Create New Token** (or **Generate New Token**).
4. Note your credentials:
   - **`KAGGLE_USERNAME`**: Your Kaggle username handle (e.g. `tanvirkabirshaon` or from your profile URL `kaggle.com/your_username`).
   - **`KAGGLE_KEY`**: The secret token string provided by Kaggle.

---

### 3. Clone the Repository & Configure Secrets Locally

```bash
# Clone the repository
git clone https://github.com/tsyncIO/TrainGrid.git
cd TrainGrid

# Copy the example environment file
cp .env.example .env
```

Open `.env` in your editor and enter your credentials:

```env
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_token_string
```

> **Security Note:** `.env` is listed in `.gitignore` and is never committed to Git history.

---

### 4. Set Up Local Virtual Environment (Optional, for local development)

Using `uv`:
```bash
# Create and activate virtual environment
uv venv --clear /tmp/TrainGrid-venv
ln -sfn /tmp/TrainGrid-venv .venv
source .venv/bin/activate

# Install dependencies locally
uv pip install -r requirements.txt

# Run system report locally
python src/system_report.py
```

---

### 5. Sync Credentials to GitHub Repository Secrets

Use the GitHub CLI to automatically upload your credentials to GitHub Secrets in one command:

```bash
gh secret set -f .env
```

To verify both secrets are uploaded:
```bash
gh secret list
```
You should see:
- `KAGGLE_USERNAME`
- `KAGGLE_KEY`

---

### 6. Trigger the Workflow

You can trigger the workflow from the terminal via `gh`:

```bash
gh workflow run "traingrid.yml"
```

And watch it execute live:
```bash
gh run watch
```

Alternatively, trigger it via GitHub Web UI:
1. Go to `https://github.com/<your-username>/TrainGrid/actions`.
2. Click **TrainGrid** in the left sidebar.
3. Click **Run workflow** → select branch `main` → click **Run workflow**.

---

### 7. View Results and Verification

The workflow takes approximately 1 minute to complete. Once finished, you will see the system report in the step logs:

```text
=== TrainGrid System Report ===
OS: Linux 6.18.55+ (x86_64)
Python: 3.13.18
CPU cores: 4
RAM: 31.35 GB
Disk Total: 8156.88 GB | Free: 2513.08 GB
GPUs:
  - nvidia-smi not available (or lists attached GPU when enable_gpu: true)
PyTorch: {'torch_version': '2.11.0+cpu', 'cuda_available': False, 'device_count': 0}
```

---

## Workflow Configuration Options

You can customize execution parameters inside [`.github/workflows/traingrid.yml`](.github/workflows/traingrid.yml):

| Parameter | Type | Default | Description |
|---|---|---|---|
| `custom_script` | string | `python src/system_report.py` | Command/script executed inside the Kaggle kernel |
| `enable_gpu` | boolean | `false` | Enable Kaggle GPU accelerator (`true` / `false`) |
| `enable_tpu` | boolean | `false` | Enable Kaggle TPU accelerator (`true` / `false`) |
| `enable_internet` | boolean | `true` | Enable network access for cloning repo & pip installs |
| `working_subdir` | string | `""` | Subdirectory inside repository where script executes |
| `sleep_time` | number | `15` | Polling interval (seconds) to check execution status |
| `dataset_sources` | string | `""` | Kaggle datasets to mount: `{username}/{dataset-slug}` |
| `competition_sources` | string | `""` | Competition datasets to mount |

---

## Technical Notes & Kaggle CLI Reproducibility

If you are developing or maintaining Kaggle automation pipelines, keep these key points in mind:

### 1. Kaggle CLI Dual-Credential Support (`kaggle.json` vs `access_token`)
- **Legacy Kaggle CLI (`<2.0.0`)**: Required a JSON file at `~/.kaggle/kaggle.json` with `{"username": "...", "key": "..."}`.
- **Modern Kaggle CLI (`>=2.0.0`)**: Now expects a raw token file at `~/.kaggle/access_token` or the environment variable `KAGGLE_API_TOKEN`.
- **How TrainGrid solves this**: `traingrid-action` automatically provisions **both** credential formats and exports `KAGGLE_API_TOKEN`, ensuring full backward and forward compatibility regardless of the Kaggle CLI version installed.

### 2. Upstream Bug Fixes in `traingrid-action`
Standard third-party actions frequently fail on modern runners due to two upstream issues:
1. **Missing `six` dependency in `kaggle 2.2.5+`**: The newest CLI release imports `six` internally without bundling it. TrainGrid explicitly installs `kaggle six` during environment setup to prevent runtime crashes.
2. **Case-insensitive status polling**: Newer Kaggle CLI versions report completion as `KernelWorkerStatus.COMPLETE` instead of lowercase `"complete"`. TrainGrid's polling engine uses regex matching (`=~ [Cc][Oo][Mm][Pp][Ll][Ee][Tt][Ee]`), preventing runners from hanging in infinite loops.

---
| `sleep_time` | number | `15` | Polling interval (seconds) to check execution status |
| `dataset_sources` | string | `""` | Kaggle datasets to mount: `{username}/{dataset-slug}` |
| `competition_sources` | string | `""` | Competition datasets to mount |

---

## Author & License

- **Author:** Tanvir Kabir Shaon
- **License:** MIT

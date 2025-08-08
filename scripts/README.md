# Local Environment Setup

This directory contains scripts for automating the setup of the local development environment.

## setup_local_env.py

This script provisions a complete local Kubernetes development environment using `k3d` and `Helm`.

### Prerequisites

Before running the script, you must have the following tools installed and available in your system's PATH:

* **Docker Desktop**: The container runtime.
* **k3d**: For creating the local Kubernetes cluster.
* **kubectl**: For interacting with the cluster.
* **Helm**: For managing Kubernetes applications.

### Usage

To create and configure the local environment, run the following command from the project's **root directory**:

```bash
python scripts/setup_local_env.py
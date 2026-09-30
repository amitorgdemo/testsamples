# Azure Infrastructure Provisioning API Service

A secured, enterprise-structured REST API built with **FastAPI** (Python 3.13+) designed to orchestrate Azure cloud resources dynamically while maintaining an autonomous tracking repository.

## 🗂️ Repository Architecture

The project adheres to a clean, decoupled service-oriented architecture:

```text
azure-vnet-provisioner/
│
├── app/
│   ├── __init__.py          # App initialization & global middleware mounting
│   ├── api/
│   │   ├── __init__.py      # Package routing tree mapping
│   │   ├── auth_api.py      # Authentication endpoints (Token issuance)
│   │   ├── rg_api.py        # Independent Resource Group API paths
│   │   └── vnet_api.py      # Virtual Network API paths
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py      # Cryptography, user DB & token management
│   ├── db/
│   │   ├── __init__.py
│   │   └── vnet_repo.py     # Local JSON flat-file data persistence layer
│   ├── models/
│   │   ├── __init__.py      # Unified model contract exposures
│   │   ├── resource_group.py# Resource Group Pydantic contracts
│   │   ├── subnetschema.py  # Subnet validation schemas
│   │   └── vnet.py          # Virtual Network payload and response contracts
│   └── services/
│       ├── __init__.py
│       ├── azure_services.py# Standalone Resource Group core service layer
│       └── vnet_service.py  # Standalone Network orchestration service layer
│
├── requirements.txt         # Project dependencies spec
└── run.py                   # Server engine startup entry script
```

---

## ⚙️ Initial Startup & Local Build

1. **Initialize and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Authenticate your Terminal with Azure**:
   Ensure your ambient workstation environment has access to manage your subscription by authenticating via the Azure CLI:
   ```bash
   az login --scope https://management.azure.com/.default
   ```

4. **Launch Server Runtime**:
   ```bash
   python run.py
   ```
   The interactive API catalog documentation page will instantly be accessible at **`http://127.0.0`**.

---

## 🔒 Security Layer & Evaluation Credentials

This system features a global **ASGI Middleware Layer** that intercepts traffic down to the routing path. Except for explicit system configuration paths (`/docs`, `/api/v1/auth/token`), **all routes are strictly protected**. 

The authentication architecture accepts standard **OAuth2 Password Bearer** flows, matching inputs against a secure, local mock database using cryptographically safe **SHA-256 password hashing validation**, issuing stateless **JWT (JSON Web Tokens)**.

You may simulate evaluation testing operations with any of these pre-configured user credentials:

| Username | Password | Role / Access Tier |
| :--- | :--- | :--- |
| `admin` | `AzureDemo2026!` | Administrator (Full Access) |
| `network_engineer` | `NetOpsPass2026!` | Engineer (Full Access) |

---

## 🚀 Core API Endpoints

### 1. Token Issuance (`POST /api/v1/auth/token`)
Exchanges clean credentials for a valid 60-minute JWT token string.

### 2. Idempotent Network Provisioning (`POST /api/v1/vnets`)
Accepts strict data payload structures. It runs an **idempotent check** against the targeted landing space—automatically spinning up the Resource Group via the shared core service layer if missing, or safely reusing it if it exists—before initializing the VNET block.
* **Payload Validation Rule**: If mandatory structural fields like `vnet_name` or `subscription_id` are omitted, the engine blocks processing immediately, throwing a descriptive `422 Unprocessable Entity` payload tracing block.

### 3. Local Metadata Pull (`GET /api/v1/vnets/db/{resource_id}`)
Pulls historical resource deployment tracking traces out of the local tracking persistence file.

### 4. Real-Time Azure Discovery (`GET /api/v1/vnets/azure/details`)
Queries live runtime execution states and configurations directly from the Azure ARM Fabric architecture.

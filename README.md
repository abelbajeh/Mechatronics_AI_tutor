
```markdown
# Design and Development of a Mobile Mechatronic Tutor with Edge AI Capability

> **🚧 Work in Progress:** The codebase is currently under active development. Some modules (like the visual interface and full hardware integration) are still being finalized.

This repository contains the software orchestrator, data ingestion pipeline, semantic routing logic, and hardware interface code for a fully offline, edge-native educational tutor.

## 🛠️ Hardware Setup

This system is explicitly designed and optimized to run natively on the **Raspberry Pi 5 (4GB)** to ensure data privacy, cloud independence, and cost-efficiency.

### Required Components
* **Compute Unit:** Raspberry Pi 5 (**4GB RAM**).
* **Power Supply:** Lithium-ion battery pack with a Battery Management System (BMS) and a Buck Converter to step down voltage for the electronics.
* **Audio Input:** USB Lavalier Microphone (Selected specifically to isolate human speech from the mechanical vibrations of the DC motors).
* **Audio Output:** USB Speakers.
* **Display:** 7-inch HDMI Display mounted at a 15-degree tilt for optimal viewing.
* **Drive System:** 4x DC Geared Motors controlled by an L298N Motor Driver Module.

---

## 💻 Software & Environment Setup

The cognitive architecture utilizes a decoupled design, separating the background AI inference server from the Python software orchestrator.

### 1. Prerequisites
Ensure you have the following installed on your development environment (or the Raspberry Pi):
* **Python 3.10+**
* **SQLite3** (for the telemetry database).
* A local LLM server. The `localbrain.py` orchestrator expects an OpenAI-compatible API running locally at `http://127.0.0.1:8080/v1/chat/completions`. (We recommend `llama.cpp` for running the BitNet 1.58b model).

### 2. Clone and Initialize the Environment
Clone the repository and set up your Python virtual environment:
```bash
git clone [https://github.com/](https://github.com/)[Your_Username]/mecha_tutor.git
cd mecha_tutor

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

```

### 3. Install Dependencies

Install the required libraries for the vector database, embeddings, and routing logic:

```bash
pip install langchain-chroma langchain-huggingface sentence-transformers requests numpy

```

*(Note: To ensure the system remains completely offline, the embedding model `all-MiniLM-L6-v2` is configured to run using local files only via `HF_HUB_OFFLINE=1`).*

---

## 🧠 Engineering Constraints: The 4GB RAM Defense

Deploying a Generative AI tutor natively on a **4GB Raspberry Pi 5** requires strict memory management. The system architecture is mathematically bounded to ensure feasibility without triggering Out-Of-Memory (OOM) OS crashes.

| Component | Engineering Calculation | Memory Cost (RAM) |
| --- | --- | --- |
| **Model Weights** | $2.4\text{B param} \times 1.58 \text{ bits} / 8$ (quantized) | **$\approx 0.48 \text{ GB}$** |
| **KV Cache** | $2 \times N_{l}(24) \times N_{h}(32) \times D_{h}(64) \times N_{ctx}(2048) \times 2\text{b}$ | **$\approx 0.40 \text{ GB}$** |
| **RAG/Knowledge** | ChromaDB Index for curriculum micro-chunks | **$\approx 0.01 \text{ GB}$** |
| **Operating System** | Raspberry Pi OS (Bookworm 64-bit) baseline | $\approx 1.00 \text{ GB}$ |
| **Total Usage** |  | **$\approx 1.89 \text{ GB}$** |

> **Conclusion:** By utilizing extreme 1.58-bit ternary quantization, the entire cognitive architecture consumes less than 2.0 GB of RAM. This leaves over **2.0 GB of free overhead** on the 4GB Pi 5 for audio processing, computer vision routines, and motor control logic.

---

## 🗄️ Database Initialization

Before running the tutor, you must initialize the localized SQLite telemetry database which handles user authentication and tracks student proficiency.

Run the provided SQL script to build the schema:

```bash
sqlite3 edge_tutor_data.db < data.sql

```

This will generate the required tables (`users`, `learning_profile`, `test_sessions`, etc.) optimized for fast lookups on the edge device.

---

## 🚀 Running the System

**1. Start the Local Inference Server**
Before launching the Python orchestrator, ensure your local LLM (BitNet 1.58b) is actively running and listening on port `8080`.

**2. Launch the Orchestrator**
Run the main cognitive loop. The system will load the `all-MiniLM-L6-v2` embedding model, initialize the ChromaDB connection, and start the semantic router.

```bash
python3 localbrain.py

```

### How the Pipeline Works

When you interact with the terminal:

1. **Semantic Routing:** The `Semantic_router` intercepts the query. If it detects casual small talk (e.g., "hello"), it bypasses the database.
2. **Knowledge Retrieval (RAG):** If technical keywords are detected, the `RAG` module queries the local `chroma_db`. It enforces a strict cosine distance threshold of `0.4` to prevent hallucinations.
3. **Generation:** The context and the query are merged and streamed to the local LLM server to generate a response.

---

## 👥 Contributors (Group A)

* Bajeh Abel O.
* Kochnet Emmanuella S.
* Ashiebi Augustine U.
* Chigbu Emmanuel U.

**Supervisors:** Dr. K.O Shobowale and Engr T.E. Agov

```

```

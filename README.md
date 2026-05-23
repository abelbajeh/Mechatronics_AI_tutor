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

## 💻 Software & Environment Setup (Raspberry Pi OS Lite / SSH)

The cognitive architecture utilizes a decoupled design, separating the background AI inference server from the Python software orchestrator. Because the system runs headlessly via SSH, we use terminal multiplexers (`tmux`) to keep the AI server running in the background.

### 1. System Prerequisites
Update your package list and install the necessary build tools and dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv sqlite3 git build-essential cmake tmux wget curl

```

### 2. Clone and Initialize the Environment

Clone the repository and set up your Python virtual environment:

```bash
git clone [https://github.com/](https://github.com/)[Your_Username]/mecha_tutor.git
cd mecha_tutor

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Install Python Dependencies

Install the required libraries for the vector database, embeddings, and routing logic:

```bash
pip install langchain-chroma langchain-huggingface sentence-transformers requests numpy

```

*(Note: To ensure the system remains completely offline, the embedding model `all-MiniLM-L6-v2` is configured to run using local files only via `HF_HUB_OFFLINE=1`).*

---

## 🧠 BitNet 1.58b Inference Server Setup

To serve the quantized BitNet model as a local API, we compile `llama.cpp` directly on the Raspberry Pi 5 to take advantage of the Cortex-A76 ARM NEON optimizations.

**1. Clone and Compile llama.cpp:**

```bash
# Navigate to your home directory or a dedicated tools folder
cd ~
git clone [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
cd llama.cpp

# Compile using all 4 cores of the Pi 5
make -j4

```

**2. Download the Quantized Model:**
Create a models directory and download your specific BitNet/1.58b `.gguf` file. *(Replace the URL below with the actual HuggingFace download link for your specific BitNet model).*

```bash
mkdir models
wget -O models/bitnet_1.58b.gguf "[https://huggingface.co/your-model-link-here/resolve/main/model.gguf](https://huggingface.co/your-model-link-here/resolve/main/model.gguf)"

```

**3. Start the Inference Server in the Background:**
Because you are connected via SSH, closing the terminal will kill the server. We use `tmux` to keep it running.

```bash
# Start a new tmux session named 'llm_server'
tmux new -s llm_server

# Run the server (2048 context window, port 8080)
./llama-server -m models/bitnet_1.58b.gguf -c 2048 --port 8080 --host 127.0.0.1

```

*To detach from the tmux session and leave it running in the background, press `Ctrl+B`, then release and press `D`.*

*(To re-attach later to check logs: `tmux attach -t llm_server`)*

---

## 🗄️ Database Initialization

Before running the tutor, you must initialize the localized SQLite telemetry database which handles user authentication and tracks student proficiency.

Navigate back to your `mecha_tutor` directory and run the provided SQL script to build the schema:

```bash
cd ~/mecha_tutor
sqlite3 edge_tutor_data.db < data.sql

```

---

## 🚀 Running the System

**1. Verify the Local Inference Server**
Ensure your `llama-server` is running in the background (via `tmux`) and listening on port `8080`.

**2. Launch the Orchestrator**
Run the main cognitive loop. The system will load the `all-MiniLM-L6-v2` embedding model, initialize the ChromaDB connection, and start the semantic router.

```bash
# Ensure your virtual environment is active
source .venv/bin/activate

# Start the tutor
python3 localbrain.py

```

### How the Pipeline Works

When you interact with the terminal:

1. **Semantic Routing:** The `Semantic_router` intercepts the query. If it detects casual small talk (e.g., "hello"), it bypasses the database.
2. **Knowledge Retrieval (RAG):** If technical keywords are detected, the `RAG` module queries the local `chroma_db`. It enforces a strict cosine distance threshold of `0.4` to prevent hallucinations.
3. **Generation:** The context and the query are merged and streamed to the local LLM server to generate a response.

---

## ⚖️ Engineering Constraints: The 4GB RAM Defense

Deploying a Generative AI tutor natively on a **4GB Raspberry Pi 5** requires strict memory management. The system architecture is mathematically bounded to ensure feasibility without triggering Out-Of-Memory (OOM) OS crashes.

| Component | Engineering Calculation | Memory Cost (RAM) |
| --- | --- | --- |
| **Model Weights** | $2.4\text{B param} \times 1.58 \text{ bits} / 8$ (quantized) | **$\approx 0.48 \text{ GB}$** |
| **KV Cache** | $2 \times N_{l}(24) \times N_{h}(32) \times D_{h}(64) \times N_{ctx}(2048) \times 2\text{b}$ | **$\approx 0.40 \text{ GB}$** |
| **RAG/Knowledge** | ChromaDB Index for curriculum micro-chunks | **$\approx 0.01 \text{ GB}$** |
| **Operating System** | Raspberry Pi OS Lite (Headless 64-bit) baseline | $\approx 0.30 \text{ GB}$ |
| **Total Usage** |  | **$\approx 1.19 \text{ GB}$** |

> **Conclusion:** By utilizing extreme 1.58-bit ternary quantization and running a headless OS, the entire cognitive architecture consumes less than 1.2 GB of RAM. This leaves over **2.8 GB of free overhead** on the 4GB Pi 5 for audio processing, semantic routing arrays, and motor control logic.

---

## 👥 Contributors (Group A)

* Bajeh Abel O.
* Kochnet Emmanuella S.
* Ashiebi Augustine U.
* Chigbu Emmanuel U.

**Supervisors:** Dr. K.O Shobowale and Engr T.E. Agov

```

```

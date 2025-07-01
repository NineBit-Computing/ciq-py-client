# 🧠 NineBit CIQ Python SDK

![](banner.png)
[![Version](https://img.shields.io/pypi/v/ninebit-ciq)](https://pypi.org/project/ninebit-ciq)
[![License](https://img.shields.io/github/license/NineBit-Computing/ciq-py-client)](https://github.com/NineBit-Computing/ciq-py-client/blob/main/LICENSE)

Official Python client for interacting with [NineBit CIQ](https://ciq.ninebit.in), a Retrieval-Augmented Generation (RAG) workflow orchestration platform for rapid prototyping of AI/ML ideas using enterprise data and open-source models.

---

## 🚀 Features

- 🔐 Auth via API Key (`X-API-Key` header)
- ⚙️ Trigger & track workflows (synchronously or asynchronously)
- 🔄 Get live workflow status
- 🧵 Non-blocking execution via threads
- 🧰 CLI support for easy experimentation
- 📦 Lightweight, synchronous, and logging-enabled

---

## 📦 Installation

```bash
pip install ninebit-ciq
```

Or clone and install locally:

```
git clone https://github.com/NineBit-Computing/ciq-py-client.git
cd ciq-py-client
pip install .
```

## 🧪 Quickstart (Python)

```python
from ninebit_ciq import NineBitCIQClient

client = NineBitCIQClient(
    api_key="YOUR_API_KEY"
)

def on_done(error, data):
    if error:
        print(f"Task failed: {error}")
    else:
        print(f"Task succeeded: {str(data)}")

# 1. Ingest file as datasource for performing RAG
client.ingest_file(file="files/my_file.pdf", callback=on_done)

# 2. Ask your query
client.rag_query(query="What is axiom?", callback=on_done)

```

## 🧠 Non-Blocking Workflow Monitoring

CIQ workflows are asynchronous — they may take time to complete. You can track them without blocking the main thread.

▶ Python (Threaded)

```python
import threading
from ninebit_ciq import NineBitCIQClient

def on_complete(result):
    print("Workflow finished:", result)

def wait_async(client, wf_id):
    result = client.wait_for_completion(wf_id)
    on_complete(result)

client = NineBitCIQClient(api_key="YOUR_API_KEY")
wf_id = client.trigger_workflow({"input": "data"})

threading.Thread(target=wait_async, args=(client, wf_id)).start()
print("Main thread is free to do other work.")
```

## 🔐 Authentication

Pass your API Key using the X-API-Key header:

Python SDK: NineBitCIQClient(api_key)

## 📚 SDK Reference

| Method                                                | Description                                 |
| ----------------------------------------------------- | ------------------------------------------- |
| `get_design_time_workflow()`                          | Fetches the base workflow configuration     |
| `trigger_workflow(data: dict)`                        | Triggers a new workflow and returns `wf_id` |
| `get_workflow_status(wf_id)`                          | Gets the current status of a workflow       |
| `wait_for_completion(wf_id, interval=5, timeout=300)` | Polls until the workflow completes          |

## 🛠️ Logging

You can control logging verbosity:

```python
from ninebit_ciq import NineBitCIQClient
import logging

client = NineBitCIQClient(api_key, log_level=logging.INFO)
```

## 📁 Project Structure

```
ciq-py-client/
├── src/ninebit_ciq/
│ ├── client.py # Core SDK logic
│ ├── logger.py # Logger setup
│ ├── cli.py # CLI interface
│ └── **init**.py # Version info
├── examples/usage.py
├── examples/usage_with_thread.py
├── README.md
├── setup.py
└── version.txt
```

## 📄 License

MIT License © NineBit Computing

## ✉️ Contact

Questions? Reach out via ninebit.in or raise an issue in the GitHub repo.

## Contributing

While we value open-source contributions to this SDK, the code is generated programmatically. Additions made directly would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

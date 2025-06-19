# NineBit CIQ Client

Internal Python client for communicating with the NineBit CIQ backend.

> 🚫 This package is **not open source**. Do not publish to public indexes like PyPI.

Sure! Here's the same information in **Markdown format**, ready to copy into your `README.md` or internal docs:

---

## 📦 Packaging & Dependencies (Python Library)

- ✅ Declare **runtime dependencies** in `setup.cfg` under `install_requires`  
  → Example: `requests>=2.31.0`
- ❌ Do **not** use `requirements.txt` for consumers
- ✅ Use `requirements.txt` for **development & testing** (optional)
- ❌ Do not bundle source code of dependencies (like vendoring `requests`)

---

## 🚀 Steps to Build & Publish to PyPI

1. **[Optional] Create virtual environment:**

   ```bash
   python3.11 -m venv .venv && source .venv/bin/activate
   ```

2. **Install required tools:**

   ```bash
   pip install --upgrade build twine
   ```

3. **Build the package:**

   ```bash
   python -m build
   ```

4. **Configure `~/.pypirc`** (once):

   ```ini
   [pypi]
   username = __token__
   password = pypi-<your-api-token>
   ```

5. **Upload to PyPI:**

   ```bash
   python -m twine upload dist/*
   ```

---

✅ After the first upload, consumers can install with:

```bash
pip install ninebit-ciq
```

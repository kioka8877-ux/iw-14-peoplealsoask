# IW-14 PeopleAlsoAsk

> People Also Ask + Related Searches
> Part of the **PERTURABO Iron Warriors** fleet — SERP/Search API siege.

## 🎯 What It Does

Content research, questions

## 📡 API Endpoints

### `/extract`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | ✅ | — | Search query |
| `gl` | string | ❌ | "us" | Country code |
| `hl` | string | ❌ | "en" | Language code |

### Response Format

```
JSON (questions + answers + source_url)
```

## 💰 Why This Exists

**Target beaten:** Google SERP Scraper

This Iron Warrior is self-hosted — no RapidAPI 25% commission, no marketplace tax.
Deploy it on your own infrastructure and pay $0 per request.

## 🚀 Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn httpx beautifulsoup4 pydantic

# Run the Iron Warrior
cd IW-14_PeopleAlsoAsk
uvicorn main:app --host 0.0.0.0 --port 8000

# Test it
curl "http://localhost:8000/extract?q=test"
```

## 🏗️ Architecture

```
IW-14_PeopleAlsoAsk/
├── main.py          # FastAPI app with endpoint(s)
├── shared/
│   └── base.py      # Shared module (HTTP client, parsing, models)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

Built with:
- **FastAPI** — async web framework with auto-generated docs (`/docs`)
- **httpx** — async HTTP client
- **BeautifulSoup4** — HTML parsing
- **Pydantic v2** — type-safe response models

## 📊 Cost Comparison

| Provider | Cost per 10K requests | This Iron Warrior |
|---|---|---|
| RapidAPI (with 25% commission) | Google SERP Scraper | **$0** (self-hosted) |

## 🔗 Part of PERTURABO

This Iron Warrior is one of 20 specialized SERP wrappers forged during the
PERTURABO API siege. Each wrapper targets a specific search vertical.

**Fleet status:** 20/20 operational
**Total fleet code:** 2,007 lines
**Shared module:** `base.py` (127 lines)

```markdown
# AI Merch Maker Lite – Simplified Edition

A minimal four-language pipeline that simulates AI-powered merch creation, mock-up generation, and “publishing” via a lightweight Java HTTP server. No paid API keys or external dependencies—everything runs on built-in libraries and a sample image.

---

## Repository Layout

```
ai-merch-maker-lite/
├── python/
│   └── product_generator.py
├── javascript/
│   └── mockup_generator.js
├── java/
│   └── ProductPublisher.java
├── orchestrator/
│   └── pipeline_orchestrator.py
├── sample_image.jpg
├── .gitignore
└── README.md
```

---

## Prerequisites

- **Python** 3.7+  
  (`python --version`)
- **Node.js** 12+  
  (`node --version`)
- **Java** 11+ (JDK)  
  (`java -version`)

_No additional packages, modules or JARs required._

---

## Quick-Start

### 1. Clone the repo

```
git clone https://github.com/your-username/ai-merch-maker-lite.git
cd ai-merch-maker-lite
```

### 2. Add a sample image

Place any `.jpg` in the root and name it:

```
sample_image.jpg
```

This stands in for the DALL-E output.

### 3. Compile & launch the Java server

```
cd java
javac ProductPublisher.java
java ProductPublisher
```

Server runs on → `http://localhost:8080`

Leave this terminal open.

### 4. Run the full pipeline

Open a second terminal in the project root:

```
python orchestrator/pipeline_orchestrator.py vintage
```

**What happens:**

1. **Python** generates `product_data_.json` + `product_.jpg`.  
2. **Node.js** creates `mockup_data_.json`.  
3. **Python orchestrator** POSTs data to the Java server → appends to `products_database.json` + logs in `published_products.log`.  
4. A final report is saved as `pipeline_result_.json`.

### 5. Inspect & test

- **Database**: `products_database.json`  
- **Logs**: `published_products.log`  
- **Orchestrator report**: `pipeline_result_.json`

Test HTTP endpoints:

```
curl http://localhost:8080/health
curl http://localhost:8080/stats
curl http://localhost:8080/products
```

---

## Running Components Individually

| Task                       | Command                                                                  |
|----------------------------|--------------------------------------------------------------------------|
| Generate product only      | `python python/product_generator.py minimalist`                          |
| Create mock-up only        | `node javascript/mockup_generator.js product_data_.json`            |
| Publish manually           | `curl -X POST http://localhost:8080/publish -H "Content-Type: application/json" -d @product_data_.json` |

---

## Simulating a Daily Schedule

```
python orchestrator/pipeline_orchestrator.py space schedule
```

> In demo mode it still runs once, but the code shows where a real cron/Task Scheduler hook would go.

---

## Clean-Up Helpers

```
rm product_*.jpg mockup_*.jpg
rm product_data_*.json mockup_data_*.json pipeline_result_*.json
rm products_database.json published_products.log
```


```

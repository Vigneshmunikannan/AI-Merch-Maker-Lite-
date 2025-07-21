```markdown
# AI Merch Maker Lite – Simplified Edition

A minimal four-language pipeline that simulates AI-powered merch creation, mock-up generation, and “publishing” via a lightweight Java HTTP server. No paid API keys or external dependencies—everything runs on built-in libraries and a sample image.

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
git clone github url
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

```

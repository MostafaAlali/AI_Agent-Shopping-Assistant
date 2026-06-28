# 🛒 AI Shopping Agent (Text + Image)

An agentic multi-modal shopping assistant that enables users to discover products using both natural language and images, retrieve inventory data from SQLite, enrich results with ratings, and place orders through a controlled confirmation workflow.

---

## 🚀 Problem

Traditional e-commerce search often fails to understand what customers actually want.

Users may:

* Struggle to describe products accurately using text
* Depend on unreliable visual search systems
* Receive irrelevant search results
* Spend excessive time finding the right product

These challenges lead to:

* Slow product discovery
* Poor user experience
* Lower conversion rates
* Increased search abandonment

---

## 💡 Solution

AI Shopping Agent combines LLM reasoning, image understanding, and tool orchestration to create a smarter shopping experience.

The system can:

* Understand natural language shopping requests
* Analyze uploaded product images
* Extract product attributes using a vision-capable LLM
* Search a local product inventory
* Retrieve customer ratings
* Present ranked recommendations
* Place orders only after explicit user confirmation

---
Try the agent by you self for here:[AI Shopping Assistant](https://aiagent-shopping-assistant-1.streamlit.app/)

---
## 🎯 Benefits

### For Customers

* Faster product discovery
* Better search accuracy
* Visual product search
* Conversational shopping experience

### For Businesses

* Higher conversion rates
* Better customer engagement
* Reduced search abandonment
* Scalable AI-powered product discovery

---

## 🏗️ Architecture

The application is built around a LangChain agent that dynamically selects tools based on user intent.

```text
User (Text / Image)
          │
          ▼
   Streamlit Chat UI
          │
          ▼
   LangChain Agent
          │
 ┌────────┼────────┐
 │        │        │
 ▼        ▼        ▼
Vision   Search   Ratings
 Tool     Tool      Tool
 │         │         │
 └─────┬───┴────┬────┘
       │        │
       ▼        ▼
     SQLite Inventory
     Reviews
       │
       ▼
  Agent Response
       │
       ▼
 Checkout Tool
       │
       ▼
 Orders Database
```

---

## 🧰 Tools

### `search_products(query, max_price, is_organic)`

Searches the SQLite inventory database based on:

* Product keywords
* Maximum price
* Organic preference

Returns matching products.

---

### `get_rating(product_id)`

Retrieves customer ratings for a product.

Used to:

* Rank products
* Filter results
* Provide richer recommendations

---

### `describe_prduct_image(image_path)`

Uses a Groq-hosted vision model to:

1. Analyze the uploaded image
2. Extract product attributes
3. Generate structured JSON
4. Convert attributes into a searchable query



---

### `checkout(product_id)`

Places an order by inserting a new row into the SQLite `orders` table.

Safety guardrails ensure that checkout occurs only after explicit user confirmation.

---

## 🤖 Agent Behavior

The system prompt enforces strict shopping workflows.

### Image Search

When an image is uploaded:

1. Agent calls `describe_prduct_image`
2. Extracts product attributes
3. Generates a search query
4. Searches inventory
5. Returns ranked recommendations

---

### Browsing

When users search for products:

1. Agent calls `search_products`
2. Retrieves candidates
3. Calls `get_rating` for each candidate
4. Filters and ranks results
5. Displays products with explicit IDs

Example:

```text
#1 Premium Organic Coffee (ID:12)
Price: $14.99
Rating: ★4.8

#2 Dark Roast Espresso (ID:25)
Price: $18.99
Rating: ★4.6
```

---

### Ordering

The agent:

* Never orders automatically
* Requires explicit confirmation
* Verifies the selected product ID originated from a previous recommendation

Example:

```text
User: Order number 2


Agent:
Order placed successfully.
```

---

## ✨ Features

* 🧠 Multi-modal shopping (text + image)
* 🖼️ Image-to-search workflow
* 🔄 Agentic tool routing
* ⭐ Ratings-aware recommendations
* 🛒 Safe checkout flow
* 💬 Conversational memory
* 💻 Streamlit chat interface
* 🛡️ Guardrails against accidental purchases

---

## 🧠 Tech Stack

| Component              | Technology       |
| ---------------------- | ---------------- |
| Language               | Python           |
| Agent Framework        | LangChain        |
| LLM Provider           | Groq             |
| LLM Models             | Groq-hosted LLMs |
| Vision                 | Multimodal LLM   |
| Frontend               | Streamlit        |
| Database               | SQLite           |
| Environment Management | python-dotenv    |
| Ratings Integration    | reviews_api      |

---

## ⚙️ Installation

### Prerequisites

* Python 3.8+
* Groq API Key

---

### Clone Repository

```bash
git clone https://github.com/MostafaAlali/AI_Agent-Shopping-Assistant.git

cd ai-shopping-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 📖 Example Workflow

### Scenario A: Text Browsing → Order

User:

```text
organic apple under $20 with rating 4.5+
```

Agent:

```text
#1 Organic Green Apple (ID:5)
$12.99 ★4.7

#2 Organic Red Apple (ID:8)
$14.99 ★4.8
```

User:

```text
order number 2
```

Agent:

```text
Order placed successfully.
```

---

### Scenario B: Image Search

1. Upload a product image
2. Vision model extracts attributes
3. Agent searches inventory
4. Results displayed with IDs
5. User confirms purchase

---

## 📂 Project Structure

```text
ai-shopping-agent/
│
├── app.py
├── shopping_agent.py
├── store.db
├── requirements.txt
├── .env.example
└── README.md
```

---


## 🔮 Future Improvements

* Rename `describe_prduct_image` → `describe_product_image`
* Integrate `ratings.py:get_ratings_for_products()` directly into ranking pipeline
* Replace temporary image files with in-memory processing
* Add structured UI filters:

  * Maximum price
  * Organic toggle
  * Minimum rating
* Personalized recommendations
* Multi-language support
* Real-time inventory updates

---


## 📜 License

MIT License

See the LICENSE file for details.

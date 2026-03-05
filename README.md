# LangGraph E-Commerce Support Chatbot

An AI-powered customer support chatbot built as a learning project to explore multi-agent architectures with LangGraph, retrieval augmented generation (RAG), and natural language processing.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55+-red.svg)](https://streamlit.io)

## Project Overview

This project implements an intelligent customer support assistant that can:
- Track order status and delivery information
- Process return and refund requests
- Answer policy-related questions using RAG
- Create support tickets for complex issues
- Route queries to specialized agents based on intent

## Architecture

```
Customer Query (Streamlit UI)
         |
   Intent Classifier
         |
    +---------+---------+---------+
    |         |         |         |
Order Agent  Refund  Policy  Support
(Database)   Agent   Agent   Agent
             (DB)    (RAG)   (DB)
```

## Technology Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (Llama 3.1 8B)
- **Database**: PostgreSQL
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Framework**: LangChain, LangGraph

## Features

### 1. Order Tracking
Query order status, tracking numbers, and estimated delivery dates from the database.

### 2. Refund Processing
Automated refund request creation with database integration.

### 3. Policy Q&A
Retrieval Augmented Generation (RAG) system that searches through company policies to answer customer questions about returns, shipping, and FAQs.

### 4. Support Tickets
Creates support tickets for complex issues like payment failures or account problems.

### 5. Intent-Based Routing
Automatically routes customer queries to the appropriate specialized agent.

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 18
- Groq API key (free at https://console.groq.com)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/git4k/-E-Commerce-Support-Chatbot.git
cd -E-Commerce-Support-Chatbot
```

2. Create virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup configuration:
```bash
# Copy example config
cp config.example.py config.py

# Edit config.py and add:
# - Your Groq API key
# - Your PostgreSQL password
```

5. Setup PostgreSQL database:
```sql
CREATE DATABASE ecommerce_support;
```

Then run the table creation SQL from the Database Schema section below.

6. Seed the database:
```bash
python app/db/seed_data.py
```

7. Run the app:
```bash
streamlit run streamlit_app_simple.py
```

8. Open browser: http://localhost:8501

## Example Queries

### Order Status
- "Where is my order ORD101?"
- "Track order ORD150"
- "When will my order arrive?"

### Refunds
- "I want to return order ORD120"
- "My item arrived damaged"
- "How do I get a refund?"

### Policies
- "What is your return policy?"
- "How long does shipping take?"
- "Do you offer free shipping?"

### Support
- "My payment failed"
- "I can't log into my account"
- "I need help with a billing issue"

## Database Schema

### Orders Table
```sql
order_id TEXT PRIMARY KEY
customer_id INT
order_status TEXT (processing/shipped/delivered/cancelled)
tracking_number TEXT
order_date TIMESTAMP
estimated_delivery TIMESTAMP
```

### Refunds Table
```sql
refund_id SERIAL PRIMARY KEY
order_id TEXT
status TEXT
created_at TIMESTAMP
```

### Tickets Table
```sql
ticket_id SERIAL PRIMARY KEY
customer_id INT
issue_type TEXT
description TEXT
status TEXT
created_at TIMESTAMP
```

## Project Structure

```
langgraph-ecommerce-support/
├── app/
│   ├── agents/
│   │   └── agents.py          # Agent definitions
│   ├── tools/
│   │   └── tools.py           # Database interaction tools
│   ├── db/
│   │   └── seed_data.py       # Database seeder
│   ├── rag/
│   │   └── rag_engine.py      # FAISS vectorstore
│   └── graph/
│       └── workflow.py        # LangGraph orchestration
├── data/
│   └── policies/              # Policy documents
│       ├── faq.md
│       ├── return_policy.md
│       └── shipping_policy.md
├── config.py                  # Configuration
├── streamlit_app_simple.py    # Main application
└── requirements.txt           # Dependencies
```

## System Workflow

1. User sends message via Streamlit interface
2. Intent classifier analyzes the query
3. Routes to appropriate agent:
   - Policy question → RAG Agent (searches vectorstore)
   - Order query → Order Agent (queries database)
   - Refund request → Refund Agent (creates refund record)
   - Complex issue → Support Agent (creates ticket)
4. Agent executes tools and generates response
5. Response displayed to user

## Performance

- First query: 5-10 seconds (loading embeddings model)
- Subsequent queries: 0.3-0.5 seconds
- Database queries: <100ms
- RAG search: Cached after first use

## Security Features

- No internal analytics queries allowed
- Customer data isolation
- SQL injection prevention via parameterized queries
- API keys stored in config (not committed to git)

## Learning Outcomes

This project helped me learn:
- Multi-agent system design and orchestration
- Retrieval Augmented Generation (RAG) implementation
- Vector embeddings and similarity search
- Intent classification and routing
- Database integration with AI systems
- Production-ready application structure

## Future Enhancements

- Add conversation memory for multi-turn dialogues
- Implement email notifications for tickets/refunds
- Build admin dashboard for analytics
- Add voice input support
- Support multiple languages
- Integrate with real e-commerce platforms

## Dependencies

Key packages:
- langchain & langgraph - Agent framework
- psycopg2-binary - PostgreSQL connector
- sentence-transformers - Embeddings
- faiss-cpu - Vector search
- streamlit - Web UI
- langchain-groq - LLM integration

## License

MIT License - Feel free to use for learning and portfolio projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or feedback, please open an issue on GitHub.

---

If you found this project helpful, please give it a star!

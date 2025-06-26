# 🦙 Website Article Summarization using LLaMA 2 (Ongoing Project)

This project focuses on building an efficient, domain-adaptive summarization system using the **LLaMA 2 7B** language model. It leverages **parameter-efficient fine-tuning (PEFT)** techniques to make summarization viable even on resource-constrained devices. The system retrieves and parses live website data, and generates coherent, factual summaries tailored for real-world usability.

> ⚠️ **Note:** This is an active development project. Model training and system integration are ongoing.

---

## 🔍 Problem Statement

In a world flooded with unstructured and noisy web content, users struggle to extract key information quickly. Traditional summarization techniques fall short in scalability, factual reliability, and hardware efficiency. This project addresses these issues through:

- Retrieval-augmented summarization
- Lightweight deployment strategies
- Custom training on real-world web content

---

## 🚀 Project Objectives

- Fine-tune **LLaMA 2 7B** using **LoRA** for efficient training and deployment.
- Summarize dynamic website content retrieved using **Serper API**.
- Parse and clean HTML content using **BeautifulSoup**.
- Build an interactive front-end using **Streamlit**.

---

## 🛠️ Tech Stack

- `Python`
- `LLaMA 2 7B` via Hugging Face Transformers
- `PEFT` (LoRA)
- `Serper API` for Google Search results
- `BeautifulSoup` for web scraping
- `Streamlit` for interactive UI

---

## 📈 Target Metrics (In Progress)

| Metric                  | Target Value                  |
|------------------------|-------------------------------|
| ROUGE-L                | > 40                          |
| Inference Time         | < 2 seconds/article           |
| Model Size Reduction   | 40–60% via LoRA               |
| Human Eval Score       | > 4.0 / 5.0 on summary quality|

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yaseeng-md/llama-website-summarization.git
cd llama-website-summarization

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

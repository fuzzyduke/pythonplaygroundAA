# 🧠 Python LLM & Document Querying – Exercise Summary

## 📌 Objective
We explored **local Large Language Models (LLMs)** and **document-based querying** using FAISS, LangChain, and Hugging Face embeddings. The goal was to process PDFs, convert them into an easily searchable format, and enable querying from a local LLM.

---

## 🛠️ Exercise 1: Setting Up a Local LLM
**What We Did:** Attempted to run a **LLaMA-based model (Hermes 3)** locally.

### ✅ **Approach**
- Installed `llama-cpp-python` (Faced dependency issues)
- Explored **GPT4All** as an alternative
- Successfully ran **GPT4All** with `langchain`

### 🎯 **Outcome**
- Successfully loaded and queried a local LLM.

---

## 📂 Exercise 2: Indexing PDFs into FAISS
**What We Did:** Converted PDFs into vector embeddings using **FAISS** (Facebook AI Similarity Search).

### ✅ **Approach**
1. Loaded PDFs from a folder (`kb/`)
2. Used **`HuggingFaceEmbeddings`** to generate embeddings.
3. Stored them in a **FAISS vector database**.

### 🎯 **Outcome**
- Successfully created a searchable index for the PDF content.

---

## ❓ Exercise 3: Querying FAISS Without LLM
**What We Did:** Queried the FAISS database for **relevant text chunks**.

### ✅ **Approach**
- Loaded FAISS vectors.
- Retrieved the most relevant pieces of text based on a user question.
- **No LLM was used** in this step.

### 🎯 **Outcome**
- Retrieved matching document chunks but **did not generate answers**.

---

## 🧠 Exercise 4: Combining FAISS & LLM
**What We Did:** Integrated **FAISS** with an **LLM** to generate responses.

### ✅ **Approach**
1. Queried **FAISS** to retrieve relevant document snippets.
2. Passed the retrieved text to a local **LLM (GPT4All)** to generate an answer.

### 🎯 **Outcome**
- Now, users could ask **questions based on document content** and get meaningful responses.

---

## 🛠️ Exercise 5: Troubleshooting & Fixes
### 🛑 **Errors Encountered & Solutions**
- **Installation Issues:** Fixed missing packages (`langchain_community`, `sentence-transformers`).
- **FAISS Pickle Security Warning:** Enabled safe deserialization.
- **GitHub Sync Issues:** Used `git pull --rebase` before pushing.

---

## 🔗 Final Result
Users can now:
✅ **Upload PDFs** → **Index into FAISS** → **Query Documents** → **Get Answers via Local LLM**.

This setup allows **local, private, and efficient AI-driven document querying** without relying on cloud-based APIs.

---

## 🚀 Next Steps
- Improve response accuracy by fine-tuning the **retrieval process**.
- Add a **UI** for easier interaction.
- Experiment with **different LLMs** for better generation.

This exercise provides a **strong foundation** for building **offline AI-powered knowledge retrieval systems**! 🔥

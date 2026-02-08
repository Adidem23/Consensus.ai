# 🧠 LLM Debate Agent

> A multi-agent reasoning system that debates complex questions, evaluates arguments, and produces more reliable, explainable AI outputs.


## 📌 Problem Statement

Large Language Models (LLMs) often:
- Produce confident but incorrect answers
- Struggle with controversial or subjective questions
- Provide single-perspective reasoning
- Lack transparent evaluation of their own responses

For decision-making, learning, and analysis, a single LLM response is not enough.  
Users need **balanced reasoning**, **counter-arguments**, and **measurable confidence**.


## 💡 Proposed Solution

The **LLM Debate Agent** introduces a **multi-agent debate architecture** where multiple LLMs independently reason from opposing perspectives, followed by an unbiased evaluation agent.

Instead of asking:

> *“What is the answer?”*

We ask:

> **“What are the strongest arguments for and against this claim, and which one stands up to scrutiny?”**

This approach improves:
- Answer reliability
- Reasoning transparency
- Trustworthiness of LLM outputs


## 🏗️ System Architecture

### 📐 Architecture Overview

The system is designed as a graph-based multi-agent workflow where each agent has a well-defined role and execution boundary.

**Key components:**
- **Pro Agent** – argues in favor of the claim
- **Con Agent** – argues against the claim
- **Judge Agent** – evaluates arguments and produces the final verdict

<img width="1916" height="767" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/6f148b1f-abd8-49fa-8f24-428fdf662a88" />


### 🔁 Execution Flow

The debate follows a structured, step-by-step flow:

1. User submits a question or claim  
2. Pro and Con agents generate independent arguments  
3. (Optional) Multi-round rebuttals enhance depth  
4. Judge agent evaluates arguments on quality and relevance  
5. Final verdict and scores are returned to the user  

<img width="4000" height="1000" alt="Flow Chart" src="https://github.com/user-attachments/assets/9009a5a1-dcba-4b89-a00f-2b8ccf4a0404" />


## 🎥 Project Walkthrough & Demo

- **Architecture Summary Video**  
  👉 https://youtu.be/YYz59eWWCT0

- **End-to-End Demo Video**  
  👉 https://youtu.be/-n4D94Ny4ek?si=sbvnMG049G9L5ke2


## 🚀 Why This Matters

Unlike traditional single-response LLM systems, the **LLM Debate Agent**:
- Makes disagreement explicit
- Encourages deeper reasoning
- Provides evaluative confidence instead of blind trust

This makes it suitable for **decision support**, **education**, and **LLM evaluation workflows**.


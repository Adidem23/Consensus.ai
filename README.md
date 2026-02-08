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

The system is designed as council of Different LLM nodes where they critique each others output and one supervisor Node handles LLM responses and gives most relevant output 

**Key components:**
- **Supervisor Agent** – Delegates user query to all nodes in LLM Debate and Gathers final output of all and returns most realiable output
- **LLM Nodes** – They Critique with each other enhances their output and then send final Answer to Supervisor Ndoe 
- **Central Autority** – This is central which knows which LLM has given answer which has given a critique . In brief it is LLM Debate State Manager 
- **Opik**- All LLM calls are being traced to comet opik 

<img width="1916" height="767" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/6f148b1f-abd8-49fa-8f24-428fdf662a88" />


### 🔁 Execution Flow

The debate follows a structured, step-by-step flow:

1. User submits a question or claim  
2. Supervisor delegates it to all llm nodes in Council 
3. LLM nodes generates one final output at their end 
4. LLM nodes sends the output to supervisor Node 
5. Supervisor Checks the most reelevant answer and returns Back to user  

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


## Tech Stack 👩🏾‍💻
## 🛠️ Tech Stack

<p align="left">
  <img src="https://raw.githubusercontent.com/langchain-ai/langgraph/main/docs/static/img/langgraph_logo.png" alt="LangGraph" height="50"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" height="50"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/openai/openai-original.svg" alt="OpenAI" height="50"/>
  <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/mistralai.svg" alt="Mistral" height="50"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" alt="Docker" height="50"/>
</p>

**LangGraph · Python · OpenAI · Mistral · Docker**




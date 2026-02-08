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


## 🤖 Tech Stack Used

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/175ee65f-1a64-4db1-9b00-1f65755bfed6" height="45"/><br/>
      <b>NextJs</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="45"/><br/>
      <b>Python</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/f2f4f0fb-0619-41f0-b0fd-cfadd644fd2b" height="45"/><br/>
      <b>FastApi</b>
    </td>
     <td align="center">
      <img src="https://github.com/user-attachments/assets/77bb4677-ec84-43de-9123-ee45d1fdeb32" height="45"/><br/>
      <b>Pydantic</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/e2ea7528-ba0c-4ff4-b6fb-b52412838634" height="45"/><br/>
      <b>MongoDB</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/c5cefdaf-22ce-4479-b585-3eb60f76eb93" height="45"/><br/>
      <b>Gemini</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/3be09b6f-42fc-4891-a2af-b0c7af519d86" height="45"/><br/>
      <b>Mistral</b>
    </td>
     <td align="center">
      <img src="https://github.com/user-attachments/assets/49a38bf5-adf5-43a5-b28a-6d647a8b9bec" height="45"/><br/>
      <b>Google ADK</b>
    </td>
     <td align="center">
      <img src="https://github.com/user-attachments/assets/1b48577c-4991-47a1-ab09-9c3d43fb31f9" height="45"/><br/>
      <b>LangGraph</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/23843af5-13ad-4489-b130-6ac67ed35640" height="45"/><br/>
      <b>A2A Protocol</b>
    </td>
     <td align="center">
      <img src="https://github.com/user-attachments/assets/8cc17a1c-f338-4e25-878c-2d5767c6ff45" height="45"/><br/>
      <b>Comet Opik</b>
    </td>
  </tr>
</table>





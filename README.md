# JobReady AI

> Turning a life-ending moment into a life-changing phase — through right guidance, awareness and information.

**JobReady AI is a GenAI-powered job search companion for mid-career professionals facing involuntary job loss.**

It is being built end-to-end — from product discovery through technical architecture to a deployable product — as a demonstration of both product management methodology and applied GenAI capability.

---

## The Problem

Mid-career professionals (30–42, 8–15 years experience) who are laid off, benched, or between contracts are trapped in a job search system they cannot see, understand, or navigate alone. They apply frantically, receive no feedback, and spiral into paralysis — turning a temporary disruption into a prolonged crisis.

JobReady AI exists to provide the guidance, awareness and information that turns that paralysis into structured, confident momentum.

---

## Who It's For

**Meet Rahul** — 37, Senior Software Engineer, 11 years of experience, laid off six weeks ago. Breadwinner. Young child. Applying without strategy, without feedback, without direction. JobReady AI is built for him.

---

## Core Features

| Feature | What it does |
|---------|--------------|
| **JD Analyser** | Paste a job description, get a fit score and gap analysis against your profile |
| **Application Tracker** | Log and monitor applications with pipeline visibility and stale-flagging |
| **Mock Interview Engine** | Role-specific Q&A with AI-evaluated feedback and scoring |
| **Daily Momentum Generator** *(planned)* | Micro-actions to beat paralysis and rebuild momentum |
| **Interview Question Generator** *(planned)* | Role-specific questions generated from any JD |

---

## How It's Being Built

This project follows a disciplined, phased product development lifecycle. Every phase produces real documentation — not just code.

### ✅ Phase 1 — Product Discovery & Definition
Complete. Six documents establishing who the user is, what their problem is, and what we will build.

- [Problem Statement](JobReadyAI_ProblemStatement.pdf)
- [User Persona](JobReadyAI_UserPersona.pdf)
- [User Journey Map](JobReadyAI_UserJourneyMap.pdf)
- [Product Requirements Document (PRD)](JobReadyAI_PRD.pdf)
- [RICE Prioritisation](JobReadyAI_RICE.pdf)
- [Success Metrics](JobReadyAI_SuccessMetrics.pdf)

### ✅ Phase 2 — Technical Architecture & Design
Complete. The engineering foundation — architecture, tech stack, LLM selection, prompt engine design.

- [Technical Design Document (TDD)](JobReadyAI_TechnicalDesignDocument.pdf)

### 🔨 Phase 3 — Build Sprint 1: Core Engine
In progress. Building the JD Analyser — the highest-priority feature — end-to-end in Google Colab.

### ⏳ Phase 4 — Build Sprint 2: Full Product
### ⏳ Phase 5 — Evaluation & Governance
### ⏳ Phase 6 — Documentation & Marketing

---

## Tech Stack

- **Python** — primary language
- **Google Colab** — development & runtime environment
- **Gemini API** — LLM engine (OpenAI as interchangeable fallback)
- **ReportLab** — PDF report generation
- **Pandas** — data handling for the Application Tracker
- **GitHub** — code storage and documentation

The architecture is **LLM-agnostic by design** — switching between Gemini and OpenAI requires changing a single configuration variable.

---

## Project Philosophy

1. **Every feature traces back to a real user problem.** No feature exists without a moment in the user's journey that justifies it.
2. **Every technical decision is defensible.** Tech choices are documented with rationale, not made by default.
3. **Outcomes are measured, not assumed.** Success metrics are defined before building.

---

## About the Builder

Built by **Aditya Nagaria** — Product & Program Manager with 13+ years of experience across Life Sciences GxP environments, CI/CD governance, DevOps and Agile delivery, now building at the intersection of product management and applied AI.

This project demonstrates the full product lifecycle: discovery, definition, prioritisation, architecture, and build — with the rigour of a regulated-industry background applied to GenAI product development.

---

*This is a living project. Documentation and code are updated as each phase progresses.*

# AI-Powered Agentic Workflow for Project Management

This repository contains a reusable agent toolkit and a multi-step workflow that turns a product specification into a structured project plan. The workflow is demonstrated with InnovateNext Solutions’ Email Router specification and is designed around the common technical project management artifacts of user stories, product features, and engineering tasks.

## Project Overview

The project has two connected parts:

- **Agent toolkit (`phase_1/`)** — reusable prompt, evaluation, routing, retrieval-augmented, and action-planning agents, with standalone examples for each agent.
- **Project planning workflow (`phase_2/`)** — a workflow that extracts planning steps from a high-level request, routes each step to a role-specific worker, evaluates the worker response, and assembles results into a project plan.

The workflow models three specialist roles: a Product Manager for user stories, a Program Manager for features, and a Development Engineer for engineering tasks. `phase_2/agentic_workflow.py` configures these roles and reads the Email Router product specification from `phase_2/Product-Spec-Email-Router.txt`.

## Repository Structure

```text
.
├── requirements.txt
├── phase_1/
│   ├── workflow_agents/
│   │   └── base_agents.py
│   ├── action_planning_agent.py
│   ├── augmented_prompt_agent.py
│   ├── direct_prompt_agent.py
│   ├── evaluation_agent.py
│   ├── knowledge_augmented_prompt_agent.py
│   ├── rag_knowledge_prompt_agent.py
│   └── routing_agent.py
└── phase_2/
    ├── Product-Spec-Email-Router.txt
    ├── agentic_workflow.py
    ├── reflection.md
    ├── workflow_agents/
    │   └── base_agents.py
    └── test_artifacts/
```

The `base_agents.py` files are phase-specific copies of the agent library. Phase 2 imports its local copy, while the standalone agent examples in Phase 1 use the Phase 1 package.

## Agent Toolkit

The toolkit in `phase_1/workflow_agents/base_agents.py` includes:

- `DirectPromptAgent` for direct model prompting.
- `AugmentedPromptAgent` for persona-guided prompting.
- `KnowledgeAugmentedPromptAgent` for responses grounded in supplied knowledge.
- `RAGKnowledgePromptAgent` for retrieval-augmented responses.
- `EvaluationAgent` for checking and refining worker responses against criteria.
- `RoutingAgent` for embedding-based semantic selection among agents.
- `ActionPlanningAgent` for turning a high-level request into workflow steps.

The scripts at the top level of `phase_1/` demonstrate the toolkit’s agents individually.

## Workflow Behavior

The phase 2 workflow uses the Action Planning Agent to produce steps from a project request. The Routing Agent compares each short step with descriptions of the available specialist roles using text embeddings. The selected role’s worker agent produces a response, and its Evaluation Agent can request revisions against role-specific output criteria. The script records step results and errors, then assembles the completed results into labeled sections.

The current workflow is a working pilot. Its execution behavior and a proposed context accumulation improvement are summarized in [phase_2/reflection.md](phase_2/reflection.md).

## Environment Setup

Python 3.10 or later is suitable for this project. From the repository root, create and activate a virtual environment, then install the pinned dependencies.

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the repository root with an OpenAI API key. `python-dotenv` loads this value for the agent scripts.

```text
OPENAI_API_KEY=your_openai_api_key
```

## Running the Workflow

From the repository root, run:

```powershell
python phase_2/agentic_workflow.py
```

The same command works in macOS and Linux shells. A successful run prints the workflow trace and final plan. Timestamped trace and plan files are written to `phase_2/test_artifacts/`.

## Running Individual Agent Examples

Each Phase 1 script runs a standalone example of its corresponding agent. For example:

```powershell
python phase_1/direct_prompt_agent.py
python phase_1/routing_agent.py
python phase_1/action_planning_agent.py
```

The remaining examples are `augmented_prompt_agent.py`, `knowledge_augmented_prompt_agent.py`, `rag_knowledge_prompt_agent.py`, and `evaluation_agent.py`. These examples also require `OPENAI_API_KEY`.

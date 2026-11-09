# Phase 2: Project Planning Workflow

Phase 2 applies the agent toolkit to a technical project management scenario. The workflow in `agentic_workflow.py` reads the Email Router product specification, asks an Action Planning Agent to derive workflow steps, and uses embedding-based routing to assign each step to a Product Manager, Program Manager, or Development Engineer worker. Evaluation agents check and refine the resulting user stories, features, and engineering tasks.

## Contents

- `agentic_workflow.py` — workflow configuration, execution, error handling, and final plan assembly.
- `Product-Spec-Email-Router.txt` — the product specification used in the pilot.
- `workflow_agents/base_agents.py` — the Phase 2 copy of the agent toolkit.
- `test_artifacts/` — timestamped workflow traces and final plan outputs.
- `reflection.md` — observations about the workflow’s strengths, limitations, and a proposed improvement.

The workflow is run from the repository root as `python phase_2/agentic_workflow.py`. Environment setup and API key configuration are covered in the [main README](../README.md).

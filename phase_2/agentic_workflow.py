import os
import sys
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent   

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# load the product spec
product_spec_path = Path(__file__).with_name("Product-Spec-Email-Router.txt")
product_spec = product_spec_path.read_text(encoding="utf-8")

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)

action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge_action_planning,
)
# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    + product_spec
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager,
)
# Product Manager - Evaluation Agent
persona_product_manager_eval = "You are an evaluation agent that checks whether user stories follow the required format."
evaluation_criteria_product_manager = (
    "The answer should be stories that follow the following structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    agent_to_evaluate=product_manager_knowledge_agent,
    max_interactions=3,
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager,
)
# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_program_manager = (
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=evaluation_criteria_program_manager,
    agent_to_evaluate=program_manager_knowledge_agent, 
    max_interactions=3
)
# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer,
)
# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)

development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev_engineer,
    agent_to_evaluate=development_engineer_knowledge_agent,
    max_interactions=3
)

# Routing Agent
routing_agent = RoutingAgent(openai_api_key, {})
routing_agent.agents = [
    {
        "name": "Product Manager",
        "description": "Define user stories from the product specification, identifying user personas, actions, and desired outcomes.",
        "func": lambda query: product_manager_support_function(query),
    },
    {
        "name": "Program Manager",
        "description": "Group related user stories into cohesive product features and describe the value and functionality of each feature.",
        "func": lambda query: program_manager_support_function(query),
    },
    {
        "name": "Development Engineer",
        "description": "Break user stories into engineering development tasks with technical descriptions, acceptance criteria, estimates, and dependencies.",
        "func": lambda query: development_engineer_support_function(query),
    },
]

# Job function persona support functions
# NOTE: The query response from the respective Knowledge Augmented Prompt Agents is obtained within the evaluation agent's evaluate() method, which returns a dictionary containing the final response. You can access the final response using result["final_response"].
def product_manager_support_function(query):
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def program_manager_support_function(query):
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]


def development_engineer_support_function(query):
    result = development_engineer_evaluation_agent.evaluate(query)
    return result["final_response"]

# Run the workflow

class Tee:
    """Write workflow output to both the console and a text file."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for stream in self.streams:
            stream.write(text)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()


original_stdout = sys.stdout
loop_output_file = Path(__file__).with_name("workflow_loop_output.txt").open("w", encoding="utf-8")
sys.stdout = Tee(original_stdout, loop_output_file)

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "Produce a complete project plan for the Email Router product, including user stories, product features, and engineering tasks."
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")

extracted_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
completed_steps = []
completed_roles = []
for i, step in enumerate(extracted_steps):
    print(f"\nExecuting step {i}: {step}")
    result = routing_agent.route_prompt(step)
    completed_steps.append(result)
    completed_roles.append(routing_agent.last_agent_name)
    print(f"Result of step {i}: {result}")

section_roles = {
    "User Stories": "Product Manager",
    "Product Features": "Program Manager",
    "Engineering Tasks": "Development Engineer",
}
plan_output = StringIO()
sys.stdout = plan_output
print("\n*** Final Project Plan ***\n")
for section, role in section_roles.items():
    print(f"--- {section} ---")
    section_results = [
        result for result, producing_role in zip(completed_steps, completed_roles)
        if producing_role == role
    ]
    if section_results:
        for result in section_results:
            print(result)
    else:
        print("No results were routed to this section.")

sys.stdout = original_stdout
final_plan = plan_output.getvalue()
print(final_plan, end="")
Path(__file__).with_name("final_project_plan.txt").write_text(final_plan, encoding="utf-8")
loop_output_file.close()

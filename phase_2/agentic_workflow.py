import os
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

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "Produce a complete project plan for the Email Router product, including user stories, product features, and engineering tasks."
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, assemble the completed steps into a single consolidated project plan with
#      clearly labelled sections for user stories, product features, and engineering tasks, and
#      print that plan. Do not print only the last completed step.
#
# TODO: 13 - Implement the assembly step used by TODO 12 step 4.
#   Group the entries in 'completed_steps' by the role that produced them and print one plan, e.g.:
#
#       print("\n*** Consolidated Project Plan ***\n")
#       for section in ("User Stories", "Product Features", "Engineering Tasks"):
#           print(f"--- {section} ---")
#           # print the completed_steps belonging to this section
#
#   Keep the routing input separate from this assembly: route on the short step text only, and do
#   not feed accumulated context back into 'routing_agent.route()'.

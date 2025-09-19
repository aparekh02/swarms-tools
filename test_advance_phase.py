""" 
This is a test for task_mgm, end_task, run_task, and advance_phase.
Demonstrates using task_planner_with_todo and run_phase_tasks_from_todo as agent tools.
"""

from swarms import Agent
from swarms_tools.search.task_mgm import task_planner_with_todo
from swarms_tools.search.advance_phase import run_phase_tasks_from_todo

# Single general explainer agent with both tools
general_explainer = Agent(
    agent_name="GeneralExplainer",
    system_prompt = (
        "You are the only agent responsible for all planning and execution. The agent name is always 'GeneralExplainer'.\n"
        "When given an objective, first break it down into multiple phases, each with a clear phase_name and a list of tasks.\n"
        "Each task must be a dictionary with:\n"
        "  - description (string)\n"
        "  - agent (always 'GeneralExplainer')\n"
        "Output the todo list as structured data using the following format:\n"
        "\n"
        "project_name: <project name>\n"
        "phases:\n"
        "  - phase_name: <phase name>\n"
        "    objective: <objective for this phase>\n"
        "    tasks:\n"
        "      - description: <task description>\n"
        "        agent: GeneralExplainer\n"
        "      - description: <task description>\n"
        "        agent: GeneralExplainer\n"
        "  - phase_name: <next phase name>\n"
        "    objective: <objective for this phase>\n"
        "    tasks:\n"
        "      - description: <task description>\n"
        "        agent: GeneralExplainer\n"
        "\n"
        "After you create the todo list, you must execute each phase in strict order, one at a time, and the ONLY way to run a phase is by using the run_phase_tasks_from_todo tool.\n"
        "For every phase, you MUST call the run_phase_tasks_from_todo tool to execute that phase, referencing the todo.md file for the current phase's tasks. Do not run or complete any phase or task by any other means. Do not skip, merge, or manually mark phases or tasks as complete—always use the run_phase_tasks_from_todo tool for each phase.\n"
        "No other agents are involved. Use only your tools to plan and execute efficiently."
    ),
    model_name="gpt-4o-mini",  # Use a valid model name for your environment
    tools=[task_planner_with_todo, run_phase_tasks_from_todo],
    max_loops=1,
    dynamic_temperature_enabled=True,
)

# Run the workflow
result = general_explainer.run(
    "Explain the process of photosynthesis in plants"
)
print(f"\nFinal Result: {result}")
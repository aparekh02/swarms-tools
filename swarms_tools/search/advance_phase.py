"""
Makes sure that all tasks are marked with a [X] (or completed) AND begins running next task of next phase.

This version is for single-agent only. The agent parameter is required and all tasks are run with this agent.
"""

import os
import re
from typing import Any

from swarms_tools.search.run_task import run_task_without_timeout
from swarms_tools.search.end_task import end_task

def run_phase_tasks_from_todo(
    todo_md_path: str,
    phase_name: str,
    agent: Any,
) -> str:
    """
    Runs all incomplete tasks in the specified phase from the todo.md file, marking each as completed after execution.

    This function is for single-agent mode only. All tasks are run with the provided `agent` argument.

    Args:
        todo_md_path: Full path to the todo.md file.
        phase_name: Name of the phase to run tasks for.
        agent (Any): The agent object to use for all tasks.

    Returns:
        String stating what tasks have been run.
    """

    def extract_task_description_from_line(line: str):
        """
        Extracts the task description from a todo.md task line.
        Returns task_description (str)
        """
        desc_match = re.match(
            r"\[\s?\]\s*(.*?)(?:\s+##ID:.*?##)?(?:\s+##AGENT:.*?##)?$",
            line.strip()
        )
        task_description = desc_match.group(1).strip() if desc_match else line.strip()
        return task_description

    if not os.path.exists(todo_md_path):
        raise FileNotFoundError(f"todo.md not found at {todo_md_path}")

    with open(todo_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    phase_header = f"## {phase_name}"
    phase_start = None
    phase_end = None
    for idx, line in enumerate(lines):
        if line.strip() == phase_header:
            phase_start = idx
            break
    if phase_start is None:
        raise ValueError(f"Phase '{phase_name}' not found in todo.md")

    for idx in range(phase_start + 1, len(lines)):
        if lines[idx].strip().startswith("## ") and idx > phase_start:
            phase_end = idx
            break
    if phase_end is None:
        phase_end = len(lines)

    task_line_tuples = []
    for i in range(phase_start + 1, phase_end):
        line = lines[i]
        if re.match(r"\[\s?\]|\[X\]", line.strip()):
            task_line_tuples.append((i, line.rstrip("\n")))

    if not task_line_tuples:
        raise ValueError(f"No tasks found for phase '{phase_name}'")

    run_task_descriptions = []

    if agent is None:
        raise ValueError("No agent provided for single-agent mode.")

    for line_number, task_line in task_line_tuples:
        if re.match(r"\[\s\]", task_line.strip()):
            task_description = extract_task_description_from_line(task_line)
            print(f"Running task on line {line_number+1}: '{task_description}' with single agent.")

            result = run_task_without_timeout(
                agent=agent,
                task_description=task_description
            )

            print(f"\n--- Result for task '{task_description}' ---")
            print(result)

            run_task_descriptions.append(
                f"Task: '{task_description}' - completed.\nResult:\n{result}"
            )

            end_task(line_number)

    if not run_task_descriptions:
        return f"No incomplete tasks found for phase '{phase_name}'."
    else:
        return (
            f"Tasks run for phase '{phase_name}':\n\n" +
            "\n\n".join(run_task_descriptions)
        )

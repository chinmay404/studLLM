import yaml
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from config.get_llm import LLM

llm = LLM.get_groq_llm()

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)  # Load YAML as a dictionary

@CrewBase
class Studllm():
    """Studllm crew"""

    agents_config = load_yaml('config/agents.yaml')  # Load YAML as dict
    tasks_config = load_yaml('config/tasks.yaml')  # Load tasks YAML

    @agent
    def researcher(self) -> Agent:
        if "communication" not in self.agents_config:
            raise KeyError("Key 'communication' not found in agents.yaml")
        
        return Agent(
            config=self.agents_config['communication'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        if "communication" not in self.tasks_config:
            raise KeyError("Key 'communication' not found in tasks.yaml")
        
        return Task(
            config=self.tasks_config['communication'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Studllm crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory=True,
            llm=llm,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "0"},
            }
        )

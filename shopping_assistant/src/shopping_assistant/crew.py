from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ShoppingAssistant():
    """Shopping Assistant Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def product_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['product_scraper'],
            verbose=True
        )

    @agent
    def price_comparator(self) -> Agent:
        return Agent(
            config=self.agents_config['price_comparator'],
            verbose=True
        )

    @agent
    def notifier(self) -> Agent:
        return Agent(
            config=self.agents_config['notifier'],
            verbose=True
        )

    @task
    def scrape_task(self) -> Task:
        return Task(config=self.tasks_config['scrape_task'])

    @task
    def compare_task(self) -> Task:
        return Task(config=self.tasks_config['compare_task'])

    @task
    def notify_task(self) -> Task:
        return Task(config=self.tasks_config['notify_task'])

    @crew
    def crew(self) -> Crew:
        """Creates the Shopping Assistant Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class ShoppingAssistant():
    """Shopping Assistant Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # 🔹 Modify search tool to include ALL e-commerce websites
    serper_search = SerperDevTool()
    scraper_tool = ScrapeWebsiteTool()

    @agent
    def product_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['product_scraper'],
            tools=[self.serper_search, self.scraper_tool],  # ✅ Search all e-commerce sites
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
        return Task(
            config=self.tasks_config['scrape_task'],
            input_formatter=self.modify_search_query  # ✅ Fixes search query dynamically
        )

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

    def modify_search_query(self, inputs):
        """🔹 Ensures search query includes ALL e-commerce sites dynamically"""
        product_name = inputs["product_name"]
        search_query = (
            f"{product_name} price site:amazon.com OR "
            f"site:flipkart.com OR site:walmart.com OR site:bestbuy.com OR site:ebay.com"
        )
        print(f"🔍 Modified Search Query: {search_query}")  # ✅ Debugging
        return {"search_query": search_query}

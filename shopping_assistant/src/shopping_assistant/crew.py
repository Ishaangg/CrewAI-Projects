import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class ShoppingAssistant():
    """
    Shopping Assistant Crew
    """

    # Paths to YAML configs
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Tools
    serper_search = SerperDevTool()
    scraper_tool = ScrapeWebsiteTool()

    @agent
    def product_scraper(self) -> Agent:
        """
        Agent to handle searching and scraping product data from multiple e-commerce sites.
        """
        return Agent(
            config=self.agents_config['product_scraper'],
            tools=[self.serper_search, self.scraper_tool],
            verbose=True
        )

    @agent
    def price_comparator(self) -> Agent:
        """
        Agent to compare/finalize product based on user-specified decision criterion.
        """
        return Agent(
            config=self.agents_config['price_comparator'],
            verbose=True
        )

    @agent
    def notifier(self) -> Agent:
        """
        Agent to send notifications/alerts once the best option is found.
        """
        return Agent(
            config=self.agents_config['notifier'],
            verbose=True
        )

    @task
    def scrape_task(self) -> Task:
        """
        Task that searches for the product on multiple e-commerce sites and returns
        a JSON with all found prices or other relevant info.
        """
        return Task(
            config=self.tasks_config['scrape_task'],
            input_formatter=self.modify_search_query
        )

    @task
    def compare_task(self) -> Task:
        """
        Task that uses the 'decision_criterion' to pick the best product from the scraped data.
        """
        return Task(config=self.tasks_config['compare_task'])

    @task
    def notify_task(self) -> Task:
        """
        Task that notifies the user once the best product is identified.
        """
        return Task(config=self.tasks_config['notify_task'])

    @crew
    def crew(self) -> Crew:
        """
        Creates and returns the Shopping Assistant Crew,
        executing tasks in a sequential pipeline.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def modify_search_query(self, inputs):
        """
        Ensures search query includes multiple e-commerce sites and
        carries forward user’s decision criterion.
        """
        product_name = inputs["product_name"]
        # We carry forward the user criterion if given, otherwise default to 'cost'
        decision_criterion = inputs.get("decision_criterion", "cost")

        # Dynamically assemble a search query
        search_query = (
            f"{product_name} price site:amazon.com OR "
            f"site:flipkart.com OR site:walmart.com OR site:bestbuy.com OR site:ebay.com"
        )
        print(f"🔍 Modified Search Query: {search_query}")  # Debugging

        # Return a dictionary with everything needed in subsequent tasks
        return {
            "search_query": search_query,
            "product_name": product_name,
            "decision_criterion": decision_criterion
        }

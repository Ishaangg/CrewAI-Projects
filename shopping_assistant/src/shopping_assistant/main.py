#!/usr/bin/env python
import sys
import warnings
from crew import ShoppingAssistant  # Assumes 'crew.py' or 'main.py' is exposed as a module named `crew`
import os
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
import agentops
from dotenv import load_dotenv
load_dotenv()
def run():
    """
    Run the shopping assistant crew.
    """
    session = agentops.init(api_key=os.getenv('AGENTOPS_API_KEY'))
    # Example input that now includes a 'decision_criterion' parameter
    inputs = {
        'product_name': 'T-Shirt',
        'decision_criterion': 'rating'  
        # Could be 'cost', 'rating', 'shipping_speed', 'brand_reputation', etc.
    }

    # Kick off the process
    ShoppingAssistant().crew().kickoff(inputs=inputs)
    session.end_session()

if __name__ == "__main__":
    run()

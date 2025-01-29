#!/usr/bin/env python
import sys
import warnings
from shopping_assistant.crew import ShoppingAssistant

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the shopping assistant crew."""
    inputs = {
        'product_name': 'iPhone 15 Pro'
    }
    ShoppingAssistant().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

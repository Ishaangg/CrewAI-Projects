#!/usr/bin/env python
import sys
import warnings
from crew import ShoppingAssistant
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Run the shopping assistant crew."""
    inputs = {
        'product_name': 'Air fryer'
    }
    ShoppingAssistant().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

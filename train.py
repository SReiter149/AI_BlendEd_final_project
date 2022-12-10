"""
run this file to train the agent
nothing interesting here, just a sample of how one could use all the files created
"""

from agent import agent
from pong import game

pong = game()
agent = agent(pong)
agent.main()
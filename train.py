from agent import agent
from pong import game

pong = game()
agent = agent(pong)
agent.main()
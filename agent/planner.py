
from abc import ABC, abstractmethod

from agent.state import AgentAction, AgentState


class Planner(ABC):

    @abstractmethod
    def plan(self, state: AgentState) -> AgentAction:
        pass


from agent.state import (
    AgentState,
    AgentStatus,
    ActionType,
    AgentAction,
    ToolResult
)


def test_agent_initial_state():
    state = AgentState(task="Calculate 10 + 20")

    assert state.status == AgentStatus.IDLE
    assert state.step_count == 0
    assert state.max_steps == 10
    assert state.history == []


def test_agent_actions():
    action = AgentAction(
        action_type=ActionType.CALL_TOOL,
        tool_name="calculator",
        arguments={"a": 10, "b": 20}
    )

    assert action.action_type == ActionType.CALL_TOOL
    assert action.tool_name == "calculator"


def test_tool_result():
    result = ToolResult(
        success=True,
        output=30
    )

    assert result.success is True
    assert result.output == 30


def test_agent_states_are_independent():
    first = AgentState(task="Task one")
    second = AgentState(task="Task two")

    first.history.append({"event": "started"})

    assert len(first.history) == 1
    assert len(second.history) == 0

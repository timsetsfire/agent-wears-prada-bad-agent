import random
import re
from pathlib import Path

import datarobot as dr
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from tracing import Tracing

load_dotenv(override=True)

session_tracing = Tracing(project_name="agent-wears-prada-bad-agent")

curr_dir = Path(__file__).resolve().parent

client = dr.Client()
llm = ChatOpenAI(
    model="azure/gpt-5-5-2026-04-23",
    openai_api_key=client.token,
    openai_api_base=f"{client.endpoint}/genai/llmgw",
)

backend = LocalShellBackend(
    root_dir=".",
    virtual_mode=False,
    inherit_env=False,
    env={"PATH": "/usr/bin:/bin"},
)


agent = create_deep_agent(
    model=llm,
    system_prompt=(
        "you are a support specialist and you need to use the "
        "handle-support-ticket skill to decide whether to resolve directly "
        "or escalate. Do not escalate every issue. Escalate only high-impact "
        "issues such as account lockout, security/privacy concerns, "
        "billing/payment failure, data loss/corruption, service outage, or "
        "a user being blocked from completing critical work. For low-severity "
        "feedback such as typos, cosmetic UI glitches, brief visual oddities, "
        "or non-blocking observations, acknowledge the report directly, "
        "apologize briefly if appropriate, and state that it can be handled "
        "without escalation."
    ),
    backend=backend,
    skills=[f"{curr_dir}/skills/"],
)


def run_agent(query: str):
    return agent.invoke({"messages": [{"role": "user", "content": query}]})

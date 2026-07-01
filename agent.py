import random
import re
from pathlib import Path

import datarobot as dr
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

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
        "you are a support specialist and you need to use the handle-support-ticket skill to decide whether to resolve directly or escalate."
    ),
    backend=backend,
    skills=[f"{curr_dir}/skills/"],
)


def run_agent(query: str):
    return agent.invoke({"messages": [{"role": "user", "content": query}]})
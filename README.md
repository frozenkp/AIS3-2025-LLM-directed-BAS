# AIS3 2025: LLM-Directed BAS PoC

This is a Proof-of-Concept (PoC) for a BAS (Breach and Attack Simulation) system directed by a Large Language Model (LLM). It allows natural language attack descriptions to be executed via a local command execution server using [NirCmd](https://www.nirsoft.net/utils/nircmd.html).

## Requirements

### OpenAI API Key

Set your OpenAI API key and base URL as environment variables. You can refer to `example_key.env` for a sample configuration.

```bash
export OPENAI_API_KEY='YOUR_KEY_HERE'
export OPENAI_API_BASE='https://api.openai.com/v1'
```

### NirCmd

Download `NirCmd.exe` from [NirSoft](https://www.nirsoft.net/utils/nircmd.html) and place it in the same directory as `agent.py`.

By default, the script assumes `NirCmd.exe` is located at `.\NirCmd.exe`. You can modify this path in `agent.py` if needed.

## Getting Started

### Agent (MCP Server)

`agent.py` acts as a simple MCP server that receives and executes commands using NirCmd. It should be deployed in the test environment where NirCmd is available.

Run the agent with:

```python
python agent.py
```

### Client

`main.py` is the client responsible for sending attack instructions in natural language to the MCP server (`agent.py`).

Example:
```python
python main.py '192.168.0.1:8000' 'Set test.exe on my desktop to be a startup program' --log 'log/test.log'
```

In this example:
	•	`192.168.0.1:8000` is the address and port of the MCP server.
	•	The second argument is a natural language instruction for the attack.
	•	`--log` specifies the log file path.

⸻

This project is developed as part of the AIS3 2025 event for experimental and research purposes only.
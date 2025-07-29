from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_tools(mcp_config):
    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()

    return tools

"""
Example mcp_config:

mcp_config = {
    'interactive powershell': {
        'url': 'http://100.89.224.111:8000/sse',
        'transport': 'sse',
    },
    'thought': {
        'command': 'python',
        'args': ['./think_tool.py'],
        'transport': 'stdio',
    },
}
"""

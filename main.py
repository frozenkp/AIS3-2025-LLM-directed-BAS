import asyncio
from LLMBAS import LLMBAS
import logger
import argparse

async def main():
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('mcp', help='Address and port for the MCP server.')
    parser.add_argument('attack', help='Attack description.')
    parser.add_argument('--log', help='Path to the log file.', default=None)
    args = parser.parse_args()
    
    # MCP configuration
    mcp_config = {
        'mcp_tools': {
            'url': f'http://{args.mcp}/sse',
            'transport': 'sse',
        },
    }

    # prepare LLMBAS client
    llmbas = await LLMBAS.new(mcp_config, log_file=args.log, log_level=logger.DEBUG)

    # run
    result = await llmbas.run(args.attack)

if __name__ == '__main__':
    asyncio.run(main())

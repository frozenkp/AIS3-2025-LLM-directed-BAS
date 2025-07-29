from LLM import LLM
import logger
import MCP
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.tool import ToolMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

class LLMBAS():
    class AgentState(TypedDict):
        messages:       Annotated[List[BaseMessage], add_messages]
        attack:         str

    def __init__(self, llm, tools, logger):
        self.LLM = llm
        self.logger = logger
        self.tools = tools
        self.tool_node = ToolNode(self.tools)

        # prepare graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()

    # for bypassing the aysnc init function
    @classmethod
    async def new(cls, mcp_config, provider='openai', model='gpt-4o', log_file=None, log_level=logger.INFO):
        # logger
        bas_logger = logger.Logger('LLMBAS', log_file=log_file, level=log_level)

        # llm
        llm = LLM(provider, model, logger_config={'name': 'LLMBAS.LLM'})

        # tools
        tools = await MCP.get_tools(mcp_config)

        return cls(llm, tools, bas_logger)

    # _build_graph builds the langgraph workflow
    def _build_graph(self):
        # define the worflow with a custom agent state
        workflow = StateGraph(self.AgentState)

        # define node
        workflow.add_node('agent_node', self._agent_node)
        workflow.add_node('tool_node', self.tool_node)
   
        # set entry node
        workflow.set_entry_point('agent_node')
        
        # define edge
        workflow.add_edge('agent_node', 'tool_node')
        workflow.add_edge('tool_node', END)

        return workflow 

    # _agent_node provides attack description and tool information to ask LLM to perform attack.
    def _agent_node(self, state: AgentState) -> AgentState:
        # input
        attack = state['attack']

        # read prompt template
        with open('tmpl/agent.tmpl', 'r') as fp:
            prompt_tmpl = fp.read()

        # craft prompt
        prompt = prompt_tmpl.format(attack=attack)

        # craft messages
        messages = [HumanMessage(content=prompt)]

        # prepare model
        client = self.LLM.client(tools=self.tools)

        # invoke
        response = client.invoke(messages)

        return {'messages': [HumanMessage(content=prompt), response]}

    # _log_node_output logs the update in each node
    def _log_node_output(self, node_name, node_output):
        if 'messages' in node_output:
            messages = node_output['messages']
            
            for message in messages:
                match message:
                    case AIMessage():
                        self.logger.module('AMSG').info(logger.Msg('AI Message', message.content, 'blue'))
                        if hasattr(message, 'tool_calls') and message.tool_calls:
                            for call in message.tool_calls:
                                self.logger.module('AMSG').info(logger.Msg('Tool Call Name', call['name'], 'cyan'))
                                self.logger.module('AMSG').info(logger.Msg('Tool Call Args', call['args'], 'cyan'))

                    case ToolMessage():
                        self.logger.module('TMSG').info(logger.Msg('Tool Response Name', message.name, 'cyan'))
                        self.logger.module('TMSG').info(logger.Msg('Tool Response Message', message.content, 'cyan'))

                    case HumanMessage():
                        self.logger.module('HMSG').debug(logger.Msg('Human Message', message.content, 'blue'))

                    case _:
                        self.logger.module('NODE').warning(logger.Msg('Unhandled Message', message, 'blue'))

    # run 
    async def run(self, attack: str):
        # prepare initial state
        initial_state = {
            'messages':     [],
            'attack':       attack,
        }
        
        # run with output log
        async for mode, output in self.app.astream(initial_state, stream_mode=['updates']):
            match mode:
                case 'updates':
                    for node_name, node_output in output.items():
                        self._log_node_output(node_name, node_output)

                case _:
                    self.logger.module('RUN').warning(f'Unhandled mode: {mode}')
    
        return 

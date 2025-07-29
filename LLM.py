import logger
import sys
from langchain_openai import ChatOpenAI

class LLM():
    def __init__(self, provider='openai', model='gpt-4o', logger_config={'name': 'LLM'}):
        self.provider = provider
        self.model = model

        # prepare logger
        self.logger = logger.Logger(**logger_config)

    def client(self, model=None, schema=None, tools=None):
        model = self.model if not model else model

        # prepare model
        if self.provider.strip().lower() == 'openai':
            self.logger.module('CLIENT').info(f'Prepare {model} model from {self.provider}')
            client = ChatOpenAI(model=model)
        else:
            self.logger.module('CLIENT').error(f'Unsupported provider {self.provider}')
            raise ValueError('Unsupported provider {self.provider}')

        # check tools and schema
        if schema is not None and tools is not None:
            self.logger.module('CLIENT').error('Schema and tools should not be included at the same time')
            raise ValueError('Schema and tools should not be included at the same time')
        
        if schema:
            # bind the response schema to the model
            self.logger.module('CLIENT').info('Bind the schema to the model')
            client = client.with_structured_output(schema)
        elif tools:
            # bind the tools to the model
            self.logger.module('CLIENT').info('Bind the tools to the model')
            client = client.bind_tools(tools)

        return _model(client, self.logger)

class _model():
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def invoke(self, *args, **kargs):
        try:
            self.logger.module('INVOKE').info('Invoke')
            result = self.client.invoke(*args, **kargs)

        except KeyboardInterrupt:
            self.logger.module('INVOKE').warning('KeyboardInterrupt')
            pass

        except Exception as e:
            self.logger.module('INVOKE').error(f'Catch exception: {e}')
            self.logger.module('INVOKE').info('Invoke again...')
            result = self.invoke(*args, **kargs)

        return result

    async def ainvoke(self, *args, **kargs):
        try:
            self.logger.module('AINVOKE').info('AInvoke')
            result = await self.client.ainvoke(*args, **kargs)

        except KeyboardInterrupt:
            self.logger.module('AINVOKE').warning('KeyboardInterrupt')
            pass

        except Exception as e:
            self.logger.module('AINVOKE').error(f'Catch exception: {e}')
            self.logger.module('AINVOKE').info('Invoke again...')
            result = await self.ainvoke(*args, **kargs)

        return result

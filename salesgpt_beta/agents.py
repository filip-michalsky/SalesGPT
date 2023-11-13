import os, time, json
from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from copy import deepcopy
from typing import Any, Callable, Dict, List, Union
from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from pydantic import Field
from salesgpt_beta.logger import time_logger, logger
from salesgpt_beta.daos import ChatDao, CustomerDao, ProductDao
from salesgpt_beta.prompts import SALES_AGENT_PROMPT
from salesgpt_beta.stages import StagesManager
from salesgpt_beta.tools import get_tools_list, find_tool_by_name


class SalesGPT(Chain):
    chatDao: ChatDao = Field(...)
    customerDao: CustomerDao = Field(...)
    llm: OpenAI = Field(...)

    salesperson_name: str = "Ted Lasso"
    salesperson_role: str = "Business Development Representative"
    company_name: str = "Sleep Haven"
    company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers."
    company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service."
    conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress."
    conversation_type: str = "call"
    product_files = []

    assistant: Assistant = Field(...)
    thread: Thread = Field(...)

    @time_logger
    def seed_agent(self):
        customer = self.customerDao.load()
        if customer is None:
            prompt_template = PromptTemplate.from_template(SALES_AGENT_PROMPT)
            prompt = prompt_template.format(
                salesperson_name=self.salesperson_name,
                salesperson_role=self.salesperson_role,
                company_name=self.company_name,
                company_business=self.company_business,
                company_values=self.company_values,
                conversation_purpose=self.conversation_purpose,
                conversation_type=self.conversation_type,
                customer_name=self.customerDao.get_name(),
                conversation_stages=StagesManager.get_stages_as_string()
            )
            logger.info(f'generated prompt: {prompt}')
            self.assistant = self.llm.beta.assistants.create(
                name=self.salesperson_name,
                instructions=prompt,
                model="gpt-4-1106-preview",
                tools=[{"type": "code_interpreter"}, {"type": "retrieval"}] + get_tools_list(),
                file_ids=self.product_files
            )
            self.thread = self.llm.beta.threads.create()
            self.customerDao.save(assistant_id=self.assistant.id, thread_id=self.thread.id)
        else:
            self.assistant = self.llm.beta.assistants.retrieve(assistant_id=customer.assistant_id)
            self.thread = self.llm.beta.threads.retrieve(thread_id=customer.thread_id)
        self.chatDao = ChatDao(salesperson_name=self.salesperson_name, customer_name=self.customerDao.get_name())

    @time_logger
    def step(self, stream: bool = False) -> str:
        """
        Args:
            stream (bool): whether to return
            streaming generator object to manipulate streaming chunks in downstream applications.
        """
        if not stream:
            return self._call(inputs={})['output']
        else:
            raise NotImplementedError('NotImplementedError')

    @time_logger
    def human_step(self, human_input):
        # process human input
        self.llm.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=human_input
        )
        self.chatDao.append(name=self.customerDao.get_name(), content=human_input)

    @property
    def input_keys(self) -> List[str]:
        return []

    @property
    def output_keys(self) -> List[str]:
        return []

    @time_logger
    def acall(self, *args, **kwargs):
        raise NotImplementedError("This method has not been implemented yet.")

    @time_logger
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run one step of the sales agent."""
        run = self.llm.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        while run.status != 'completed':
            run = self.llm.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=self.thread.id
            )
            if run.status == 'requires_action':
                self.use_tools(run)
            else:
                logger.info(f'run id: {run.id}, run status: {run.status}')
                time.sleep(6)
        messages = self.llm.beta.threads.messages.list(
            thread_id=self.thread.id,
            order='desc',
            limit=1
        )
        msg = ''
        for message in messages:
            msg = message.content[0].text.value
            self.chatDao.append(name=self.salesperson_name, content=msg)
            msg.replace("<END_OF_TURN>", "")
            break
        return {'output': msg}

    @time_logger
    def use_tools(self, run: Run):
        logger.info(f'run id: {run.id} starts to use tools')
        tool_call_resp = []
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool_call.function.name
            function_to_call = find_tool_by_name(function_name)
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            tool_call_resp.append((tool_call.id, function_response))
        logger.info(f'run id: {run.id} finished using tools: {tool_call_resp}')
        run = self.llm.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=run.id,
            tool_outputs=[{"tool_call_id": call_id, "output": call_resp} for call_id, call_resp in tool_call_resp]
        )
        while run.status != 'completed':
            run = self.llm.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=self.thread.id
            )
            logger.info(f'run id: {run.id}, run status: {run.status}')
            time.sleep(3)

    @classmethod
    @time_logger
    def from_llm(cls, llm: OpenAI, customer_name: str, customer_phone: str,
                 salesperson_name: str, product_catalog: str,
                 verbose: bool = False, **kwargs) -> "SalesGPT":
        customerDao = CustomerDao(name=customer_name, phone=customer_phone)
        file_ref = None
        product_files = []

        if os.path.isfile(product_catalog):
            product_files.append(product_catalog)
            file_ref = product_catalog
        elif os.path.isdir(product_catalog):
            files = os.listdir(product_catalog)
            product_files = [os.sep.join([product_catalog, f]) for f in files]
            file_ref = product_catalog.split(os.sep)[-1]

        existed_file_map = {}
        if file_ref is not None:
            productDao = ProductDao(name=file_ref)
            products = productDao.load()

            if products is not None:
                existed_file_map = json.loads(str(products.desc))

            for pf in product_files:
                if existed_file_map.get(pf, None) is None:
                    file = llm.files.create(
                        file=open(pf, 'rb'),
                        purpose='assistants'
                    )
                    existed_file_map[pf] = file.id
                    logger.info(f'{pf} finished uploading: {file.id}')
            productDao.save(desc=json.dumps(existed_file_map, ensure_ascii=False))

        return cls(
            llm=llm,
            salesperson_name=salesperson_name,
            customerDao=customerDao,
            product_files=list(existed_file_map.values()),
            verbose=verbose,
            **kwargs,
        )

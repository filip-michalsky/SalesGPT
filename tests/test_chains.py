import os
from salesgpt.chains import StageAnalyzerChain
from langchain.chat_models import ChatLiteLLM
from salesgpt.prompts import STAGE_ANALYZER_INCEPTION_PROMPT_V2
from salesgpt.stages import CONVERSATION_STAGES
from salesgpt.chats import SalesChat

from langchain.prompts.prompt import PromptTemplate


class TestChains:
    def test_stage_analyzer_chain(self, load_env):
        salesperson_name = 'Ted Lasso'
        customer_name = 'Alice Yu'
        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)

        llm = ChatLiteLLM(temperature=0)

        stage_analyzer_chain = StageAnalyzerChain.from_llm(llm=llm, verbose=True)

        next_stage = stage_analyzer_chain.run(
            conversation_history="\n".join(sales_chat.query_last_history()).rstrip("\n"),
            conversation_stage_id=1,
            conversation_stages="\n".join(
                [
                    str(key) + ": " + str(value)
                    for key, value in CONVERSATION_STAGES.items()
                ]
            ),
        )

        print(f'next_stage={next_stage}')

        assert next_stage is not None, "Agent output cannot be None."

    def test_stage_analyzer_chain_with_multiple_steps(self, load_env):

        salesperson_name = 'Ted Lasso'
        customer_name = 'Alice Yu'
        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)
        chat_msgs = sales_chat.query_history(chat_id='de8afffa0d554d05ac14b608535f8b8e')

        llm = ChatLiteLLM(temperature=0)
        stage_analyzer_chain = StageAnalyzerChain.from_llm(
            llm=llm, custom_template=STAGE_ANALYZER_INCEPTION_PROMPT_V2, verbose=False)
        chat_step = 6
        next_stage = 1
        print('\n'.join(chat_msgs))
        for i in range(0, len(chat_msgs), chat_step):
            next_stage = stage_analyzer_chain.run(
                conversation_history="\n".join(chat_msgs[i: i+chat_step]).rstrip("\n"),
                conversation_stage_id=next_stage,
                conversation_stages="\n".join(
                    [
                        str(key) + ": " + str(value)
                        for key, value in CONVERSATION_STAGES.items()
                    ]
                ),
            )
            print(f'next_stage = {next_stage}')





import os
from salesgpt.chains import StageAnalyzerChain
from langchain.chat_models import ChatLiteLLM
from salesgpt.stages import CONVERSATION_STAGES
from salesgpt.chats import SalesChat


class TestChains:
    def test_stage_analyzer_chain(self, load_env):

        salesperson_name = 'Ted Lasso'
        customer_name = 'Alice Yu'
        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)

        llm = ChatLiteLLM(temperature=0)

        stage_analyzer_chain = StageAnalyzerChain.from_llm(llm, verbose=True)

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





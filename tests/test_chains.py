import os
from salesgpt.chains import StageAnalyzerChain
from langchain.chat_models import ChatLiteLLM
from salesgpt.stages import StagesManager
from salesgpt.chats import SalesChat


class TestChains:
    def test_stage_analyzer_chain(self, load_env):
        salesperson_name = 'Ted Lasso'
        customer_name = 'Alice Yu'
        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)

        llm = ChatLiteLLM(temperature=0)

        stage_analyzer_chain = StageAnalyzerChain.from_llm(llm=llm, use_snippets=False, verbose=True)

        next_stage = stage_analyzer_chain.run(
            conversation_history="\n".join(sales_chat.query_last_history()).rstrip("\n"),
            conversation_stage_id=1,
            conversation_stages=StagesManager.get_stages_as_string(),
        )

        print(f'next_stage={next_stage}')

        assert next_stage is not None, "Agent output cannot be None."

    def test_stage_analyzer_chain_with_snippets(self, load_env):

        salesperson_name = 'Ted Lasso'
        customer_name = 'Alice Yu'
        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)
        # chat_msgs = sales_chat.query_history(chat_id='3c6722a74d2a420f96658963a9f11512')
        chat_msgs = sales_chat.query_history(chat_id='fe2bfac0b89b42f78a6bbca7c356c840')

        llm = ChatLiteLLM(temperature=0)
        stage_analyzer_chain = StageAnalyzerChain.from_llm(llm=llm, verbose=True)
        analyze_batch_step = 2
        next_stage = 1
        stages = [str(next_stage)]
        for i in range(0, len(chat_msgs), analyze_batch_step):
            cur_history = "\n".join(chat_msgs[i: i+analyze_batch_step]).rstrip("\n")
            next_stage = stage_analyzer_chain.run(
                conversation_history=cur_history,
                conversation_stage_id=next_stage,
                conversation_stages=StagesManager.get_stages_as_string(),
            )
            stages.append(str(next_stage))
        stages_route = '->'.join(stages)
        print(f'stages_route = {stages_route}')





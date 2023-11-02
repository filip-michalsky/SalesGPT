from salesgpt.chats import SalesChat


class TestDatabase:

    def test_chats(self, load_env):

        salesperson_name = 'bob'
        customer_name = 'alice'

        sales_chat = SalesChat(salesperson_name=salesperson_name, customer_name=customer_name)
        sales_chat.append(name=salesperson_name, content='hello, alice')
        sales_chat.append(name=customer_name, content='hello, bob')
        sales_chat.append(name=salesperson_name, content='by, alice')
        sales_chat.append(name=customer_name, content='bye, bob <END_OF_CALL>')

        assert(sales_chat.is_live_ended(), "chat is ended")

        chat_id = sales_chat.get_live_chat_id()
        history = sales_chat.query_history(chat_id=chat_id)
        print(history)
        assert history is not None, "Agent output cannot be None."

        last_history = sales_chat.query_last_history()
        print(last_history)
        assert last_history is not None, "Agent output cannot be None."

        print(sales_chat.query_all_history())
        assert last_history is not None, "Agent output cannot be None."

        assert sales_chat.delete_all_history() is None, "Agent output cannot be None."

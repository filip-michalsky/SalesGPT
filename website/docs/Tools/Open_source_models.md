---
sidebar_position: 5

---

# Using Open Source Models

SalesGPT allows you to use open-source models instead of paid models like OpenAI's GPT. To do this, follow these steps:

1. **Change the GPT_MODEL Environment Variable:**
   Update the `GPT_MODEL` environment variable in your `.env` file to the desired open-source model. For example:
   ```
   GPT_MODEL=your_open_source_model
   ```

2. **Update the `_streaming_generator` Function:**
   If you are using an open-source model, you may need to add an `api_base` argument to the `_streaming_generator` function in the `agents.py` script. This argument should be set to the inference URL of the model. If the model is deployed locally, use a localhost URL; otherwise, use any other working URL depending on the deployment.

   Here is an example of how to modify the `_streaming_generator` function:
   ```python
   return self.sales_conversation_utterance_chain.llm.completion_with_retry(
       messages=messages,
       stop="<END_OF_TURN>",
       stream=True,
       model=self.model_name,
       api_base="your_inference_url"  # Add this line for open-source models
   )
   ```

By following these steps, you can configure SalesGPT to use an open-source model for generating responses.

For more information on possible model deployments, you can visit: [LiteLLM Providers Documentation](https://litellm.vercel.app/docs/providers)


import inspect
import json
import logging
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union, cast

import yaml
from langchain_core._api import deprecated
from langchain_core.load.dump import dumpd
from langchain_core.memory import BaseMemory
from langchain_core.outputs import RunInfo
import yaml
from langchain_core._api import deprecated
from langchain_core.load.dump import dumpd
from langchain_core.memory import BaseMemory
from langchain_core.outputs import RunInfo
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field,
    create_model,
    root_validator,
    validator,
)
from langchain_core.runnables import (
    RunnableConfig,
    RunnableSerializable,
    ensure_config,
    run_in_executor,
)

from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.manager import (
    AsyncCallbackManager,
    AsyncCallbackManagerForChainRun,
    CallbackManager,
    CallbackManagerForChainRun,
    Callbacks,
)
from langchain.schema import RUN_KEY

class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True

# Assuming the rest of the class definition is here...

def invoke(
    self,
    input: Dict[str, Any],
    config: Optional[RunnableConfig] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    intermediate_steps = []  # Initialize the list to capture intermediate steps

    config = ensure_config(config)
    callbacks = config.get("callbacks")
    tags = config.get("tags")
    metadata = config.get("metadata")
    run_name = config.get("run_name")
    include_run_info = kwargs.get("include_run_info", False)
    return_only_outputs = kwargs.get("return_only_outputs", False)

    inputs = self.prep_inputs(input)
    callback_manager = CallbackManager.configure(
        callbacks,
        self.callbacks,
        self.verbose,
        tags,
        self.tags,
        metadata,
        self.metadata,
    )
    new_arg_supported = inspect.signature(self._call).parameters.get("run_manager")
    run_manager = callback_manager.on_chain_start(
        dumpd(self),
        inputs,
        name=run_name,
    )

    # Capture the start of the chain as an intermediate step
    intermediate_steps.append({"event": "Chain Started", "details": "Inputs prepared"})

    try:
        outputs = (
            self._call(inputs, run_manager=run_manager)
            if new_arg_supported
            else self._call(inputs)
        )
        # Capture a successful call as an intermediate step
        intermediate_steps.append({"event": "Call Successful", "outputs": outputs})
    except BaseException as e:
        run_manager.on_chain_error(e)
        # Capture errors as intermediate steps
        intermediate_steps.append({"event": "Error", "error": str(e)})
        raise e
    finally:
        run_manager.on_chain_end(outputs)

    final_outputs: Dict[str, Any] = self.prep_outputs(
        inputs, outputs, return_only_outputs
    )
    if include_run_info:
        final_outputs["run_info"] = RunInfo(run_id=run_manager.run_id)

    # Include intermediate steps in the final outputs
    final_outputs["intermediate_steps"] = intermediate_steps

    return final_outputs

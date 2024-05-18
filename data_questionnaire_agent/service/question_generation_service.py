from typing import Optional, Iterator, List
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains.openai_functions import create_structured_output_chain
# from langchain.chains.openai_functions import create_structured_output_runnable as create_structured_output_chain

# from langchain.chains.openai_functions import create_structured_output_chain
# from langchain.chains import LLMChain
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chains.llm import LLMChain

from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import prompts
from data_questionnaire_agent.config import cfg



# from langchain_core.language_models import BaseLanguageModel
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.output_parsers.openai_functions import PydanticOutputFunctionsParser
# from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# from langchain_core.pydantic_v1 import BaseModel, Field


def prompt_factory_secondary_questions() -> ChatPromptTemplate:
    TODO: 'You are a British data integration and gouvernance expert that can ask questions about data integration and gouvernance to help a customer with data integration and gouvernance problems. You use British English.
    # 
    section = prompts["questionnaire"]["secondary"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "questions_answers",
            "answers",
            "questions_per_batch",
        ],
    )


def chain_factory_secondary_question() -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_secondary_questions(),
        verbose=cfg.verbose_llm,
    )


def prepare_secondary_question(
    questionnaire: Questionnaire,
    knowledge_base: str,
    questions_per_batch: int = cfg.questions_per_batch,
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "questions_answers": str(questionnaire),
        "answers": questionnaire.answers_str(),
        "questions_per_batch": questions_per_batch,
    }


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )
    from data_questionnaire_agent.test.provider.knowledge_base_provider import (
        provide_data_quality_ops,
    )
    from data_questionnaire_agent.log_init import logger
    # from langchain.callbacks import get_openai_callback
    
    from langchain_community.callbacks import get_openai_callback
    import asyncio

    questionnaire = create_questionnaire_2_questions()
    knowledge_base = provide_data_quality_ops()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    with get_openai_callback() as cb:
        chain = chain_factory_secondary_question()
        # XXX: this is a blocking call
        res: ResponseQuestions = asyncio.run(chain.run(input))
        logger.info("total cost: %s", cb)
    assert isinstance(res, ResponseQuestions)
    logger.info("response questions: %s", res)

from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Literal
from models import Classification,Response
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', convert_system_message_to_human=True)


class AttributesState(TypedDict):
    query: str
    category: str
    classification: list

def query_classification(state: AttributesState):
    query = state['query']

    # Output parser
    parser = PydanticOutputParser(pydantic_object=Classification)

    # Prompt template
    template = PromptTemplate(
        template=(
            "You are an expert in genetic variant interpretation.\n"
            "Based on the following query, classify the variant according to ACMG/AMP guidelines.\n\n"
            "Respond ONLY in the following format:\n"
            "{format_instructions}\n\n"
            "Query: {query}"
        ),
        input_variables=['query'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    # Chain together
    chain = template | model | parser

    # Run chain
    final_result = chain.invoke({'query': query})

    state['category'] = final_result.model_dump()['class_']
    # state['category']=final_result['class_']
    return state

def pathogenic_classification(state: AttributesState):
    query= state['query']
    parser = PydanticOutputParser(pydantic_object=Response)
    template = PromptTemplate(
        template = (
            "You are a Expert in Genetic variant interpretation. \n"
            "Based on the following query, classify the variant according to ACMG/AMP guidelines in the following creteria : PVS1 – Very Strong , PS1 – Strong , PS2 – Strong , PS3 – Strong , PS4 – Strong , PM1 – Moderate , PM2 – Moderate , PM3 – Moderate , PM4 – Moderate , PM5 – Moderate , PM6 – Moderate , PP1 – Supporting , PP2 – Supporting , PP3 – Supporting , PP4 – Supporting , PP5 – Supporting (Deprecated). and also give the reason.\n\n"
            "Respond ONLY in the following format:\n"
            "{format_instructions}\n\n"
            "Query: {query}"
        ),
        input_variables=['query'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )
    chain = template | model | parser

    # Run chain
    final_result = chain.invoke({'query': query})

    return {'classification':final_result.model_dump()['result']}

def benign_classification(state: AttributesState):
    query= state['query']
    parser = PydanticOutputParser(pydantic_object=Response)
    template = PromptTemplate(
        template = (
            "You are a Expert in Genetic variant interpretation. \n"
            "Based on the following query, classify the variant according to ACMG/AMP guidelines in the following creteria "
            "BA1 (Stand-alone) , BS1 (Strong) , BS2 (Strong) , BS3 (Strong) , BS4 (Strong) , \nBP1–BP7 (Supporting) \nBP1: Missense in a gene where only truncating variants cause disease."
            "\nBP2: Observed in trans with a pathogenic variant (dominant disorder).\nBP3: In-frame indels in non-conserved regions.\nBP4: Multiple tools predict benign.\nBP5: Variant found in individual with alternate cause of disease.\nBP6: Reputable source reports benign without supporting data.\nBP7: Synonymous variant with no predicted splicing effect.. and also give the reason.\n\n"
            "Respond ONLY in the following format:\n"
            "{format_instructions}\n\n"
            "Query: {query}"
        ),
        input_variables=['query'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )
    chain = template | model | parser

    # Run chain
    final_result = chain.invoke({'query': query})


    return {'classification':final_result.model_dump()['result']}

def not_valid_classification(state: AttributesState):
    return {'classification':[]}

def category_classification(state: AttributesState) -> Literal["pathogenic_classification", "benign_classification","not_valid_classification"]:
    if state['category'] == "Pathogenic":
        return 'pathogenic_classification'
    elif state['category'] == "Benign":
        return 'benign_classification'
    else:
        return 'not_valid_classification'

graph = StateGraph(AttributesState)

graph.add_node('query_classification',query_classification)
graph.add_node('pathogenic_classification',pathogenic_classification)
graph.add_node('benign_classification',benign_classification)
graph.add_node('not_valid_classification',not_valid_classification)

graph.add_edge(START,'query_classification')
graph.add_conditional_edges('query_classification',category_classification)
graph.add_edge('pathogenic_classification',END)
graph.add_edge('benign_classification',END)

workflow = graph.compile()

def attribute_Prediction(query):
    print('called')
    return workflow.invoke({'query':query})
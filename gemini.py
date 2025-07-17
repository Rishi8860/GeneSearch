from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import HuggingFaceHub
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from models import Response
load_dotenv()

def attribute_Prediction(query):
    print("called")
    parser = PydanticOutputParser(pydantic_object=Response)
    # model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', convert_system_message_to_human=True)
    llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
    )

    embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local("acmg_vector_db", embeddings=embedding_model,allow_dangerous_deserialization=True)
    docs = db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    model = ChatHuggingFace(llm=llm)

    template = PromptTemplate(
        template = (
        "Based on the given query: '{query}', return the classification according to ACMG/AMP guidelines \nHere is the detailed Guidelines for the related creterias{docs} \n. Include both the final classification (e.g., 'Pathogenic', 'Likely Benign') and the specific ACMG criteria codes used (e.g., PS1, PM2, BS3), it can be more than one. Format the response as follows: {format_instruction}."),
    input_variables=['query','docs'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
    )

    chain = template | model | parser

    final_result = chain.invoke({'query':query,'docs':context})
            
    return final_result.dict()

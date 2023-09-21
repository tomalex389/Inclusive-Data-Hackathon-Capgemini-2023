# Bring in deps
import os 
import dotenv
from apikey import apikey 

import streamlit as st 
import langchain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('🦜🔗 MoneyManager - A Financial Advisory ChatBot')
prompt = st.text_input('What financial services are you interested in today? For example, how about Traditional/ROTH IRAs, 401Ks, or Stocks?') 

# Prompt templates
topic_template = PromptTemplate(
    input_variables = ['topic'], 
    template='Write me advice for the {topic}, specifically what are the top 5 best investments in this category'
)

advice_template = PromptTemplate(
    input_variables = ['entity'], 
    template='Thank you for those suggestions! Really appreciate it. Give me your best advice among the top 5 {entity}.'
)

# of/including
financial_institutions_template = PromptTemplate(
    input_variables = ['topic'], 
    template='Can you list five financial institutions that offer excellent financial services of {topic}? Which institution out of the five you listed is the best and why is the best?'
)

# Memory 
topic_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
advice_memory = ConversationBufferMemory(input_key='entity', memory_key='chat_history')
financial_institutions_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
topic_chain = LLMChain(llm=llm, prompt=topic_template, verbose=True, output_key='title', memory=topic_memory)
advice_chain = LLMChain(llm=llm, prompt=advice_template, verbose=True, output_key='advice', memory=advice_memory)
provider_chain = LLMChain(llm=llm, prompt=financial_institutions_template, verbose=True, output_key='financial_institutions', memory=financial_institutions_memory)
sequential_chain = SequentialChain(chains=[topic_chain, advice_chain, provider_chain], input_variables=['topic', 'entity'], output_variables=['topic', 'advice', 'financial_institutions'], verbose=True)

# Show stuff on the screen if there's a prompt
if prompt: 
    response = sequential_chain({'topic':prompt, 'entity': ''})  # Added 'entity' input key
    st.markdown("### MoneyManager generated the top-5 best investment vehicles for your topic: ")
    st.write(response['topic'])
    
    st.markdown("### MoneyManager advises you on what to invest in: ")
    st.write(response['advice'])

    st.markdown("### MoneyManager gives you a list of financial institutions that have the investment vehicle you are looking for: ")
    st.write(response['financial_institutions'])
    
    st.header("History of responses generated by MoneyManager: ")
    with st.expander('Best Investments History'): 
        st.info(topic_memory.buffer)

    with st.expander('Advice History'): 
        st.info(advice_memory.buffer)
    
    with st.expander('Financial Institutions History'): 
        st.info(financial_institutions_memory.buffer)

     
    # topic = topic_chain.run(topic = prompt)
    # advice = advice_chain.run(entity=topic)
    # provider = provider_chain.run(topic = prompt)

    # st.markdown("### MoneyManager generated the top-5 best investment vehicles for your topic: ")
    # st.write(topic) 
    # st.markdown("### MoneyManager advises you on what to invest in: ")
    # st.write(advice) 
    # st.markdown("### MoneyManager gives you a list of financial institutions that have the investment vehicle you are looking for: ")
    # st.write(provider) 

    # st.header("History of responses generated by MoneyManager: ")
    # with st.expander('Best Investments History'): 
    #     st.info(topic_memory.buffer)

    # with st.expander('Advice History'): 
    #     st.info(advice_memory.buffer)
    
    # with st.expander('Financial Institutions History'): 
    #     st.info(financial_institutions_memory.buffer)
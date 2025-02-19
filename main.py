from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM
from prompt import RESUME_PATH,JD_PATH
from colorama import Fore
import json



llm = OllamaLLM(model='deepseek-r1:7b')

loader = PyPDFLoader(file_path=RESUME_PATH)
documents = loader.load()
# print(documents)
texts = []
for doc in documents:
    page_content = doc.page_content
    texts.append(page_content)
# print(texts)
    
full_resume = ""
for text in texts:
    full_resume+=text


messages = [{
    'role': 'system',
    'content':f'You are given a copy of a job descripiton = {JD_PATH} and my resume = {full_resume}...based on the provided documents give me completely factual, unbiased answers to my queries. You can be stern and ruthless with your answers tough love is appreciated'
}]

while True:
    query = input('User: ')
    if query != '/quit':
        messages.append(dict(role = 'user', content = query))
        response = ""
        print(Fore.GREEN + "Bot: ")
        for chunk in llm.stream(f"chat_history = {messages}, query = {query}/"):
            print(chunk, end="", flush=True)
            response += str(chunk)
        print(Fore.RESET)
        messages.append(dict(role = 'bot', content = response))
    else:
        messages.append(dict(role = 'user', content = '/quit'))
        messages.append(dict(role = 'bot', content = 'It was nice talking to you ヾ(￣▽￣) Bye~Bye~'))
        with open(file='messages_0.json',mode="+w") as f:
            json.dump(messages, f, indent=4)
        print(Fore.GREEN + "Bot :It was nice talking to you ヾ(￣▽￣) Bye~Bye~")
        break
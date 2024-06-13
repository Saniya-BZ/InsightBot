

# measuring time

import time
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import FastEmbedEmbeddings

class ChatAI:
    def __init__(self):
        self.chat_history = []
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.model = ChatOllama(model="mistral", temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=256, chunk_overlap=50
        )
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
             maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self, pdf_file_path: str):
        try:
            start_time = time.time()
            docs = PyPDFLoader(file_path=pdf_file_path).load()
            print(f"Loaded {len(docs)} documents from {pdf_file_path}")

            if not docs:
                raise ValueError("No documents loaded from the PDF file.")

            chunks = []
            for doc in docs:
                text = doc.page_content
                chunks.extend(self.text_splitter.split_text(text))

            print(f"Split into {len(chunks)} chunks")

            if not chunks:
                raise ValueError("No chunks created from the document.")

            self.vector_store = Chroma.from_texts(
                texts=chunks, embedding=FastEmbedEmbeddings()
            )
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 3, "score_threshold": 0.5},
            )

            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.model,
                chain_type="stuff",
                retriever=self.retriever,
                combine_docs_chain_kwargs={"prompt": self.prompt},
                return_source_documents=True,
                return_generated_question=True,
            )

            end_time = time.time()
            print(f"Ingestion complete. Chain setup successful. Time taken: {end_time - start_time:.2f} seconds")
        except Exception as e:
            print(f"Error during ingestion: {e}")

    def ask(self, query: str):
        if not self.chain:
            print("Chain not initialized.")
            return "Please, add a PDF document first."

        try:
            start_time = time.time()
            result = self.chain.invoke({"question": query, "chat_history": self.chat_history})
            context = result["source_documents"]
            answer = result["answer"]

            if not context:
                answer = "Im forwarding this to help desk"

            self.chat_history.extend([(query, answer)])

            end_time = time.time()
            print(f"Question answered. Time taken: {end_time - start_time:.2f} seconds")

            print(f"\n\nChat History: {self.chat_history}")
            print(f"\n\nSource Documents: {context}")
            print(f"\n\nGenerated Question: {result['generated_question']}")

            return answer
        except Exception as e:
            print(f"Error during ask: {e}")
            return "An error occurred."

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.chat_history = []


















# #prompt change

# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     def __init__(self):
#         self.chat_history = []
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             chunks = []
#             for doc in docs:
#                 text = doc.page_content
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             self.vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = self.vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={"k": 3, "score_threshold": 0.5},
#             )

#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#             print("Ingestion complete. Chain setup successful.")
#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             print("Chain not initialized.")
#             return "Please, add a PDF document first."

#         result = self.chain.invoke({"question": query, "chat_history": self.chat_history})
#         context = result["source_documents"]
#         answer = result["answer"]

#         if not context:
#             answer = "Im forwading this to help desk"

#         self.chat_history.extend([(query, answer)])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {context}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return answer

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []

















# # testtttttttt

# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     def __init__(self):
#         self.chat_history = []
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             # Extract text and split into chunks
#             chunks = []
#             for doc in docs:
#                 text = doc.page_content  # Extract the text from the Document
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             self.vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = self.vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#             print("Ingestion complete. Chain setup successful.")

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             print("Chain not initialized.")
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []












# # this ooneeeeeeee

# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain




# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             # Extract text and split into chunks
#             chunks = []
#             for doc in docs:
#                 text = doc.page_content  # Extract the text from the Document
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             self.vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = self.vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#             print("Ingestion complete. Chain setup successful.")

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             print("Chain not initialized.")
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []


# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             # Extract text and split into chunks
#             chunks = []
#             for doc in docs:
#                 text = doc.page_content  # Extract the text from the Document
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []

























# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             # Extract text and split into chunks
#             chunks = []
#             for doc in docs:
#                 text = doc.page_content  # Extract the text from the Document
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []








#######FINEEEEEEEEEEEEEEEEEEEEe
# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")

#             if not docs:
#                 raise ValueError("No documents loaded from the PDF file.")

#             # Extract text and split into chunks
#             chunks = []
#             for doc in docs:
#                 text = doc.page_content  # Extract the text from the Document
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []










#OKKKKKKKKKKKKKKKKKKKKKKKKKKKK
# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load and split the document
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             chunks = self.text_splitter.split_documents(docs)

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")
            
#             # Create vector store
#             self.vector_store = Chroma.from_documents(
#                 documents=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = self.vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")
#             print(f"Split into {len(chunks)} chunks")

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []



















# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load and split the document
#             docs = PyPDFLoader(file_path=pdf_file_path).load()
#             chunks = self.text_splitter.split_documents(docs)

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")
            
#             # Create vector store
#             self.vector_store = Chroma.from_documents(
#                 documents=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = self.vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )
#             print(f"Loaded {len(docs)} documents from {pdf_file_path}")
#             print(f"Split into {len(chunks)} chunks")

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []



















# import fitz  # PyMuPDF
# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.embeddings import FastEmbedEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain

# class ChatAI:
#     chat_history = []
#     vector_store = None
#     retriever = None
#     chain = None

#     def __init__(self):
#         self.model = ChatOllama(model="mistral", temperature=0)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1024, chunk_overlap=100
#         )
#         self.prompt = PromptTemplate.from_template(
#             """
#             <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
#             to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
#              maximum and keep the answer concise. [/INST] </s> 
#             [INST] Question: {question} 
#             Context: {context} 
#             Answer: [/INST]
#             """
#         )

#     def ingest(self, pdf_file_path: str):
#         try:
#             # Load documents from the PDF file using PyMuPDF
#             doc = fitz.open(pdf_file_path)
#             texts = []
#             for page_num in range(len(doc)):
#                 page = doc.load_page(page_num)
#                 text = page.get_text()
#                 texts.append(text)
            
#             print(f"Loaded {len(texts)} pages from {pdf_file_path}")

#             if not texts:
#                 raise ValueError("No text extracted from the PDF file.")

#             # Split the text into chunks
#             chunks = []
#             for text in texts:
#                 chunks.extend(self.text_splitter.split_text(text))

#             print(f"Split into {len(chunks)} chunks")

#             if not chunks:
#                 raise ValueError("No chunks created from the document.")

#             # Create the vector store
#             vector_store = Chroma.from_texts(
#                 texts=chunks, embedding=FastEmbedEmbeddings()
#             )
#             self.retriever = vector_store.as_retriever(
#                 search_type="similarity_score_threshold",
#                 search_kwargs={
#                     "k": 3,
#                     "score_threshold": 0.5,
#                 },
#             )

#             # Create the conversational retrieval chain
#             self.chain = ConversationalRetrievalChain.from_llm(
#                 llm=self.model,
#                 chain_type="stuff",
#                 retriever=self.retriever,
#                 combine_docs_chain_kwargs={"prompt": self.prompt},
#                 return_source_documents=True,
#                 return_generated_question=True,
#             )

#         except Exception as e:
#             print(f"Error during ingestion: {e}")

#     def ask(self, query: str):
#         if not self.chain:
#             return "Please, add a PDF document first."

#         result = self.chain.invoke(
#             {"question": query, "chat_history": self.chat_history}
#         )
#         self.chat_history.extend([(query, result["answer"])])

#         print(f"\n\nChat History: {self.chat_history}")
#         print(f"\n\nSource Documents: {result['source_documents']}")
#         print(f"\n\nGenerated Question: {result['generated_question']}")

#         return result["answer"]

#     def clear(self):
#         self.vector_store = None
#         self.retriever = None
#         self.chain = None
#         self.chat_history = []




















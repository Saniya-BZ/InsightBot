
###### test

from flask import Flask, request, jsonify, send_from_directory
import os
from rag import ChatAI


app = Flask(__name__)
assistant = ChatAI()

DOCUMENTS_FOLDER = 'C:\\Users\\Administrator\\Downloads\\all_documents'
TEMPLATES_FOLDER = 'templates'

# Ensure documents folder exists
if not os.path.exists(DOCUMENTS_FOLDER):
    os.makedirs(DOCUMENTS_FOLDER)

@app.route('/ingest', methods=['POST'])
def ingest():
    files = request.files.getlist('files')
    for file in files:
        filename = file.filename
        file_path = os.path.join(DOCUMENTS_FOLDER, filename)
        file.save(file_path)
        if os.path.exists(file_path):
            print(f"Ingesting file from path: {file_path}")
            assistant.ingest(file_path)
        else:
            print(f"File path does not exist: {file_path}")
    return jsonify({"status": "success"})

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    # Re-initialize the assistant here if necessary
    if not assistant.chain:
        initialize_assistant()
    response = assistant.ask(query)
    return jsonify({"response": response})

@app.route('/fetch', methods=['GET'])
def fetch():
    documents = []
    for filename in os.listdir(DOCUMENTS_FOLDER):
        if filename.endswith('.pdf'):
            documents.append(filename)
    return jsonify({"documents": documents})

@app.route('/')
def index():
    return send_from_directory(TEMPLATES_FOLDER, 'index.html')

def initialize_assistant():
    # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
    for filename in os.listdir(DOCUMENTS_FOLDER):
        if filename.endswith('.pdf'):
            file_path = os.path.join(DOCUMENTS_FOLDER, filename)
            if os.path.exists(file_path):
                print(f"Loading document on startup from path: {file_path}")
                assistant.ingest(file_path)
            else:
                print(f"File path does not exist: {file_path}")


if __name__ == '__main__':
    initialize_assistant()
    app.run(debug=True)




# #thissss oneeeeeeeee
# from flask import Flask, request, jsonify, send_from_directory
# import os
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# DOCUMENTS_FOLDER = 'documents'
# TEMPLATES_FOLDER = 'templates'

# # Ensure documents folder exists
# if not os.path.exists(DOCUMENTS_FOLDER):
#     os.makedirs(DOCUMENTS_FOLDER)

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     files = request.files.getlist('files')
#     for file in files:
#         filename = file.filename
#         file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#         file.save(file_path)
#         if os.path.exists(file_path):
#             print(f"Ingesting file from path: {file_path}")
#             assistant.ingest(file_path)
#         else:
#             print(f"File path does not exist: {file_path}")
#     return jsonify({"status": "success"})

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     response = assistant.ask(query)
#     return jsonify({"response": response})

# @app.route('/fetch', methods=['GET'])
# def fetch():
#     documents = []
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             documents.append(filename)
#     return jsonify({"documents": documents})

# @app.route('/')
# def index():
#     return send_from_directory(TEMPLATES_FOLDER, 'index.html')

# if __name__ == '__main__':
#     # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#             if os.path.exists(file_path):
#                 print(f"Loading document on startup from path: {file_path}")
#                 assistant.ingest(file_path)
#             else:
#                 print(f"File path does not exist: {file_path}")
    
#     app.run(debug=True)
    


    
# if __name__ == '__main__':
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#             if os.path.exists(file_path):
#                 print(f"Loading document on startup from path: {file_path}")
#                 assistant.ingest(file_path)
#             else:
#                 print(f"File path does not exist: {file_path}")
    
#     app.run(debug=True)

# if __name__ == '__main__':
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#             if os.path.exists(file_path):
#                 print(f"Loading document on startup from path: {file_path}")
#                 assistant.ingest(file_path)
#             else:
#                 print(f"File path does not exist: {file_path}")
    
#     app.run(debug=True, use_reloader=False)










# #chatgpt

# from flask import Flask, request, jsonify, send_from_directory
# from flask import Flask, request, jsonify
# from rag import ChatAI
# import os
# app = Flask(__name__)
# assistant = ChatAI()

# DOCUMENTS_FOLDER = 'documents'
# TEMPLATES_FOLDER = 'templates'

# # Ensure documents folder exists
# if not os.path.exists(DOCUMENTS_FOLDER):
#     os.makedirs(DOCUMENTS_FOLDER)

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     files = request.files.getlist('files')
#     for file in files:
#         filename = file.filename
#         file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#         file.save(file_path)
#         print(f"Ingesting file from path: {file_path}")
#         assistant.ingest(file_path)
#     return jsonify({"status": "success"})


# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     response = assistant.ask(query)
#     return jsonify({"response": response})

# @app.route('/fetch', methods=['GET'])
# def fetch():
#     documents = []
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             documents.append(filename)
#     return jsonify({"documents": documents})

# @app.route('/')
# def index():
#     return send_from_directory(TEMPLATES_FOLDER, 'index.html')

# if __name__ == '__main__':
#     # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             print(f"Loading document on startup from path: {file_path}")
#             assistant.ingest(os.path.join(DOCUMENTS_FOLDER, filename))
    
#     app.run(debug=True)










# ##### this one
# import os
# from flask import Flask, request, jsonify
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# DOCUMENTS_FOLDER = 'documents'

# # Ensure documents folder exists
# if not os.path.exists(DOCUMENTS_FOLDER):
#     os.makedirs(DOCUMENTS_FOLDER)

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     files = request.files.getlist('files')
#     for file in files:
#         filename = file.filename
#         file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#         file.save(file_path)
#         assistant.ingest(file_path)
#     return jsonify({"status": "success"})

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     response = assistant.ask(query)
#     return jsonify({"response": response})
# @app.route('/fetch', methods=['GET'])
# def fetch():
#     documents = []
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             documents.append(filename)
#     return jsonify({"documents": documents})

# if __name__ == '__main__':
#     # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             assistant.ingest(os.path.join(DOCUMENTS_FOLDER, filename))
    
#     app.run(debug=True)
































# import os
# from flask import Flask, request, jsonify
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# DOCUMENTS_FOLDER = 'documents'

# # Ensure documents folder exists
# if not os.path.exists(DOCUMENTS_FOLDER):
#     os.makedirs(DOCUMENTS_FOLDER)

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     files = request.files.getlist('files')
#     for file in files:
#         filename = file.filename
#         file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#         file.save(file_path)
#         assistant.ingest(file_path)
#     return jsonify({"status": "success"})

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     response = assistant.ask(query)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             assistant.ingest(os.path.join(DOCUMENTS_FOLDER, filename))
    
#     app.run(debug=True)









#fineeeeeeeeeeeeeeeeeeee
# import os
# from flask import Flask, request, jsonify
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# DOCUMENTS_FOLDER = 'documents'

# # Ensure documents folder exists
# if not os.path.exists(DOCUMENTS_FOLDER):
#     os.makedirs(DOCUMENTS_FOLDER)

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     files = request.files.getlist('files')
#     for file in files:
#         filename = file.filename
#         file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#         file.save(file_path)
#         assistant.ingest(file_path)
#     return jsonify({"status": "success"})

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     response = assistant.ask(query)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     # Ingest all existing documents in the DOCUMENTS_FOLDER on startup
#     for filename in os.listdir(DOCUMENTS_FOLDER):
#         if filename.endswith('.pdf'):
#             assistant.ingest(os.path.join(DOCUMENTS_FOLDER, filename))
    
#     app.run(debug=True)

    





















#OKKKKKKKKKKKKKKKKKKKKKK
# import os
# from flask import Flask, request, jsonify
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# # Path to your Downloads folder (adjust if needed)
# DOCUMENTS_FOLDER = "C:\\Users\\Administrator\\Downloads\\All_files"

# # Ingest PDFs from the Downloads folder at startup
# for filename in os.listdir(DOCUMENTS_FOLDER):
#     if filename.endswith(".pdf"):
#         assistant.ingest(os.path.join(DOCUMENTS_FOLDER, filename))

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.json
#     query = data.get('query', '')
#     response = assistant.query(query)
#     return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)



















# import os
# from flask import Flask, request, jsonify, render_template
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# # Define the path to the downloads folder where your PDFs are stored
# DOCUMENTS_FOLDER = 'C:/Users/Administrator/Downloads/All_files'  # Update this path accordingly

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     try:
#         # Iterate over all files in the DOCUMENTS_FOLDER
#         for filename in os.listdir(DOCUMENTS_FOLDER):
#             if filename.endswith('.pdf'):
#                 file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#                 assistant.ingest(file_path)
#         return jsonify({"message": "Documents ingested successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     if query:
#         response = assistant.ask(query)
#         return jsonify({"response": response}), 200
#     return jsonify({"error": "No query provided"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)














# import os
# from flask import Flask, request, jsonify, render_template
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# # Define the path to the downloads folder where your PDFs are stored
# DOCUMENTS_FOLDER = 'C:/Users/Administrator/Downloads/All_files'  # Update this path accordingly

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     try:
#         # Iterate over all files in the DOCUMENTS_FOLDER
#         for filename in os.listdir(DOCUMENTS_FOLDER):
#             if filename.endswith('.pdf'):
#                 file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#                 assistant.ingest(file_path)
#         return jsonify({"message": "Documents ingested successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     if query:
#         response = assistant.ask(query)
#         return jsonify({"response": response}), 200
#     return jsonify({"error": "No query provided"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)



























# import os
# from flask import Flask, request, jsonify, render_template
# from rag import ChatAI

# app = Flask(__name__)
# assistant = ChatAI()

# # Define the path to the downloads folder where your PDFs are stored
# DOCUMENTS_FOLDER = "C:/Users/Administrator/Downloads/All_files"  # Update this path accordingly

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ingest', methods=['POST'])
# def ingest():
#     try:
#         # Iterate over all files in the DOCUMENTS_FOLDER
#         for filename in os.listdir(DOCUMENTS_FOLDER):
#             if filename.endswith('.pdf'):
#                 file_path = os.path.join(DOCUMENTS_FOLDER, filename)
#                 assistant.ingest(file_path)
#         return jsonify({"message": "Documents ingested successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.json.get('query')
#     if query:
#         response = assistant.ask(query)
#         return jsonify({"response": response}), 200
#     return jsonify({"error": "No query provided"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)













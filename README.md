## TEAM BANANA 

![image](https://github.com/42cursus/42hackathon2024/assets/66947064/e55e5a32-42d5-4058-9dd6-34a554123ae0)

Produced through @Microsoft Copilot by @uknowWho


AI-Powered Teaching Assistant: Your Personal Educator

Meet Banana Education, the AI-driven study assistant designed to capture the essence of educational content with PDF textbooks summarization, customizable assessments and fast review quizzes creation. Designed for teachers who seek efficient tools to create engaging assessments as well as for students across various academic levels who benefit from concise summaries of educational materials, interactive review activities, and personalized assessments tailored to their learning needs.


    Upload: Simply upload your PDF document.
    Analyze: Our AI-Powered Teaching Assistant will analyze the content, breaking it down into manageable sections.
    Learn: You can then interact with the content in a dynamic and engaging way, with features like text-to-speech, interactive quizzes, and summarized notes.

Key Features

    Smart Analysis: AI technology breaks down complex information into easy-to-understand sections.
    Interactive Learning: Engage with the content through text-to-speech, quizzes, and summarized notes.
    Accessible: User-friendly design makes learning accessible for all

### Some necessary tools
```
pip3 install faiss-cpu langchain-openai BeautifulSoup4 langchain-community langchain anthropic
```

### Useful links
[anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

[OpenAI Quickstart](https://platform.openai.com/docs/quickstart?context=python)

[Computing Sentence Embeddings](https://www.sbert.net/examples/applications/computing-embeddings/README.html)

[Retrieval Augmented Generation (RAG)](https://deci.ai/blog/retrieval-augmented-generation-using-langchain/)


### Project structure
```
.
├── claude                 # "claude" is a Python package
│     ├── __init__.py      # this file makes "app" a "Python package"
│     ├── main.py          # "main" module, e.g. import app.main
│     ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│     └── routers          # "routers" is a "Python subpackage"
│     │   ├── __init__.py  # makes "routers" a "Python subpackage"
│     │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│     │   ├── chat.py      # "chat" submodule, e.g. import app.routers.chat
│     │   └── users.py     # "users" submodule, e.g. import app.routers.users
│     └── claude_retriever # "claude_retriever" is a "Python subpackage"
│         ├── __init__.py  # makes "claude_retriever" a "Python subpackage"
│         └── client.py     # "admin" submodule, e.g. import app.internal.admin
```

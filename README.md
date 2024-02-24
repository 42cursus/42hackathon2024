pip3 install faiss-cpu langchain-openai BeautifulSoup4 langchain-community langchain anthropic

[anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)
[OpenAI Quickstart](https://platform.openai.com/docs/quickstart?context=python)
[Computing Sentence Embeddings](https://www.sbert.net/examples/applications/computing-embeddings/README.html)
[Retrieval Augmented Generation (RAG)](https://deci.ai/blog/retrieval-augmented-generation-using-langchain/)
      

.
├── app                    # "app" is a Python package
│     ├── __init__.py      # this file makes "app" a "Python package"
│     ├── main.py          # "main" module, e.g. import app.main
│     ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│     └── routers          # "routers" is a "Python subpackage"
│     │   ├── __init__.py  # makes "routers" a "Python subpackage"
│     │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│     │   └── users.py     # "users" submodule, e.g. import app.routers.users
│     └── internal         # "internal" is a "Python subpackage"
│         ├── __init__.py  # makes "internal" a "Python subpackage"
│         └── admin.py     # "admin" submodule, e.g. import app.internal.admin
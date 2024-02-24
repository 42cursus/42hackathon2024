import os
import sys
import anthropic
import claude_retriever
from claude_retriever.searcher.searchtools.websearch import BraveSearchTool
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import nest_asyncio
nest_asyncio.apply()
import json

# Import and configure logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a handler to log to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(handler)

ANTHROPIC_SEARCH_MODEL = "claude-2"
api_key = os.environ['ANTHROPIC_API_KEY']

# Create a searcher
brave_search_tool = BraveSearchTool(
    brave_api_key=os.environ["BRAVE_API_KEY"],
    summarize_with_claude=True,
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]
)


async def do_request(query):
    print("in anthropic_svc.do_request")
    print(query)
    # Run a test query
    query = "2023 World Cup"
    # results = brave_search_tool.search(query=query, n_search_results_to_use=3)

    client = claude_retriever.ClientWithRetrieval(
        api_key=api_key,
        search_tool=brave_search_tool
    )

    # query = "Who scored the most goals in the 2023 Women's World Cup?"
    prompt = f'{anthropic.HUMAN_PROMPT} {query}{anthropic.AI_PROMPT}'

    basic_response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model=ANTHROPIC_SEARCH_MODEL,
        max_tokens_to_sample=1000,
    )

    # print('-'*50)
    # print('Basic response:')
    # print(prompt + basic_response.completion)
    # print('-'*50)
    #
    augmented_response = client.completion_with_retrieval(
        query=query,
        model=ANTHROPIC_SEARCH_MODEL,
        n_search_results_to_use=1,
        max_searches_to_try=3,
        max_tokens_to_sample=1000
    )

    resp = {
        "augmented_response":  augmented_response,
        "basic_response": basic_response.completion
    }
    json_str = json.dumps(resp, indent=4)
    return json_str

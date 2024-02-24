import os
import sys
import anthropic
import claude_retriever
from claude_retriever.searcher.searchtools.websearch import BraveSearchTool
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import nest_asyncio
nest_asyncio.apply()

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

anthropic_search_model = "claude-2"
api_key = os.environ['ANTHROPIC_API_KEY']

# Create a searcher
brave_search_tool = BraveSearchTool(
    brave_api_key=os.environ["BRAVE_API_KEY"],
    summarize_with_claude=True,
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"]
)

client = claude_retriever.ClientWithRetrieval(
    api_key=api_key,
    verbose=True,
    search_tool=brave_search_tool
)

def get_completion(client, prompt, max_tokens=3000):
    compl = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=max_tokens,
        model=anthropic_search_model
    )
    return compl.completion


async def do_request(query):
    # Run a test query
    results = brave_search_tool.search(query=query, n_search_results_to_use=3)
    print(results)

    # query = "Who scored the most goals in the 2023 Women's World Cup?"
    prompt = f'{anthropic.HUMAN_PROMPT} {query}{anthropic.AI_PROMPT}'

    basic_response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model=anthropic_search_model,
        max_tokens_to_sample=1000,
    )

    aug_answer = client.completion_with_retrieval(
        query=query,
        model=anthropic_search_model,
        n_search_results_to_use=1,
        max_searches_to_try=3,
        max_tokens_to_sample=1000
    )

    basic_resp = basic_response.completion.strip()
    aug_resp = client.extract_between_tags('message',
                                           aug_answer + '</message>',
                                           strip=True)
    print(basic_resp)
    print(aug_resp)
    resp = {
        "basic_response": basic_resp,
        "augmented_response": aug_resp
    }
    return resp

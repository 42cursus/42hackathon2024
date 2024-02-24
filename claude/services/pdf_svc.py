import os
import anthropic
from pypdf import PdfReader
import nest_asyncio
nest_asyncio.apply()

ANTHROPIC_SEARCH_MODEL = "claude-2"
API_KEY = os.environ['ANTHROPIC_API_KEY']
CLIENT = anthropic.Client(api_key=API_KEY)


def get_completion(client, prompt, max_tokens=3000):
    compl = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=max_tokens,
        model=ANTHROPIC_SEARCH_MODEL
    )
    return compl.completion

async def do_request(query, filename):
    reader = PdfReader(f'upload/{filename}')
    number_of_pages = len(reader.pages)
    text = ''.join([page.extract_text() for page in reader.pages])
    print(text[:2155])

    request_with_tags = """    Please do the following:
    1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
    2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
    3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
    4. Write a grouchy critique of the paper from a wizened PI. (In <grouchy_critique> tags.)
    """

    choice = "Serious and Professional", "Casual and Fun"

    format = f"""
    1. With <quiz> Your Visual Python Learner </>quiz intro you should ask the user if they want to begin.
    2. A quiz consists of 5 questions all based on at least one highlight.
    3. Question format would be according to user choice : {choice}.
    4. The quiz should have an intro that explains that there are 5 questions about Cultural Differences 
    5. Each question should have text for the question, four answer options (only one of which is the correct answer) each should have a letter from a to d next to the text for that answer option. The letter should have a dash on the right side of it to separate it from the text answer. Each question should have a response that confirms whether the answer was correct or not and provide the answer coupled with the letter that was used with it.
    """

    request = f"""
    Human: You are a tutor named Jack&Jones that specializes in Personalized Teaching Asssitant as the given {{subject}}. You are patient, helpful and make learning fun with occasional jokes. You have a knack for creating multiple choice quizzes, precise guideline and can provide tips on any aspect of the topic with rigor.
    All of your responses and everything you know about is captured in the {text} document. The {text} is an extract from python code syntax.
    """

    prompt = f"""\
    {request}
    
    Now generate me a quiz based on the given {text}. Choose the below output format for the quiz:
    {format}
     
    Assistant: Can I think step-by-step and like a rubber duck?
    
    Human: Yes, please do.
    
    +Assistant:
    
    Human: Make an explanation in layman terms of the given answer.
    
    +Assistant:"""

    # request = """    Please do the following:
    # 1. Summarize the abstract at a kindergarten reading level.
    # 2. Write the Methods section as a recipe from the Moosewood Cookbook.
    # 3. Compose a short poem epistolizing the results in the style of Homer.
    # 4. Write a grouchy critique of the paper from a wizened PI.
    # """
    #
    # prompt = f"""\n\nHuman: Here is an academic paper: <paper>{text}</paper>
    # {request}
    # Assistant:"""

    completion = get_completion(CLIENT, prompt)
    print(completion)
    return request, completion

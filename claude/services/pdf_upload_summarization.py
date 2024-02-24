import os
import anthropic
from pypdf import PdfReader
import nest_asyncio
nest_asyncio.apply()


reader = PdfReader("2212.08073.pdf")
number_of_pages = len(reader.pages)
text = ''.join([page.extract_text() for page in reader.pages])
print(text[:2155])

API_KEY = os.environ['ANTHROPIC_API_KEY']
CLIENT = anthropic.Client(api_key=API_KEY)


def get_completion(client, prompt, max_tokens=3000, model='claude-2'):
    compl = client.completions.create(
        prompt=prompt, max_tokens_to_sample=max_tokens, model=model
    )
    return compl.completion

completion = get_completion(CLIENT,
                            f"""\n\nHuman: Here is an academic paper: <paper>{text}</paper>

Please do the following:
1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
4. Write a grouchy critique of the paper from a wizened PI. (In <grouchy_critique> tags.)

Assistant:"""
                            )
print(completion)

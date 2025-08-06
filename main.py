import functions_framework
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load env vars locally (ignored on Google Cloud)
load_dotenv()

@functions_framework.http
def create_slogan_with_parameters(request):
    request_json = request.get_json(silent=True)

    if not request_json or 'name' not in request_json:
        return {"error": "Missing 'name' in JSON body"}, 400

    business_description = request_json['name']
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that creates one slogan based on company descriptions."
            },
            {
                "role": "user",
                "content": business_description
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    slogan = response.choices[0].message.content

    return {
        "slogan": slogan,
        "number_of_characters": len(slogan)
    }

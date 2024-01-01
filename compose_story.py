from openai import OpenAI
import json


def compose_story():
    config = json.load(open("config.json"))
    open_ai_api_key = config["openai_api_key"]

    client = OpenAI(api_key=open_ai_api_key)
    response = client.chat.completions.create(
                        model="gpt-3.5-turbo-1106",
                        response_format={"type": "json_object"},
                        messages=[
                                {"role": "system", "content": "You are a story writer that writes horror stories. " +
                                 "the story will have title and paragraphs in JSON format"},
                                {"role": "user", "content": "Write a horror story in 3 paragraphs, with a maximum of 220 words"}])
    json_obj = json.loads(response.choices[0].message.content)
    # print(json_obj)

    # create a input file with the json content
    with open("input.txt", "w") as f:
        f.write(json_obj['title'] + "\n\n")
        for para in json_obj['paragraphs']:
            f.write(para + "\n\n")
        f.close()

from openai import OpenAI
import json


def compose_story():
    config = json.load(open("config.json"))
    open_ai_api_key = config["openai_api_key"]

    client = OpenAI(api_key=open_ai_api_key)
    response = client.chat.completions.create(
                        model=config["openai_model_for_story"],
                        response_format={"type": "json_object"},
                        messages=[
                                {"role": "system", "content": config["story_composer_context"]},
                                {"role": "user", "content": config["story_composer_prompt"]}])
    json_obj = json.loads(response.choices[0].message.content)

    # create a input file with the json content
    with open(config["story_file_name"], "w") as f:
        f.write(json_obj['title'] + "\n\n")
        for para in json_obj['paragraphs']:
            f.write(para + "\n\n")
        f.close()

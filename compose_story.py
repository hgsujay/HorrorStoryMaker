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
    # write json_obj to a file
    with open("input.json", "w") as f:
        json.dump(json_obj, f, indent=4)
        f.close()


# compose_story()

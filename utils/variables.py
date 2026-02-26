import json
import os

def load_variables(stack):

    file_path = f"/server/{os.environ["PROJECT_NAME"]}/.config/env"

    # Import variables from json file
    with open(f"{file_path}/{stack}.json", "r") as f:

        env_variables = json.loads(f.read())

        for name, value in env_variables.items():
            os.environ[name] = str(value)
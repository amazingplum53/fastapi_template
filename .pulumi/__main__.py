"""An AWS Python Pulumi program"""

import pulumi

config = pulumi.Config()
stack = pulumi.get_stack()

import prod
import dev
import sys

PROJECT_NAME = "fastapi_template"

stack_main = {
    "prod": prod,
    "dev": dev,
}.get(stack)

sys.path.append(f"/server/{PROJECT_NAME}")

from utils.variables import load_variables

load_variables(STACK)

if stack_main is None:
    raise ValueError(f"Unsupported stack: {stack}")

stack_main.deploy(stack, PROJECT_NAME)

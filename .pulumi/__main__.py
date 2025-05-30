"""An AWS Python Pulumi program"""

import pulumi

config = pulumi.Config()
stack = pulumi.get_stack()

import prod
import dev

stack_main = {
    "prod": prod,
    "dev": dev,
}.get(stack)

if stack_main is None:
    raise ValueError(f"Unsupported stack: {stack}")

stack_main.deploy(stack)

import weave
import wandb
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Initialize Weave — all Mistral calls are now traced!
weave.init("mistral-hackathon")

# Initialize W&B run
wandb.init(project="mistral-hackathon", name="mistral-chat")

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found. Add it to your environment or .env file.")

client = Mistral(api_key=api_key)

MODEL = "mistral-small-latest"
PROMPT = "Hello Mistral!"

wandb.config.update({"model": MODEL, "prompt": PROMPT})

@weave.op
def chat(prompt: str) -> str:
    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    wandb.log({
        "prompt": prompt,
        "response": content,
        "model": MODEL,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    })

    return content

result = chat(PROMPT)

wandb.finish()


from app.schemas.prompts import RegisterPrompt,PromptResponse
import mlflow

def register_prompt(prompt:RegisterPrompt) -> PromptResponse:
    response = mlflow.genai.register_prompt(
        name=prompt.name,
        commit_message=prompt.commit_message,
        template=prompt.template
    )
    return response.name, response.version

def load_prompt_name(name,version):
    return mlflow.genai.load_prompt(f"prompts:/{name}/{version}")
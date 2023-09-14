from flask import Blueprint
from prisma.models import Prompt

prompts_bp = Blueprint('prompts', __name__)

@prompts_bp.route("/prompts")
def return_all_prompts():

    all_prompts = Prompt.prisma().find_many()

    return {"data" : [prompts.model_dump() for prompts in all_prompts]}
import chainlit as cl

import guidance
from guidance import models, user, system, assistant, gen


# run this with: chainlit run chatty.py -w

# load a model (could be Transformers, LlamaCpp, VertexAI, OpenAI...)
llama3 = models.LlamaCpp('./llama3.gguf', echo=False)

@cl.on_chat_start
def on_chat_start():
    with system():
        lm = llama3 + 'You are a helpful and terse assistant.'
        cl.user_session.set("lm", lm)

    
@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="")
    await msg.send()

    lm = cl.user_session.get("lm")
    with user():
        lm += message.content

    with assistant():
        lm += gen(name="assistant", stop='.')
        msg.content = lm["assistant"]

    cl.user_session.set("lm", lm)

    await msg.update()


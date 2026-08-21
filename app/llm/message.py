def add_user_message(messages,text):
    message = {
        "role":"user",
        "content":text
    }
    messages.append(message)
    
def add_assistant_message(messages,response):
    message = {
        "role":"assistant",
        "content":response.content
    }
    messages.append(message)

def text_from_message(message):
    return "\n".join(block.text for block in message.content if block.type =="text")

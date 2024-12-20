import json

def topic_join(*sections):
    """join mqtt topic sections
    """
    topic=""
    for s in sections:
        if topic and not topic.endswith("/"):
            topic+="/"
        topic+=s
    return topic


def payload_to_dict(payload):
    """ To parse json payload
    """
    return json.loads(payload.decode("utf-8"))


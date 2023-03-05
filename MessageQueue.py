import time


class MessageQueue:

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    PROMPT = {
            "role": SYSTEM,
            "content": "You are a helpful assistant."
        }

    def __init__(self,
                 encoding,
                 max_length=20,
                 max_tokens=4000,
                 expiration=1000):

        self.Queue = []
        self.length = 0
        self.encoding = encoding
        self.expiration = expiration
        self.max_length = max_length
        self.max_tokens = max_tokens

    def add_message(self, message, role=USER):
        encode_message = self.encoding.encode(message)
        size = len(encode_message)
        if size >= self.max_tokens:
            return False
        body = {
            "role": role,
            "message": message,
            "timestamp": time.time(),
            "size": size
        }
        self.Queue.append(body)
        self.Queue = self.Queue[-self.max_length:]
        return True

    def get_recent_messages(self):
        now = time.time()
        result_size = 0
        result = [MessageQueue.PROMPT]
        for i in range(len(self.Queue) - 1, -1, -1):
            message_body = self.Queue[i]
            if now - message_body["timestamp"] > self.expiration:
                break
            size = message_body['size']
            if result_size + size < self.max_tokens:
                output = {
                    'role': message_body['role'],
                    'content': message_body['message']
                }
                result.insert(1, output)
                result_size += size
        if len(result) > 1:
            return result
        else:
            return False


if __name__ == "__main__":
    import tiktoken

    model_name = "gpt-3.5-turbo"
    encoding = tiktoken.encoding_for_model(model_name)
    mq = MessageQueue(encoding)
    message = "Who are you?"
    mq.add_message(message)
    mq.add_message("Hello!")
    mq.add_message("Hello!"*4000)
    result = mq.get_recent_messages()
    ...
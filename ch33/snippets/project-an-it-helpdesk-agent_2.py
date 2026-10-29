import anthropic
import httpx2 as httpx        # recent anthropic SDKs use httpx2; older ones use httpx


def handler(request: httpx.Request):
    sent.append(json.loads(request.content))
    return httpx.Response(200, json={"id": "msg_1", "type": "message", "role": "assistant",
                                     "model": oa.MODEL, "stop_sequence": None,
                                     "usage": {"input_tokens": 50, "output_tokens": 10}, **next(replies)})

client = anthropic.Anthropic(api_key="test", http_client=httpx.Client(transport=httpx.MockTransport(handler)))

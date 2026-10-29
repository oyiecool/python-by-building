import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from the environment
msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=500,
    messages=[{"role": "user", "content": "In one sentence, what does df -h show?"}],
)
print(msg.content[0].text)
print(msg.stop_reason, msg.usage.input_tokens, msg.usage.output_tokens)

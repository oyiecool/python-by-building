import json

import anthropic
import httpx2 as httpx           # the HTTP library the anthropic SDK uses
import pytest

import opsagent as oa


def test_path_traversal_blocked():
    out, err = oa.call_tool("tail_log", {"name": "../../opsagent.py"}, lambda *a: True)
    assert err and "unknown log" in out


def test_host_allow_list():
    out, err = oa.call_tool("check_port", {"host": "8.8.8.8", "port": 53}, lambda *a: True)
    assert err and "allow-list" in out


def test_risky_tool_needs_approval():
    out, err = oa.call_tool("restart_service", {"name": "nginx"}, lambda *a: False)
    assert err and "declined" in out
    out, err = oa.call_tool("restart_service", {"name": "nginx"}, lambda *a: True)
    assert not err and "systemctl restart nginx" in out


def test_unknown_service_and_tool():
    assert oa.call_tool("restart_service", {"name": "sshd"}, lambda *a: True)[1]
    assert oa.call_tool("rm_rf", {}, lambda *a: True)[1]


def test_step_limit(tmp_path):
    loop = [[oa._block("tool_use", id=f"t{i}", name="disk_usage", input={"host": "web01", "path": "/"})]
            for i in range(3)]
    answer, steps, _ = oa.run_agent("x", oa.ScriptedClient(loop), max_steps=3, log_path=tmp_path / "l")
    assert answer.startswith("Stopped") and steps == 3


def test_demo_passes_results_back(tmp_path):
    c = oa.ScriptedClient(oa.DEMO)
    answer, steps, used = oa.run_agent("uploads fail", c, lambda *a: False, log_path=tmp_path / "l")
    assert steps == 4 and "98.5%" in answer
    second = c.seen[2]["content"]                     # results of tail_log + disk_usage, in order
    assert [r["tool_use_id"] for r in second] == ["t2", "t3"]
    assert '"used_pct": 98.5' in second[1]["content"]
    assert len((tmp_path / "l").read_text().splitlines()) == 4


def test_with_real_sdk_objects(tmp_path):
    """Run the loop through the real anthropic client against a fake HTTP server."""
    sent = []
    replies = iter([
        {"content": [{"type": "text", "text": "Checking."},
                     {"type": "tool_use", "id": "toolu_1", "name": "disk_usage",
                      "input": {"host": "db01", "path": "/"}}], "stop_reason": "tool_use"},
        {"content": [{"type": "text", "text": "db01 is fine: 30.7% free."}], "stop_reason": "end_turn"},
    ])

    def handler(request: httpx.Request):
        sent.append(json.loads(request.content))
        r = next(replies)
        return httpx.Response(200, json={"id": "msg_1", "type": "message", "role": "assistant",
                                         "model": oa.MODEL, "stop_sequence": None,
                                         "usage": {"input_tokens": 50, "output_tokens": 10}, **r})

    client = anthropic.Anthropic(api_key="test", http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    answer, steps, used = oa.run_agent("is db01 ok?", client, log_path=tmp_path / "l")
    assert answer == "db01 is fine: 30.7% free." and steps == 2 and used == {"input": 100, "output": 20}
    assert {t["name"] for t in sent[0]["tools"]} == set(oa.TOOLS)
    tool_result = sent[1]["messages"][-1]["content"][0]
    assert tool_result["type"] == "tool_result" and tool_result["tool_use_id"] == "toolu_1"
    assert sent[1]["messages"][1]["content"][1]["type"] == "tool_use"   # assistant turn sent back intact

import json
from pathlib import Path

import pytest
from packaging.version import Version

import vulncheck as vc

DB = json.loads(Path(__file__).with_name("osv_sample.json").read_text())


@pytest.mark.parametrize("ver,hit", [("1.26.16", True), ("1.26.17", False), ("2.0.0", True),
                                     ("2.0.5", True), ("2.0.6", False), ("2.2.0", False)])
def test_urllib3_two_ranges(ver, hit):
    assert vc.affects(DB[1], "urllib3", ver)[0] is hit


def test_fixed_version_reported():
    assert vc.affects(DB[1], "urllib3", "2.0.3") == (True, "2.0.6")


def test_name_normalisation(tmp_path):
    req = tmp_path / "r.txt"
    req.write_text("Jinja2==3.1.2\nrequests[socks]==2.28.1 ; python_version>'3'\nflask>=3\n")
    pinned, skipped = vc.read_requirements(req)
    assert pinned == {"jinja2": "3.1.2", "requests": "2.28.1"} and skipped == ["flask>=3"]


def test_last_affected():
    rec = {"id": "X", "affected": [{"package": {"ecosystem": "PyPI", "name": "demo"},
           "ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "1.0"}, {"last_affected": "1.4"}]}]}]}
    assert vc.affects(rec, "demo", "1.4")[0] and not vc.affects(rec, "demo", "1.5")[0]


class FakeResp:
    def __init__(self, data): self.data = data
    def raise_for_status(self): pass
    def json(self): return self.data


class FakeSession:
    """Stands in for requests.Session so the online path is tested without a network."""
    def __init__(self): self.calls = []
    def post(self, url, json, timeout):
        self.calls.append(url)
        return FakeResp({"results": [{"vulns": [{"id": "GHSA-h5c8-rqwp-cp95"}]} if q["package"]["name"] == "jinja2"
                                     else {} for q in json["queries"]]})
    def get(self, url, timeout):
        self.calls.append(url)
        return FakeResp(next(r for r in DB if url.endswith(r["id"])))


def test_online_mode_uses_batch_then_details():
    s = FakeSession()
    recs = vc.records_online({"jinja2": "3.1.2", "flask": "3.0.3"}, session=s)
    assert s.calls == [f"{vc.OSV}/querybatch", f"{vc.OSV}/vulns/GHSA-h5c8-rqwp-cp95"]
    f = vc.check({"jinja2": "3.1.2", "flask": "3.0.3"}, recs)
    assert [(x.package, x.fixed_in, x.severity) for x in f] == [("jinja2", "3.1.3", "MODERATE")]

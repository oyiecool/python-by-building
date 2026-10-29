# test_dashboard.py
from streamlit.testing.v1 import AppTest


def test_dashboard_runs_and_filters():
    at = AppTest.from_file("dashboard.py").run(timeout=30)
    assert not at.exception
    assert at.title[0].value == "Sales dashboard"
    assert at.metric[1].value == "1,200"
    at.sidebar.multiselect[0].set_value(["NCR"]).run()
    assert at.caption[0].value.endswith("of 1,200 orders match the filters")
    assert at.metric[1].value != "1,200"


def test_empty_filter_warns():
    at = AppTest.from_file("dashboard.py").run(timeout=30)
    at.sidebar.multiselect[1].set_value([]).run()
    assert at.warning[0].value == "No orders match these filters."

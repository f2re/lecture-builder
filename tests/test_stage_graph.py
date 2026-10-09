import pytest
from lecture_tools.stage_graph import descendants, invalidate, ready_stages, route_findings


def test_ready_and_invalidation():
    state = {"stages": {"config": {"status":"complete"}, "sections":{"status":"complete"}, "publish-docx":{"status":"complete"}}}
    assert "research-search" in ready_stages(state)
    assert "fact-check" in descendants("sections")
    invalidate(state, "sections", "formula correction")
    assert state["stages"]["publish-docx"]["status"] == "stale"
    assert state["stages"]["config"]["status"] == "complete"


def test_formula_goes_to_author_not_final_editor():
    reports = {"scientific":{"findings":[{"finding_id":"s1","severity":"major","category":"formula","required_action":"Correct sign"}]}}
    plan = route_findings(reports, cycle=1, max_cycles=2)
    assert plan["requests"][0]["owner"] == "section-writer"
    assert route_findings(reports, cycle=3, max_cycles=2)["status"] == "blocked"


def test_invalid_cycle_rejected():
    with pytest.raises(ValueError):
        route_findings({}, cycle=0, max_cycles=2)

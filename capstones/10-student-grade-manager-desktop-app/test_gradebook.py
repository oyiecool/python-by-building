# test_gradebook.py
from gradebook import GradeBook, letter

def test_weighted_grade(tmp_path):
    gb = GradeBook(tmp_path / "t.db")
    sid = gb.add_student("test person")
    gb.add_score(sid, "quiz", "Q1", 18, 20)       # 90%
    gb.add_score(sid, "exam", "Midterm", 70, 100) # 70%
    assert gb.final_percent(sid) == 77.5          # (0.3*90 + 0.5*70) / 0.8
    assert letter(77.5) == "C"

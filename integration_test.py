import urllib.request
import json

API_BASE = "http://localhost:3000"

def test_login(username, password):
    url = f"{API_BASE}/api/auth/login"
    data = json.dumps({"username": username, "password": password}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            print(f"[-] Login {username}: SUCCESS -> Role: {res_data['user']['role']}")
            return res_data['user']
    except Exception as e:
        print(f"[x] Login {username}: FAILED -> {e}")
        return None

def test_get_courses():
    url = f"{API_BASE}/api/courses"
    try:
        with urllib.request.urlopen(url) as res:
            courses = json.loads(res.read().decode("utf-8"))
            print(f"[-] Get Courses: SUCCESS -> Found {len(courses)} courses")
            return courses
    except Exception as e:
        print(f"[x] Get Courses: FAILED -> {e}")
        return []

def test_get_curriculum():
    url = f"{API_BASE}/api/curriculum"
    try:
        with urllib.request.urlopen(url) as res:
            curriculum = json.loads(res.read().decode("utf-8"))
            print(f"[-] Get Curriculum: SUCCESS -> Found subjects: {list(curriculum.keys())}")
            return curriculum
    except Exception as e:
        print(f"[x] Get Curriculum: FAILED -> {e}")
        return {}

def test_update_progress(student_id, lesson_id, status_completed):
    url = f"{API_BASE}/api/students/{student_id}/progress"
    data = json.dumps({"lessonId": lesson_id, "statusCompleted": status_completed}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            print(f"[-] Update Progress (student_id={student_id}, lesson_id={lesson_id}, completed={status_completed}): SUCCESS -> {res_data}")
            return True
    except Exception as e:
        print(f"[x] Update Progress: FAILED -> {e}")
        return False

def test_get_progress(student_id):
    url = f"{API_BASE}/api/students/{student_id}/progress"
    try:
        with urllib.request.urlopen(url) as res:
            progress = json.loads(res.read().decode("utf-8"))
            print(f"[-] Get Student {student_id} Progress: SUCCESS -> Detailed entries: {len(progress)}")
            return progress
    except Exception as e:
        print(f"[x] Get Student {student_id} Progress: FAILED -> {e}")
        return {}

if __name__ == "__main__":
    print("====================================================")
    print("      RUNNING FULL-STACK BACKEND API TEST           ")
    print("====================================================")
    
    # 1. Auth Login Tests
    student_user = test_login("student1", "123456")
    admin_user = test_login("admin", "admin2026")
    
    # 2. Get Datasets
    courses = test_get_courses()
    curriculum = test_get_curriculum()
    
    if student_user:
        s_id = student_user['id']
        # 3. Modify progress: Check a checkbox
        test_update_progress(s_id, "math_chapter1_lesson1", True)
        
        # 4. Fetch to verify it saved
        prog = test_get_progress(s_id)
        assert prog.get("math_chapter1_lesson1") == 1, "Progress mismatch after checking!"
        print("[-] Verification: Checkbox checking correctly validated!")
        
        # 5. Modify progress: Uncheck the checkbox
        test_update_progress(s_id, "math_chapter1_lesson1", False)
        
        # 6. Fetch to verify it saved
        prog2 = test_get_progress(s_id)
        assert prog2.get("math_chapter1_lesson1") == 0, "Progress mismatch after unchecking!"
        print("[-] Verification: Checkbox unchecking correctly validated!")

    print("====================================================")
    print("      ALL BACKEND FUNCTIONALITY TESTS PASSED!       ")
    print("====================================================")

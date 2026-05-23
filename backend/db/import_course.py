import sqlite3
import json
import os
import sys

# Reconfigure stdout to UTF-8 to handle Vietnamese text cleanly
sys.stdout.reconfigure(encoding='utf-8')

db_path = r"D:\Project\WebLuyenThi\backend\db\database.sqlite"

# Course basic information
course_name = "Khóa nền tảng Toán ĐVĐ"
category = "THPT"
teacher = "Thầy ĐVĐ"
status = "public"
price = "Miễn phí"
image_gradient = "linear-gradient(135deg, #27ae60 0%, #1abc9c 100%)" # Premium green gradient for THPT

# Define standard placeholders
VIDEO_PLACEHOLDER = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
DOC_PLACEHOLDER = "https://example.com/tai-lieu-placeholder.pdf"
HANDWRITTEN_PLACEHOLDER = "https://example.com/ban-viet-tay-placeholder.pdf"

def get_resources(has_video=True, has_doc=True, has_handwritten=True):
    video_url = VIDEO_PLACEHOLDER if has_video else ""
    files = []
    if has_doc:
        files.append({
            "name": "📚 Tài liệu học tập.pdf",
            "url": DOC_PLACEHOLDER
        })
    if has_handwritten:
        files.append({
            "name": "✍️ Bản viết tay bài giảng.pdf",
            "url": HANDWRITTEN_PLACEHOLDER
        })
    return video_url, files

# Define all 11 chapters and their lessons based exactly on the user's screenshots
chapters = {}

# 1. HÌNH HỌC KHÔNG GIAN TOÁN 11
chapters["HÌNH HỌC KHÔNG GIAN TOÁN 11"] = [
    ["BUỔI 1 - KHOẢNG CÁCH TỪ 1 ĐIỂM TỚI 1 MẶT PHẲNG", "Mô tả: BUỔI 1 - KHOẢNG CÁCH TỪ 1 ĐIỂM TỚI 1 MẶT PHẲNG", "High", *get_resources(has_video=True, has_doc=True, has_handwritten=True)],
    ["BUỔI 2 - KĨ NĂNG TÌM GÓC GIỮA 2 MẶT PHẲNG QUA KHOẢNG CÁCH", "Mô tả: BUỔI 2 - KĨ NĂNG TÌM GÓC GIỮA 2 MẶT PHẲNG QUA KHOẢNG CÁCH", "High", *get_resources(has_video=True, has_doc=False, has_handwritten=True)],
    ["BUỔI 3 - KĨ NĂNG TÌM GÓC NHỊ DIỆN QUA KHOẢNG CÁCH", "Mô tả: BUỔI 3 - KĨ NĂNG TÌM GÓC NHỊ DIỆN QUA KHOẢNG CÁCH", "High", *get_resources(has_video=True, has_doc=True, has_handwritten=True)],
    ["BUỔI 4 - NỀN TẢNG VỀ KHOẢNG CÁCH GIỮA HAI ĐƯỜNG THẲNG CHÉO NHAU", "Mô tả: BUỔI 4 - NỀN TẢNG VỀ KHOẢNG CÁCH GIỮA HAI ĐƯỜNG THẲNG CHÉO NHAU", "High", *get_resources(has_video=True, has_doc=True, has_handwritten=False)],
    ["BUỔI 5 - CÔNG THỨC TÍNH NHANH THỂ TÍCH TỨ DIỆN", "Mô tả: BUỔI 5 - CÔNG THỨC TÍNH NHANH THỂ TÍCH TỨ DIỆN", "High", *get_resources(has_video=True, has_doc=False, has_handwritten=False)],
    ["BUỔI 6 - TỈ LỆ THỂ TÍCH", "Mô tả: BUỔI 6 - TỈ LỆ THỂ TÍCH", "High", *get_resources(has_video=True, has_doc=False, has_handwritten=False)],
    ["BUỔI 7 - CÔNG THỨC DKH, SƠ ĐỒ DKH TÍNH KHOẢNG CÁCH", "Mô tả: BUỔI 7 - CÔNG THỨC DKH, SƠ ĐỒ DKH TÍNH KHOẢNG CÁCH", "High", *get_resources(has_video=True, has_doc=True, has_handwritten=True)],
]

# 2. LỘ TRÌNH XÂY NỀN TOÁN 10 11
xn_lessons = [
    ("XN1 - BPT BẬC NHẤT HAI ẨN, HỆ BPT BẬC NHẤT HAI ẨN", True, True, True),
    ("XN2 - HỆ THỨC LƯỢNG TRONG TAM GIÁC", True, True, True),
    ("XN3 - CÁC SỐ ĐẶC TRƯNG CỦA MẪU SỐ LIỆU KHÔNG GHÉP NHÓM", True, True, True),
    ("XN4 - HÀM SỐ BẬC HAI, DẤU CỦA TAM THỨC BẬC HAI", True, True, True),
    ("XN5 - PHƯƠNG TRÌNH ĐƯỜNG THẲNG, ĐƯỜNG TRÒN, GÓC VÀ KHOẢNG CÁCH", True, True, True),
    ("XN6 - BA ĐƯỜNG CONIC (ELIP, HYPEBOL, PARABOL)", True, True, True),
    ("XN7 - CÁC QUY TẮC ĐẾM, HOÁN VỊ, CHỈNH HỢP VÀ TỔ HỢP", True, True, True),
    ("XN8 - NHỊ THỨC NEWTON", True, True, True),
    ("XN9 - BIẾN CỐ VÀ ĐỊNH NGHĨA CỔ ĐIỂN CỦA XÁC SUẤT", True, True, True),
    ("XN10 - ĐƯỜNG TRÒN ĐƠN VỊ, GIÁ TRỊ LƯỢNG GIÁC CỦA GÓC LƯỢNG GIÁC", True, True, True),
    ("XN11 - CÔNG THỨC LƯỢNG GIÁC", True, True, True),
    ("XN12 - HÀM SỐ LƯỢNG GIÁC", True, True, True),
    ("XN13 - PHƯƠNG TRÌNH LƯỢNG GIÁC", True, True, True),
    ("XN14 - DÃY SỐ, CẤP SỐ CỘNG, CẤP SỐ NHÂN", True, True, True),
    ("XN15 - PHÉP LẤY PHẦN BÙ TRONG XÁC SUẤT", True, True, True),
    ("XN16 - CÁC SỐ ĐẶC TRƯNG ĐO XU THẾ TRUNG TÂM CỦA MẪU SỐ LIỆU GHÉP NHÓM", True, True, True),
    ("XN17 - QUAN HỆ SONG SONG TRONG KHÔNG GIAN", True, True, True),
    ("XN18 - GIỚI HẠN", True, True, True),
    ("XN19 - HÀM SỐ LIÊN TỤC", True, True, True),
    ("XN20 - HOÁN VỊ LẶP", True, True, True),
    ("XN21 - PHÉP TÍNH LOGARIT", True, True, True),
    ("XN22 - HÀM SỐ MŨ - HÀM SỐ LOGARIT", True, True, True),
    ("XN23 - PHƯƠNG TRÌNH, BẤT PHƯƠNG TRÌNH MŨ LOGARIT", True, True, True),
    ("XN24 - ĐỊNH NGHĨA VÀ Ý NGHĨA CỦA ĐẠO HÀM", True, False, True), # XN24 lacks doc
]
chapters["LỘ TRÌNH XÂY NỀN TOÁN 10 11"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in xn_lessons
]

# 3. CHƯƠNG 1 - HÀM SỐ
ta_lessons = [
    ("TA1 - NỀN TẢNG VỀ TÍNH ĐƠN ĐIỆU VÀ CỰC TRỊ CỦA HÀM SỐ", True, True, True),
    ("TA2 - NỀN TẢNG VỀ MIN MAX CỦA HÀM SỐ", True, True, True),
    ("TA3 - NỀN TẢNG TIỆM CẬN ĐỒ THỊ HÀM SỐ", True, True, True),
    ("TA4 - CÁC ĐỒ THỊ HÀM SỐ KINH ĐIỂN", True, True, True),
    ("TA5 - PHƯƠNG PHÁP GHÉP TRỤC", True, True, True),
    ("TA6 - MỘT SỐ BÀI TOÁN THỰC TẾ ĐIỂN HÌNH", True, True, True),
    ("TA7 - Tổng ôn hàm số - Bài tập SGK Kết Nối Tri Thức", True, True, True),
    ("TA8 - TỔNG ÔN HÀM SỐ - BÀI TẬP SBT KẾT NỐI", True, True, True),
    ("TA9 - LUYỆN TẬP 23 BÀI TOÁN THỰC TẾ HÀM SỐ CƠ BẢN", True, True, True),
    ("TA10 - MEGALIVE TỔNG ÔN 86 BÀI TOÁN HÀM SỐ", True, True, True),
]
chapters["CHƯƠNG 1 - HÀM SỐ"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in ta_lessons
]

# 4. CHƯƠNG 2 - VECTO TRONG KHÔNG GIAN
tb_lessons = [
    ("TB1 - VECTO TRONG KHÔNG GIAN", True, True, True),
    ("TB2 - TỌA ĐỘ VECTO, BIỂU THỨC TỌA ĐỘ CÁC PHÉP TOÁN VECTO", True, True, True),
    ("TB3 - TÂM TỈ CỰ", True, True, True),
    ("TB4 - Tích có hướng của hai vecto", True, True, True),
    ("TB5 - Tổng ôn tọa độ vecto - SGK Kết Nối", True, True, True),
    ("TB6 - VECTO VẬN TỐC", True, True, True),
    ("TB7 - XÁC ĐỊNH TỌA ĐỘ THEO CÁC HƯỚNG VÀ BÀI TOÁN TỔNG HỢP LỰC", True, True, True),
]
chapters["CHƯƠNG 2 - VECTO TRONG KHÔNG GIAN"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in tb_lessons
]

# 5. CHƯƠNG 3 - CÁC SỐ ĐẶC TRƯNG ĐO MỨC ĐỘ PHÂN TÁN CỦA MẪU SỐ LIỆU GHÉP NHÓM
tc_lessons = [
    ("TC1 - Khoảng biến thiên và khoảng tứ phân vị", True, True, True),
    ("TC2 - Phương sai và độ lệch chuẩn", True, True, True),
    ("TC3 - Bài tập rèn luyện các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm", True, True, True),
]
chapters["CHƯƠNG 3 - CÁC SỐ ĐẶC TRƯNG ĐO MỨC ĐỘ PHÂN TÁN CỦA MẪU SỐ LIỆU GHÉP NHÓM"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in tc_lessons
]

# 6. CHƯƠNG 4 - NGUYÊN HÀM TÍCH PHÂN
td_lessons = [
    ("TD1 - MỞ ĐẦU VỀ NGUYÊN HÀM", True, True, True),
    ("TD2 - MỞ ĐẦU VỀ TÍCH PHÂN", True, True, True),
    ("TD3 - LUYỆN TẬP NGUYÊN HÀM TÍCH PHÂN", True, True, True),
    ("TD4 - ỨNG DỤNG TÍCH PHÂN TÍNH DIỆN TÍCH", True, True, True),
    ("TD5 - ỨNG DỤNG TÍCH PHÂN TÍNH THỂ TÍCH", True, True, True),
    ("TD6 - ỨNG DỤNG TÍCH PHÂN TRONG BÀI TOÁN CHUYỂN ĐỘNG", True, True, True),
    ("TD7 - DIỆN TÍCH CỔNG PARABOL, DIỆN TÍCH CHẢO PARABOL", True, True, True),
]
chapters["CHƯƠNG 4 - NGUYÊN HÀM TÍCH PHÂN"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in td_lessons
]

# 7. CHƯƠNG 5 - OXYZ
te_lessons = [
    ("TE1 - PHƯƠNG TRÌNH MẶT PHẲNG", True, True, True),
    ("TE2 - PHƯƠNG TRÌNH ĐƯỜNG THẲNG", True, True, True),
    ("TE3 - PHƯƠNG TRÌNH MẶT CẦU", True, True, True),
    ("TE4 - VỊ TRÍ TƯƠNG ĐỐI - CHÙM MẶT CẦU", True, True, True),
    ("TE5 - TỌA ĐỘ HÓA GIẢI TOÁN HÌNH HỌC KHÔNG GIAN", True, True, True),
]
chapters["CHƯƠNG 5 - OXYZ"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in te_lessons
]

# 8. CHƯƠNG 6 - MỘT SỐ YẾU TỐ XÁC SUẤT
tf_lessons = [
    ("TF1 - XÁC SUẤT CÓ ĐIỀU KIỆN", True, True, True),
    ("TF2 - CÔNG THỨC XÁC SUẤT TOÀN PHẦN, CÔNG THỨC BAYES", True, True, True),
    ("TF3 - TÍNH XÁC SUẤT BẰNG SƠ ĐỒ CÂY", True, True, True),
    ("TF4 - DI CHUYỂN ĐỒ VẬT TỪ HỘP NÀY SANG HỘP KHÁC", True, True, True),
]
chapters["CHƯƠNG 6 - MỘT SỐ YẾU TỐ XÁC SUẤT"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in tf_lessons
]

# 9. BÀI GIẢNG BỔ TRỢ
bt_lessons = [
    ("BỔ TRỢ 1 - ĐƠN ĐIỆU HÀM BẬC NHẤT TRÊN BẬC NHẤT CÓ THAM SỐ", True, True, False),
    ("BỔ TRỢ 2 - TÌM THAM SỐ M ĐỂ HÀM SỐ ĐƠN ĐIỆU TRÊN KHOẢNG", True, True, False),
    ("BỔ TRỢ 3 - TÍNH ĐƠN ĐIỆU HÀM HỢP, KHÔNG GHÉP TRỤC SƠ ĐỒ V", True, True, False),
    ("BỔ TRỢ 4 - TÌM THAM SỐ M ĐỂ HÀM SỐ ĐẠT CỰC TRỊ TẠI MỘT ĐIỂM NÀO", True, True, False),
    ("BỔ TRỢ 5 - BIỆN LUẬN SỐ ĐIỂM CỰC TRỊ CỦA HÀM F(X) KHI BIẾT THÔNG", True, True, False),
    ("BỔ TRỢ 6 - ĐẾM SỐ ĐIỂM CỰC TRỊ CỦA HÀM HỢP KHI BIẾT THÔNG TIN VỀ", True, True, False),
    ("BỔ TRỢ 7 - CÁC DẠNG TOÁN CÓ THAM SỐ", True, True, False),
    ("BỔ TRỢ 8 - PHƯƠNG PHÁP GHÉP TRỤC", True, True, False),
    ("Bổ trợ 9 - kĩ năng chọn điểm rơi trong bất am-gm", True, True, False),
    ("Bổ trợ 10 - mối quan hệ giữa đạo hàm bậc hai và cực trị hàm bậc ba", True, False, False),
    ("Bổ trợ 11 - xác định hình chiếu của điểm xuống mặt", True, True, False),
    ("Bổ trợ 12 - xác định giao điểm và hình chiếu của đường xuống mặt", True, True, False),
]
chapters["BÀI GIẢNG BỔ TRỢ"] = [
    [title, f"Mô tả: {title}", "Medium", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in bt_lessons
]

# 10. KIỂM TRA KHẢO SÁT CHẤT LƯỢNG
tx_lessons = [
    ("TX1 - Kiểm tra KSCL Toán 12 - Tens 2k8 - Hè 2025 - lần 1", True, True, True),
    ("TX2 - Kiểm tra KSCL Toán 12 - Tens 2k8 - Hè 2025 - lần 2", True, True, True),
    ("TX3 - Kiểm tra KSCL Toán 12 - Tens 2k8 - Hè 2025 - lần 3", True, True, True),
    ("TX4 - Kiểm tra KSCL Toán 12 lần 4 - Hàm số và hình học", True, True, True),
    ("TX5 - ĐỀ KIỂM TRA ĐÁNH GIÁ NĂNG LỰC ĐẦU NĂM", True, True, True),
    ("TX6 - ĐỀ THI THỬ ĐÁNH GIÁ NĂNG LỰC HCM VACT LẦN 1 - EMPIRE", True, True, True),
    ("TX7 - ĐỀ KIỂM TRA ĐÁNH GIÁ NĂNG LỰC ĐẦU NĂM LẦN 2", True, True, True),
    ("TX8 - ĐỀ KIỂM TRA KSCL ĐẦU NĂM MÔN TOÁN + VẬT LÝ 12 (LẦN 1)", True, True, True),
    ("TX9 - ĐỀ KIỂM TRA KSCL ĐẦU NĂM HÀM SỐ VÀ VECTO", True, True, True),
    ("TX10 - ĐỀ KIỂM TRA KSCL ĐẦU NĂM HÀM SỐ VÀ VECTO", True, True, True),
    ("TX11 - ĐỀ THI CHỌN HSG THÀNH PHỐ HÀ NỘI BẢNG A NĂM 2025-2026", True, True, True),
    ("TX12 - ĐỀ THI THỬ GIỮA HỌC KÌ 1 TOÁN 12 - SỐ 01", True, True, True),
    ("TX13 - ĐỀ THI THỬ GIỮA HỌC KÌ 1 TOÁN 12 - SỐ -2", True, True, True),
    ("TX14 - ĐỀ THI THỬ GIỮA HỌC KÌ 1 TOÁN 12 - SỐ 03", True, True, True),
    ("TX15 - ĐỀ THI THỬ GIỮA HỌC KÌ 1 TOÁN 12 - SỐ 04", True, True, True),
]
chapters["KIỂM TRA KHẢO SÁT CHẤT LƯỢNG"] = [
    [title, f"Mô tả: {title}", "High", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in tx_lessons
]

# 11. DẠY LẠI TỪ ĐẦU (Phụ đạo cho bạn mới, em có thể không học)
re_lessons = [
    ("TA3.1 - MỘT SỐ DẠNG TOÁN THỰC TẾ HÀM SỐ", True, False, False),
    ("TA3.2 - TOÁN THỰC TẾ HÀM SỐ", True, True, False),
    ("TA4.1 - NỀN TẢNG VỀ TIỆM CẬN CỦA ĐỒ THỊ HÀM SỐ", True, False, False),
    ("TA4.2 - TIỆM CẬN XIÊN", True, False, False),
    ("TA4.3 - TIỆM CẬN - BÀI TẬP LUYỆN TẬP", True, True, False),
]
chapters["DẠY LẠI TỪ ĐẦU (Phụ đạo cho bạn mới, em có thể không học)"] = [
    [title, f"Mô tả: {title}", "Medium", *get_resources(has_video=v, has_doc=d, has_handwritten=hw)]
    for title, v, d, hw in re_lessons
]

try:
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Check if the course already exists
    cursor.execute("SELECT id FROM courses WHERE name = ? AND category = ?;", (course_name, category))
    row = cursor.fetchone()
    
    if row:
        course_id = row[0]
        print(f"Course '{course_name}' already exists with ID: {course_id}. We will update it.")
        cursor.execute(
            "UPDATE courses SET image = ?, teacher = ?, status = ?, price = ? WHERE id = ?;",
            (image_gradient, teacher, status, price, course_id)
        )
    else:
        print(f"Inserting new course '{course_name}' into courses table...")
        cursor.execute(
            "INSERT INTO courses (image, name, category, teacher, status, price, slug, classin_course_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (image_gradient, course_name, category, teacher, status, price, "khoa-nen-tang-toan-dvd", "")
        )
        course_id = cursor.lastrowid
        print(f"Successfully inserted course with ID: {course_id}")

    # Step 2: Insert / Replace Curriculum Data under subject "course_<id>"
    curriculum_key = f"course_{course_id}"
    curriculum_json = json.dumps(chapters, ensure_ascii=False)
    
    print(f"Saving curriculum chapters to curriculums table under key: '{curriculum_key}'...")
    cursor.execute(
        "INSERT OR REPLACE INTO curriculums (subject, lesson_data) VALUES (?, ?);",
        (curriculum_key, curriculum_json)
    )
    
    conn.commit()
    print("Database transaction successfully committed!")
    
    # Verify records
    cursor.execute("SELECT COUNT(*) FROM courses;")
    total_courses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM curriculums;")
    total_curris = cursor.fetchone()[0]
    
    print(f"\nVerification:")
    print(f"- Total courses in DB: {total_courses}")
    print(f"- Total curriculums in DB: {total_curris}")
    print(f"- Custom course curriculum key in DB: '{curriculum_key}' is active and seeded with {len(chapters)} chapters!")

    conn.close()
except Exception as e:
    print("Error seeding database:", e)
    if 'conn' in locals() and conn:
        conn.rollback()
        conn.close()

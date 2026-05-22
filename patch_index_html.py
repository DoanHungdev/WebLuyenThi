import re

target = r"D:\Project\WebLuyenThi\frontend\index.html"
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Define replacement targets and their replacements

# 1. API Base & Course categories helper
# Let's insert it right after the script tag starts at `<script>`
# To make it safe, we'll replace the first `<script>` after line 6000 or the first `<script>` tag.
# Actually, let's look at the script tag on line 6470.
# The code is:
#   <script>
#     // Course categories dataset for the landing page catalog
#     const courseCategories = {
# Let's replace:
#   <script>
# with:
#   <script>
#     const API_BASE = 'http://localhost:3000';
#     
#     function mapServerCoursesToCategories(serverCourses) {
#       courseCategories.tsa.courses = [];
#       courseCategories.hsa.courses = [];
#       courseCategories.thpt.courses = [];
#       
#       serverCourses.forEach(c => {
#         const cat = c.category.toLowerCase();
#         const mappedCourse = {
#           title: c.name,
#           teacher: c.teacher,
#           icon: cat === 'tsa' ? '🎯' : (cat === 'hsa' ? '📊' : '📚'),
#           bannerColor: c.image && c.image.startsWith('linear-gradient') ? c.image : null,
#           imageUrl: c.image && c.image.startsWith('http') ? c.image : null,
#           link: '#',
#           price: c.price,
#           status: c.status
#         };
#         if (courseCategories[cat]) {
#           courseCategories[cat].courses.push(mappedCourse);
#         } else {
#           courseCategories.hsa.courses.push(mappedCourse);
#         }
#       });
# 
#       Object.keys(courseCategories).forEach(cat => {
#         courseCategories[cat].countText = `${courseCategories[cat].courses.length} khóa học có sẵn`;
#       });
#     }

script_start_target = """  <script>"""
script_start_replacement = """  <script>
    const API_BASE = 'http://localhost:3000';

    function mapServerCoursesToCategories(serverCourses) {
      courseCategories.tsa.courses = [];
      courseCategories.hsa.courses = [];
      courseCategories.thpt.courses = [];
      
      serverCourses.forEach(c => {
        const cat = c.category.toLowerCase();
        const mappedCourse = {
          title: c.name,
          teacher: c.teacher,
          icon: cat === 'tsa' ? '🎯' : (cat === 'hsa' ? '📊' : '📚'),
          bannerColor: c.image && c.image.startsWith('linear-gradient') ? c.image : null,
          imageUrl: c.image && c.image.startsWith('http') ? c.image : null,
          link: '#',
          price: c.price,
          status: c.status
        };
        if (courseCategories[cat]) {
          courseCategories[cat].courses.push(mappedCourse);
        } else {
          courseCategories.hsa.courses.push(mappedCourse);
        }
      });

      Object.keys(courseCategories).forEach(cat => {
        courseCategories[cat].countText = `${courseCategories[cat].courses.length} khóa học có sẵn`;
      });
    }"""

# 2. Overwrite initSystem
init_system_target = """    function initSystem() {

      // Explicitly hide studentDetailModal and youtubePlayerModal on load

      const studentDetailModal = document.getElementById('studentDetailModal');

      if (studentDetailModal) studentDetailModal.style.display = 'none';

      const youtubePlayerModal = document.getElementById('youtubePlayerModal');

      if (youtubePlayerModal) youtubePlayerModal.style.display = 'none';

      // 1. Load active curriculum (HSA) with auto-migration check for old/missing data

      let savedCurriculum = localStorage.getItem('hsa_master_curriculum');

      if (savedCurriculum) {

        try {

          const parsed = JSON.parse(savedCurriculum);

          // If it contains old chapters, or is missing english, force upgrade

          if (

            (parsed.math && parsed.math.chapters && parsed.math.chapters['Hàm Số & Đồ Thị']) ||

            (parsed.literature && parsed.literature.chapters && parsed.literature.chapters['Đọc & Suy luận cơ bản']) ||

            (!parsed.english)

          ) {

            localStorage.removeItem('hsa_master_curriculum');

            savedCurriculum = null;

          }

        } catch (e) {

          savedCurriculum = null;

        }

      }

      if (savedCurriculum) {

        try {

          activeCurriculum = JSON.parse(savedCurriculum);

        } catch (e) {

          activeCurriculum = JSON.parse(JSON.stringify(roadmapData));

        }

      } else {

        activeCurriculum = JSON.parse(JSON.stringify(roadmapData));

        localStorage.setItem('hsa_master_curriculum', JSON.stringify(activeCurriculum));

      }

      // 2. Load active TSA curriculum with auto-migration check for old mock data

      let savedTsaCurriculum = localStorage.getItem('tsa_master_curriculum');

      if (savedTsaCurriculum) {

        try {

          const parsed = JSON.parse(savedTsaCurriculum);

          // If it contains old mock chapters, force overwrite with the authentic new teacher TSA roadmap

          if (parsed.tsa_math && parsed.tsa_math.chapters && parsed.tsa_math.chapters['Đại số và Giải tích']) {

            localStorage.removeItem('tsa_master_curriculum');

            savedTsaCurriculum = null;

          }

        } catch (e) {

          savedTsaCurriculum = null;

        }

      }

      if (savedTsaCurriculum) {

        try {

          activeTsaCurriculum = JSON.parse(savedTsaCurriculum);

        } catch (e) {

          activeTsaCurriculum = JSON.parse(JSON.stringify(tsaRoadmapData));

        }

      } else {

        activeTsaCurriculum = JSON.parse(JSON.stringify(tsaRoadmapData));

        localStorage.setItem('tsa_master_curriculum', JSON.stringify(activeTsaCurriculum));

      }

      // 3. Load exams practice list

      const savedExamsList = localStorage.getItem('exams_practice_list');

      if (savedExamsList) {

        try {

          examsPracticeList = JSON.parse(savedExamsList);

        } catch (e) {

          examsPracticeList = JSON.parse(JSON.stringify(defaultExamsList));

        }

      } else {

        examsPracticeList = JSON.parse(JSON.stringify(defaultExamsList));

        localStorage.setItem('exams_practice_list', JSON.stringify(examsPracticeList));

      }

      // 4. Load users database

      const savedUsers = localStorage.getItem('hsa_users_db');

      if (savedUsers) {

        try {

          usersDb = JSON.parse(savedUsers);

        } catch (e) {

          usersDb = [];

        }

      } else {

        usersDb = [];

        localStorage.setItem('hsa_users_db', JSON.stringify(usersDb));

      }

      // Render default course catalog category

      selectCourseCategory('tsa');

    }"""

init_system_replacement = """    function initSystem() {
      // Explicitly hide studentDetailModal and youtubePlayerModal on load
      const studentDetailModal = document.getElementById('studentDetailModal');
      if (studentDetailModal) studentDetailModal.style.display = 'none';
      const youtubePlayerModal = document.getElementById('youtubePlayerModal');
      if (youtubePlayerModal) youtubePlayerModal.style.display = 'none';

      // 1. Load active curriculum (HSA) with auto-migration check for old/missing data
      let savedCurriculum = localStorage.getItem('hsa_master_curriculum');
      if (savedCurriculum) {
        try {
          const parsed = JSON.parse(savedCurriculum);
          if (
            (parsed.math && parsed.math.chapters && parsed.math.chapters['Hàm Số & Đồ Thị']) ||
            (parsed.literature && parsed.literature.chapters && parsed.literature.chapters['Đọc & Suy luận cơ bản']) ||
            (!parsed.english)
          ) {
            localStorage.removeItem('hsa_master_curriculum');
            savedCurriculum = null;
          }
        } catch (e) {
          savedCurriculum = null;
        }
      }
      if (savedCurriculum) {
        try {
          activeCurriculum = JSON.parse(savedCurriculum);
        } catch (e) {
          activeCurriculum = JSON.parse(JSON.stringify(roadmapData));
        }
      } else {
        activeCurriculum = JSON.parse(JSON.stringify(roadmapData));
        localStorage.setItem('hsa_master_curriculum', JSON.stringify(activeCurriculum));
      }

      // 2. Load active TSA curriculum with auto-migration check for old mock data
      let savedTsaCurriculum = localStorage.getItem('tsa_master_curriculum');
      if (savedTsaCurriculum) {
        try {
          const parsed = JSON.parse(savedTsaCurriculum);
          if (parsed.tsa_math && parsed.tsa_math.chapters && parsed.tsa_math.chapters['Đại số và Giải tích']) {
            localStorage.removeItem('tsa_master_curriculum');
            savedTsaCurriculum = null;
          }
        } catch (e) {
          savedTsaCurriculum = null;
        }
      }
      if (savedTsaCurriculum) {
        try {
          activeTsaCurriculum = JSON.parse(savedTsaCurriculum);
        } catch (e) {
          activeTsaCurriculum = JSON.parse(JSON.stringify(tsaRoadmapData));
        }
      } else {
        activeTsaCurriculum = JSON.parse(JSON.stringify(tsaRoadmapData));
        localStorage.setItem('tsa_master_curriculum', JSON.stringify(activeTsaCurriculum));
      }

      // 3. Load exams practice list
      const savedExamsList = localStorage.getItem('exams_practice_list');
      if (savedExamsList) {
        try {
          examsPracticeList = JSON.parse(savedExamsList);
        } catch (e) {
          examsPracticeList = JSON.parse(JSON.stringify(defaultExamsList));
        }
      } else {
        examsPracticeList = JSON.parse(JSON.stringify(defaultExamsList));
        localStorage.setItem('exams_practice_list', JSON.stringify(examsPracticeList));
      }

      // 4. Load users database
      const savedUsers = localStorage.getItem('hsa_users_db');
      if (savedUsers) {
        try {
          usersDb = JSON.parse(savedUsers);
        } catch (e) {
          usersDb = [];
        }
      } else {
        usersDb = [];
        localStorage.setItem('hsa_users_db', JSON.stringify(usersDb));
      }

      // Render default course catalog category
      selectCourseCategory('tsa');

      // DYNAMIC BACKEND SYNC AND CACHING
      console.log("Contacting Express backend server for active datasets...");
      
      // Sync Curriculums
      fetch(`${API_BASE}/api/curriculum`)
        .then(res => res.json())
        .then(data => {
          if (data && Object.keys(data).length > 0) {
            Object.keys(data).forEach(subject => {
              if (activeCurriculum[subject]) {
                activeCurriculum[subject].chapters = data[subject].chapters || data[subject];
              } else if (activeTsaCurriculum[subject]) {
                activeTsaCurriculum[subject].chapters = data[subject].chapters || data[subject];
              } else {
                activeCurriculum[subject] = data[subject];
              }
            });
            localStorage.setItem('hsa_master_curriculum', JSON.stringify(activeCurriculum));
            localStorage.setItem('tsa_master_curriculum', JSON.stringify(activeTsaCurriculum));
            if (currentUser) {
              renderSheet();
            }
          }
        })
        .catch(err => console.warn("Express backend offline. Running on offline curriculum cache."));

      // Sync Active Course Catalog
      fetch(`${API_BASE}/api/courses`)
        .then(res => res.json())
        .then(courses => {
          if (courses && courses.length > 0) {
            mapServerCoursesToCategories(courses);
            selectCourseCategory(currentSuperView || 'tsa');
          }
        })
        .catch(err => console.warn("Express backend offline. Running on static course catalog."));

      // Sync Registered Users Database
      fetch(`${API_BASE}/api/students`)
        .then(res => res.json())
        .then(students => {
          if (students && students.length > 0) {
            usersDb = students.map(s => ({
              id: s.id,
              username: s.username,
              name: s.fullname,
              className: 'Học viên',
              targetScore: '120',
              role: s.role
            }));
            localStorage.setItem('hsa_users_db', JSON.stringify(usersDb));
          }
        })
        .catch(err => console.warn("Express backend offline. Running on cached student profiles."));
    }"""

# 3. Overwrite loadProgress
load_progress_target = """    function loadProgress() {

      if (!currentUser || currentUser.role === 'admin') return;

      // HSA progress

      const HSA_KEY = `hsa_progress_${currentUser.username}`;

      const savedHsa = localStorage.getItem(HSA_KEY);

      try { progressState = savedHsa ? JSON.parse(savedHsa) : {}; } catch (e) { progressState = {}; }

      // TSA progress

      const TSA_KEY = `tsa_progress_${currentUser.username}`;

      const savedTsa = localStorage.getItem(TSA_KEY);

      try { tsaProgressState = savedTsa ? JSON.parse(savedTsa) : {}; } catch (e) { tsaProgressState = {}; }

      // Exams progress

      const EXAMS_KEY = `exams_progress_${currentUser.username}`;

      const savedExams = localStorage.getItem(EXAMS_KEY);

      try { examsProgressState = savedExams ? JSON.parse(savedExams) : {}; } catch (e) { examsProgressState = {}; }

    }"""

load_progress_replacement = """    function loadProgress() {
      if (!currentUser || currentUser.role === 'admin') return;

      // HSA progress
      const HSA_KEY = `hsa_progress_${currentUser.username}`;
      const savedHsa = localStorage.getItem(HSA_KEY);
      try { progressState = savedHsa ? JSON.parse(savedHsa) : {}; } catch (e) { progressState = {}; }

      // TSA progress
      const TSA_KEY = `tsa_progress_${currentUser.username}`;
      const savedTsa = localStorage.getItem(TSA_KEY);
      try { tsaProgressState = savedTsa ? JSON.parse(savedTsa) : {}; } catch (e) { tsaProgressState = {}; }

      // Exams progress
      const EXAMS_KEY = `exams_progress_${currentUser.username}`;
      const savedExams = localStorage.getItem(EXAMS_KEY);
      try { examsProgressState = savedExams ? JSON.parse(savedExams) : {}; } catch (e) { examsProgressState = {}; }

      // Sync dynamically with backend if user has a valid DB ID
      if (currentUser.id) {
        fetch(`${API_BASE}/api/students/${currentUser.id}/progress`)
          .then(res => res.json())
          .then(progressMap => {
            if (progressMap && Object.keys(progressMap).length > 0) {
              Object.keys(progressMap).forEach(key => {
                const val = progressMap[key] === 1;
                if (key.startsWith('exam_')) {
                  if (!examsProgressState[key]) examsProgressState[key] = {};
                  examsProgressState[key].completed = val;
                } else if (key.startsWith('tsa_')) {
                  tsaProgressState[key] = val;
                } else {
                  progressState[key] = val;
                }
              });
              
              localStorage.setItem(HSA_KEY, JSON.stringify(progressState));
              localStorage.setItem(TSA_KEY, JSON.stringify(tsaProgressState));
              localStorage.setItem(EXAMS_KEY, JSON.stringify(examsProgressState));
              
              updateDashboardStats();
              if (currentSuperView === 'exams') {
                renderExamsSheet();
              } else {
                renderSheet();
              }
            }
          })
          .catch(err => console.warn("Express backend offline. Running on cached progress checkbox records."));
      }
    }"""

# 4. Overwrite submitLogin
submit_login_target = """    window.submitLogin = function (e) {

      e.preventDefault();

      const userEl = document.getElementById('loginUser');

      const passEl = document.getElementById('loginPass');

      const username = userEl.value.trim();

      const password = passEl.value.trim();

      if (!username || !password) return;

      // Check Admin

      if (username.toLowerCase() === 'admin' && password === 'admin2026') {

        const adminUser = {

          username: 'admin',

          name: 'Quản trị viên',

          className: 'Hệ thống',

          targetScore: '150',

          role: 'admin'

        };

        localStorage.setItem('hsa_current_user', JSON.stringify(adminUser));

        userEl.value = '';

        passEl.value = '';

        if (typeof closeAuthModal === 'function') closeAuthModal();

        // Hide home and activate admin

        const homeView = document.getElementById('homeView');

        const adminView = document.getElementById('adminView');

        const coursesView = document.getElementById('coursesView');

        if (homeView) homeView.classList.remove('active');

        if (coursesView) coursesView.classList.remove('active');

        if (adminView) adminView.classList.add('active');

        checkSession();

        return;

      }

      // Check Student

      const student = usersDb.find(u => u.username.toLowerCase() === username.toLowerCase());

      if (student && student.password === password) {

        localStorage.setItem('hsa_current_user', JSON.stringify(student));

        userEl.value = '';

        passEl.value = '';

        if (typeof closeAuthModal === 'function') closeAuthModal();

        // Hide home and activate student view

        const homeView = document.getElementById('homeView');

        const studentView = document.getElementById('studentView');

        const coursesView = document.getElementById('coursesView');

        if (homeView) homeView.classList.remove('active');

        if (coursesView) coursesView.classList.remove('active');

        if (studentView) studentView.classList.add('active');

        checkSession();

      } else {

        alert("Tên đăng nhập hoặc mật khẩu không chính xác!");

      }

    };"""

submit_login_replacement = """    window.submitLogin = function (e) {
      e.preventDefault();
      const userEl = document.getElementById('loginUser');
      const passEl = document.getElementById('loginPass');
      const username = userEl.value.trim();
      const password = passEl.value.trim();

      if (!username || !password) return;

      // Try Express backend validation first
      fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      .then(async res => {
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || "Tài khoản hoặc mật khẩu không chính xác.");
        }
        return res.json();
      })
      .then(resData => {
        const user = resData.user;
        const loggedUser = {
          id: user.id,
          username: user.username,
          name: user.fullname,
          className: user.role === 'admin' ? 'Hệ thống' : 'Học viên',
          targetScore: user.role === 'admin' ? '150' : '120',
          role: user.role
        };
        
        localStorage.setItem('hsa_current_user', JSON.stringify(loggedUser));
        userEl.value = '';
        passEl.value = '';
        if (typeof closeAuthModal === 'function') closeAuthModal();

        const homeView = document.getElementById('homeView');
        const adminView = document.getElementById('adminView');
        const studentView = document.getElementById('studentView');
        const coursesView = document.getElementById('coursesView');

        if (homeView) homeView.classList.remove('active');
        if (coursesView) coursesView.classList.remove('active');

        if (loggedUser.role === 'admin') {
          if (adminView) adminView.classList.add('active');
          if (studentView) studentView.classList.remove('active');
        } else {
          if (studentView) studentView.classList.add('active');
          if (adminView) adminView.classList.remove('active');
        }

        checkSession();
      })
      .catch(err => {
        console.warn("Backend authentication offline, falling back to local storage cache:", err.message);
        
        // Local Fallback validation
        if (username.toLowerCase() === 'admin' && password === 'admin2026') {
          const adminUser = {
            username: 'admin',
            name: 'Quản trị viên',
            className: 'Hệ thống',
            targetScore: '150',
            role: 'admin'
          };
          localStorage.setItem('hsa_current_user', JSON.stringify(adminUser));
          userEl.value = '';
          passEl.value = '';
          if (typeof closeAuthModal === 'function') closeAuthModal();
          const homeView = document.getElementById('homeView');
          const adminView = document.getElementById('adminView');
          const coursesView = document.getElementById('coursesView');
          if (homeView) homeView.classList.remove('active');
          if (coursesView) coursesView.classList.remove('active');
          if (adminView) adminView.classList.add('active');
          checkSession();
          return;
        }

        const student = usersDb.find(u => u.username.toLowerCase() === username.toLowerCase());
        if (student && student.password === password) {
          localStorage.setItem('hsa_current_user', JSON.stringify(student));
          userEl.value = '';
          passEl.value = '';
          if (typeof closeAuthModal === 'function') closeAuthModal();
          const homeView = document.getElementById('homeView');
          const studentView = document.getElementById('studentView');
          const coursesView = document.getElementById('coursesView');
          if (homeView) homeView.classList.remove('active');
          if (coursesView) coursesView.classList.remove('active');
          if (studentView) studentView.classList.add('active');
          checkSession();
        } else {
          alert("Sai tài khoản hoặc mật khẩu (hoặc hệ thống đang offline và chưa lưu cache tài khoản của bạn).");
        }
      });
    };"""

# 5. Overwrite toggleLessonStatus to update server progress dynamically
toggle_lesson_target = """      let state = (currentSuperView === 'tsa') ? tsaProgressState : progressState;

      if (checkbox.checked) {

        state[uniqueId] = true;

        if (row) row.classList.add('row-completed');

      } else {

        state[uniqueId] = false;

        if (row) row.classList.remove('row-completed');

      }

      saveProgress();"""

toggle_lesson_replacement = """      let state = (currentSuperView === 'tsa') ? tsaProgressState : progressState;

      if (checkbox.checked) {

        state[uniqueId] = true;

        if (row) row.classList.add('row-completed');

      } else {

        state[uniqueId] = false;

        if (row) row.classList.remove('row-completed');

      }

      saveProgress();

      // DYNAMIC EXPRESS SYNC
      if (currentUser && currentUser.id) {
        fetch(`${API_BASE}/api/students/${currentUser.id}/progress`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            lessonId: uniqueId,
            statusCompleted: checkbox.checked
          })
        })
        .then(res => res.json())
        .then(resData => console.log(`Checkbox synced with server: ${uniqueId}`))
        .catch(err => console.warn(`Could not sync checkbox ${uniqueId} with server, saved to local cache.`));
      }"""

# 6. Overwrite switchAdminTab to fetch students progress from server
switch_admin_tab_target = """      if (tab === 'students') {

        renderAdminStudents();

        renderAdminStats();

      }"""

switch_admin_tab_replacement = """      if (tab === 'students') {
        if (typeof syncAllStudentsProgressFromServer === 'function') {
          syncAllStudentsProgressFromServer();
        } else {
          renderAdminStudents();
          renderAdminStats();
        }
      }"""

# 7. Add syncAllStudentsProgressFromServer at a safe place, e.g. before switchAdminTab
# Let's search for "window.switchAdminTab = function (tab) {" and prepend the sync function!
switch_admin_func_target = """    window.switchAdminTab = function (tab) {"""
switch_admin_func_replacement = """    async function syncAllStudentsProgressFromServer() {
      try {
        const res = await fetch(`${API_BASE}/api/students`);
        if (!res.ok) throw new Error("Server error");
        const students = await res.json();
        
        // Update local usersDb with dynamic server users
        usersDb = students.map(s => ({
          id: s.id,
          username: s.username,
          name: s.fullname,
          className: 'Học viên',
          targetScore: '120',
          role: s.role
        }));
        localStorage.setItem('hsa_users_db', JSON.stringify(usersDb));

        // Sync detailed progress for all students
        for (const student of students) {
          try {
            const progRes = await fetch(`${API_BASE}/api/students/${student.id}/progress`);
            if (progRes.ok) {
              const progressMap = await progRes.json();
              const hsaState = {};
              const tsaState = {};
              const examsState = {};
              
              Object.keys(progressMap).forEach(key => {
                const val = progressMap[key] === 1;
                if (key.startsWith('exam_')) {
                  examsState[key] = { completed: val };
                } else if (key.startsWith('tsa_')) {
                  tsaState[key] = val;
                } else {
                  hsaState[key] = val;
                }
              });
              
              localStorage.setItem(`hsa_progress_${student.username}`, JSON.stringify(hsaState));
              localStorage.setItem(`tsa_progress_${student.username}`, JSON.stringify(tsaState));
              localStorage.setItem(`exams_progress_${student.username}`, JSON.stringify(examsState));
            }
          } catch (err) {
            console.warn(`Could not sync student ${student.username} progress from backend:`, err);
          }
        }
        
        renderAdminStudents();
        renderAdminStats();
      } catch (e) {
        console.warn("Express backend offline. Running admin panels on local student storage cache.");
        renderAdminStudents();
        renderAdminStats();
      }
    }

    window.switchAdminTab = function (tab) {"""

# 8. Sync saveCurriculumChanges with backend
save_curri_target = """      curr[editingSubject].chapters[editingChapter] = updatedTopics;

      localStorage.setItem(storageKey, JSON.stringify(curr));

      alert(`Đã lưu thành công giáo án gốc chương "${editingChapter}"!`);"""

save_curri_replacement = """      curr[editingSubject].chapters[editingChapter] = updatedTopics;

      localStorage.setItem(storageKey, JSON.stringify(curr));

      // DYNAMIC BACKEND SYNC
      fetch(`${API_BASE}/api/curriculum/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: editingSubject,
          lessonData: curr[editingSubject]
        })
      })
      .then(res => res.json())
      .then(resData => console.log(`Curriculum updated on server for subject: ${editingSubject}`))
      .catch(err => console.warn(`Could not update curriculum on server, cached locally.`));

      alert(`Đã lưu thành công giáo án gốc chương "${editingChapter}"!`);"""

# Perform Replacements
# We will do literal replacements, making sure to replace exactly
# Since some lines contain unique double carriage returns, we must be careful with spacing and whitespace.

targets_replacements = [
    (script_start_target, script_start_replacement),
    (init_system_target, init_system_replacement),
    (load_progress_target, load_progress_replacement),
    (submit_login_target, submit_login_replacement),
    (toggle_lesson_target, toggle_lesson_replacement),
    (switch_admin_tab_target, switch_admin_tab_replacement),
    (switch_admin_func_target, switch_admin_func_replacement),
    (save_curri_target, save_curri_replacement)
]

for idx, (tgt, rep) in enumerate(targets_replacements):
    if tgt in content:
        content = content.replace(tgt, rep)
        print(f"Replacement {idx+1} SUCCESSFUL")
    else:
        print(f"Replacement {idx+1} FAILED!")
        # Let's find substring to debug
        first_line = tgt.split('\n')[0]
        print(f"Looking for first line: '{first_line}'")
        found = content.find(first_line)
        if found != -1:
            print(f"Found match of first line at position {found}!")
        else:
            print("First line not found at all!")

# Save patched file
with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished patching index.html successfully!")

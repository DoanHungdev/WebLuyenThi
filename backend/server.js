const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = 3000;

// Enable CORS for all origins (supports local file:// and localhost)
app.use(cors());
app.use(bodyParser.json({ limit: '10mb' })); // Support large JSON payloads for curriculum data

// Open Database connection
const dbPath = path.join(__dirname, 'db', 'database.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening SQLite database:', err);
  } else {
    console.log('Connected to SQLite database at:', dbPath);
  }
});

// ==========================================
// 1. API XÁC THỰC (AUTHENTICATION)
// ==========================================
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'Vui lòng cung cấp đầy đủ tài khoản và mật khẩu.' });
  }

  db.get('SELECT id, username, fullname, role FROM users WHERE username = ? AND password = ?', [username, password], (err, row) => {
    if (err) {
      console.error('DB error during login:', err);
      return res.status(500).json({ error: 'Lỗi hệ thống cơ sở dữ liệu.' });
    }
    if (row) {
      res.json({ success: true, user: row });
    } else {
      res.status(401).json({ error: 'Tài khoản hoặc mật khẩu không chính xác.' });
    }
  });
});

// ==========================================
// 2. API QUẢN LÝ KHÓA HỌC (COURSES)
// ==========================================
app.get('/api/courses', (req, res) => {
  db.all('SELECT * FROM courses', [], (err, rows) => {
    if (err) {
      console.error('DB error fetching courses:', err);
      return res.status(500).json({ error: 'Không thể tải danh sách khóa học.' });
    }
    res.json(rows);
  });
});

app.post('/api/courses', (req, res) => {
  const { image, name, category, teacher, status, price, slug, classin_course_id } = req.body;
  if (!name || !category || !teacher || !status || !price) {
    return res.status(400).json({ error: 'Thiếu thông tin bắt buộc để tạo khóa học.' });
  }

  db.run(
    'INSERT INTO courses (image, name, category, teacher, status, price, slug, classin_course_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
    [image || '', name, category, teacher, status, price, slug || '', classin_course_id || ''],
    function (err) {
      if (err) {
        console.error('DB error inserting course:', err);
        return res.status(500).json({ error: 'Không thể thêm khóa học.' });
      }
      res.status(201).json({ success: true, courseId: this.lastID });
    }
  );
});

app.put('/api/courses/:id', (req, res) => {
  const { id } = req.params;
  const { image, name, category, teacher, status, price, slug, classin_course_id } = req.body;
  if (!name || !category || !teacher || !status || !price) {
    return res.status(400).json({ error: 'Thiếu thông tin bắt buộc để cập nhật khóa học.' });
  }

  db.run(
    'UPDATE courses SET image = ?, name = ?, category = ?, teacher = ?, status = ?, price = ?, slug = ?, classin_course_id = ? WHERE id = ?',
    [image || '', name, category, teacher, status, price, slug || '', classin_course_id || '', id],
    function (err) {
      if (err) {
        console.error('DB error updating course:', err);
        return res.status(500).json({ error: 'Không thể cập nhật khóa học.' });
      }
      if (this.changes === 0) {
        return res.status(404).json({ error: 'Không tìm thấy khóa học để cập nhật.' });
      }
      res.json({ success: true });
    }
  );
});

app.delete('/api/courses/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM courses WHERE id = ?', [id], function (err) {
    if (err) {
      console.error('DB error deleting course:', err);
      return res.status(500).json({ error: 'Không thể xóa khóa học.' });
    }
    if (this.changes === 0) {
      return res.status(404).json({ error: 'Không tìm thấy khóa học.' });
    }
    res.json({ success: true });
  });
});

// ==========================================
// 3. API TIẾN ĐỘ HỌC SINH (STUDENT PROGRESS)
// ==========================================
// Lấy danh sách học sinh kèm số bài đã hoàn thành
app.get('/api/students', (req, res) => {
  const query = `
    SELECT u.id, u.username, u.password, u.fullname, u.role, 
           COUNT(CASE WHEN sp.status_completed = 1 THEN 1 END) as completedCount
    FROM users u
    LEFT JOIN student_progress sp ON u.id = sp.student_id
    WHERE u.role = 'student'
    GROUP BY u.id
  `;
  
  db.all(query, [], (err, rows) => {
    if (err) {
      console.error('DB error fetching students:', err);
      return res.status(500).json({ error: 'Không thể tải danh sách học sinh.' });
    }
    res.json(rows);
  });
});

// Lấy tiến độ chi tiết của một học sinh cụ thể
app.get('/api/students/:id/progress', (req, res) => {
  const { id } = req.params;
  db.all('SELECT lesson_id, status_completed, updated_at FROM student_progress WHERE student_id = ?', [id], (err, rows) => {
    if (err) {
      console.error('DB error fetching progress:', err);
      return res.status(500).json({ error: 'Không thể tải tiến trình học sinh.' });
    }
    // Convert to a dictionary for fast client-side lookups: { lesson_id: status_completed }
    const progressMap = {};
    rows.forEach(r => {
      progressMap[r.lesson_id] = r.status_completed;
    });
    res.json(progressMap);
  });
});

// Cập nhật tiến độ của học sinh
app.post('/api/students/:id/progress', (req, res) => {
  const { id } = req.params;
  const { lessonId, statusCompleted } = req.body;
  if (!lessonId) {
    return res.status(400).json({ error: 'Thiếu thông tin bài học.' });
  }

  const status = statusCompleted ? 1 : 0;
  const query = `
    INSERT INTO student_progress (student_id, lesson_id, status_completed, updated_at)
    VALUES (?, ?, ?, datetime('now'))
    ON CONFLICT(student_id, lesson_id) DO UPDATE SET
      status_completed = excluded.status_completed,
      updated_at = datetime('now')
  `;

  db.run(query, [id, lessonId, status], function (err) {
    if (err) {
      console.error('DB error updating progress:', err);
      return res.status(500).json({ error: 'Không thể lưu tiến độ học tập.' });
    }
    res.json({ success: true });
  });
});

// Admin API: Tạo mới học sinh
app.post('/api/students', (req, res) => {
  const { username, password, fullname } = req.body;
  if (!username || !password || !fullname) {
    return res.status(400).json({ error: 'Thiếu thông tin bắt buộc.' });
  }
  db.run(
    'INSERT INTO users (username, password, fullname, role) VALUES (?, ?, ?, "student")',
    [username, password, fullname],
    function (err) {
      if (err) {
        console.error('DB error creating student:', err);
        return res.status(500).json({ error: 'Không thể tạo học sinh. Tên đăng nhập có thể đã tồn tại.' });
      }
      res.status(201).json({ success: true, studentId: this.lastID });
    }
  );
});

// Admin API: Cập nhật thông tin học sinh
app.put('/api/students/:id', (req, res) => {
  const { id } = req.params;
  const { username, password, fullname } = req.body;
  if (!username || !password || !fullname) {
    return res.status(400).json({ error: 'Thiếu thông tin bắt buộc.' });
  }
  db.run(
    'UPDATE users SET username = ?, password = ?, fullname = ? WHERE id = ?',
    [username, password, fullname, id],
    function (err) {
      if (err) {
        console.error('DB error updating student:', err);
        return res.status(500).json({ error: 'Không thể cập nhật thông tin học sinh.' });
      }
      res.json({ success: true });
    }
  );
});

// Admin API: Xóa học sinh
app.delete('/api/students/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM users WHERE id = ?', [id], function (err) {
    if (err) {
      console.error('DB error deleting student:', err);
      return res.status(500).json({ error: 'Lỗi xóa tài khoản học sinh.' });
    }
    res.json({ success: true });
  });
});

// Client API: Đăng ký tài khoản mới (Signup)
app.post('/api/auth/signup', (req, res) => {
  const { username, password, fullname } = req.body;
  if (!username || !password || !fullname) {
    return res.status(400).json({ error: 'Thiếu thông tin bắt buộc.' });
  }
  db.run(
    'INSERT INTO users (username, password, fullname, role) VALUES (?, ?, ?, "student")',
    [username, password, fullname],
    function (err) {
      if (err) {
        console.error('DB error during signup:', err);
        return res.status(400).json({ error: 'Tên đăng nhập đã tồn tại.' });
      }
      res.status(201).json({ success: true, userId: this.lastID });
    }
  );
});

// ==========================================
// 4. API GIÁO ÁN GỐC (CURRICULUMS)
// ==========================================
app.get('/api/curriculum', (req, res) => {
  db.all('SELECT * FROM curriculums', [], (err, rows) => {
    if (err) {
      console.error('DB error fetching curriculum:', err);
      return res.status(500).json({ error: 'Không thể tải giáo án gốc.' });
    }
    // Return key-value object: { subject: lesson_data }
    const curriMap = {};
    rows.forEach(row => {
      try {
        curriMap[row.subject] = JSON.parse(row.lesson_data);
      } catch (e) {
        curriMap[row.subject] = row.lesson_data;
      }
    });
    res.json(curriMap);
  });
});

app.post('/api/curriculum/update', (req, res) => {
  const { subject, lessonData } = req.body;
  if (!subject || !lessonData) {
    return res.status(400).json({ error: 'Thiếu thông tin môn học hoặc nội dung giáo án.' });
  }

  const lessonDataStr = typeof lessonData === 'object' ? JSON.stringify(lessonData) : lessonData;

  db.run(
    'INSERT OR REPLACE INTO curriculums (subject, lesson_data) VALUES (?, ?)',
    [subject, lessonDataStr],
    function (err) {
      if (err) {
        console.error('DB error updating curriculum:', err);
        return res.status(500).json({ error: 'Không thể lưu chỉnh sửa giáo án gốc.' });
      }
      res.json({ success: true });
    }
  );
});

// Start Express Server
app.listen(PORT, () => {
  console.log(`==================================================`);
  console.log(`   SKIBIDI STUDY SERVER IS RUNNING ON PORT ${PORT}`);
  console.log(`   API endpoints available at http://localhost:${PORT}`);
  console.log(`==================================================`);
});

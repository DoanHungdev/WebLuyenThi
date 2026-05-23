const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, 'db', 'database.sqlite');

// Ensure db directory exists
const dbDir = path.dirname(dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

// Delete existing db if it failed mid-way to start fresh
if (fs.existsSync(dbPath)) {
  try {
    fs.unlinkSync(dbPath);
  } catch (e) {}
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err);
    process.exit(1);
  }
  console.log('Connected to SQLite database.');
});

db.serialize(() => {
  // 1. Create tables
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      fullname TEXT NOT NULL,
      role TEXT NOT NULL
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS courses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      image TEXT,
      name TEXT NOT NULL,
      category TEXT NOT NULL,
      teacher TEXT NOT NULL,
      status TEXT NOT NULL,
      price TEXT NOT NULL,
      slug TEXT,
      classin_course_id TEXT
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS curriculums (
      subject TEXT PRIMARY KEY,
      lesson_data TEXT NOT NULL
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS student_progress (
      student_id INTEGER NOT NULL,
      lesson_id TEXT NOT NULL,
      status_completed INTEGER DEFAULT 0,
      updated_at TEXT,
      PRIMARY KEY (student_id, lesson_id),
      FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
    )
  `);

  console.log('Tables created successfully.');

  // 2. Insert default users (Admin & Students)
  const defaultUsers = [
    { username: 'admin', password: 'admin2026', fullname: 'Doãn Hưng', role: 'admin' },
    { username: 'student1', password: '123456', fullname: 'Nguyễn Văn A', role: 'student' },
    { username: 'student2', password: '123456', fullname: 'Trần Thị B', role: 'student' }
  ];

  const insertUser = db.prepare('INSERT OR IGNORE INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)');
  defaultUsers.forEach(u => {
    insertUser.run(u.username, u.password, u.fullname, u.role);
  });
  insertUser.finalize();
  console.log('Default users seeded.');

  // 3. Import seed curriculums from JSON file
  const seedCurriculumPath = path.join(__dirname, 'db', 'all_curriculums.json');
  if (fs.existsSync(seedCurriculumPath)) {
    try {
      const rawData = fs.readFileSync(seedCurriculumPath, 'utf8');
      const curriculums = JSON.parse(rawData);
      
      const insertCurriculum = db.prepare('INSERT OR REPLACE INTO curriculums (subject, lesson_data) VALUES (?, ?)');
      Object.keys(curriculums).forEach(subject => {
        insertCurriculum.run(subject, JSON.stringify(curriculums[subject]));
        console.log(`Seeded curriculum for subject: ${subject}`);
      });
      insertCurriculum.finalize();
      console.log('Curriculums successfully imported into SQLite.');
    } catch (e) {
      console.error('Error importing curriculums:', e);
    }
  } else {
    console.warn('Seed curriculums JSON not found.');
  }

  // 4. Insert default courses and then close the DB
  const defaultCourses = [
    {
      image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500',
      name: 'Khóa Chuyên Sâu HSA - Đánh giá năng lực ĐHQGHN',
      category: 'HSA',
      teacher: 'Thầy Doãn Hưng & Đội ngũ Chuyên gia',
      status: 'Đang mở',
      price: '1.600.000đ'
    },
    {
      image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500',
      name: 'Bứt Phá Điểm Số TSA - Đánh giá tư duy ĐHBKHN',
      category: 'TSA',
      teacher: 'Cô Mai Phương & Thầy Hưng',
      status: 'Đang mở',
      price: '1.200.000đ'
    },
    {
      image: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500',
      name: 'Combo 80+ HSA & TSA Toàn Diện 2026',
      category: 'Combo',
      teacher: 'Tập thể Giáo viên Hệ thống',
      status: 'Đang mở',
      price: '2.800.000đ'
    },
    {
      image: 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=500',
      name: 'Chuyên đề Ngữ Văn chinh phục Đọc hiểu HSA',
      category: 'HSA',
      teacher: 'Cô Doãn Quỳnh',
      status: 'Sắp mở',
      price: '600.000đ'
    },
    {
      image: 'linear-gradient(135deg, #27ae60 0%, #1abc9c 100%)',
      name: 'Khóa nền tảng Toán ĐVĐ',
      category: 'THPT',
      teacher: 'Thầy ĐVĐ',
      status: 'public',
      price: 'Miễn phí'
    },
    {
      image: 'linear-gradient(135deg, #722ed1 0%, #1890ff 100%)',
      name: 'Lộ trình ôn thi HSA',
      category: 'lotrinh',
      teacher: 'SKIBIDI',
      status: 'public',
      price: 'Miễn phí'
    },
    {
      image: 'linear-gradient(135deg, #722ed1 0%, #1890ff 100%)',
      name: 'Lộ trình ôn thi TSA',
      category: 'lotrinh',
      teacher: 'skibidi',
      status: 'public',
      price: 'Miễn phí'
    }
  ];

  db.get('SELECT COUNT(*) as count FROM courses', (err, row) => {
    if (err) {
      console.error('Error checking courses:', err);
      db.close();
      return;
    }
    
    if (row && row.count === 0) {
      const insertCourse = db.prepare('INSERT INTO courses (image, name, category, teacher, status, price) VALUES (?, ?, ?, ?, ?, ?)');
      defaultCourses.forEach(c => {
        insertCourse.run(c.image, c.name, c.category, c.teacher, c.status, c.price);
      });
      insertCourse.finalize(() => {
        console.log('Default courses seeded.');
        db.close(() => {
          console.log('Database initialization completed successfully.');
        });
      });
    } else {
      console.log('Courses table already has data, skipping seed.');
      db.close(() => {
        console.log('Database initialization completed successfully.');
      });
    }
  });
});

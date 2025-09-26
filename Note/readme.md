# English Learning App - Database Structure

## Overview

Cấu trúc database được thiết kế để hỗ trợ đầy đủ các tính năng của ứng dụng học tiếng Anh:

### 🏗️ Core Architecture

#### **1. User Management**
- **users**: Thông tin cơ bản, level, streak, progress
- **user_preferences**: Cài đặt cá nhân hóa
- **user_settings**: Preferences cho từng module

#### **2. Course System**
- **courses**: Khóa học với metadata đầy đủ
- **course_modules**: Chia nhỏ khóa học thành modules
- **lessons**: Bài học chi tiết với nội dung
- **user_course_enrollments**: Theo dõi tiến độ học
- **user_lesson_progress**: Progress chi tiết từng bài

#### **3. Flashcard System với Spaced Repetition**
- **flashcard_decks**: Bộ thẻ học với categories
- **flashcards**: Chi tiết từng thẻ (word, definition, examples, audio)
- **user_flashcard_progress**: Áp dụng thuật toán SM-2 cho spaced repetition
  - `ease_factor`: Độ khó cá nhân
  - `interval_days`: Khoảng cách review
  - `next_review_date`: Ngày review tiếp theo

#### **4. YouTube Shadowing System**
- **youtube_videos**: Metadata video từ YouTube API
- **video_subtitles**: Subtitles được segment hóa
- **user_shadowing_sessions**: Session practice với metrics
- **user_segment_attempts**: Chi tiết từng đoạn luyện tập

#### **5. Practice & Exercise System**
- **practice_exercises**: Bài tập đa dạng (grammar, vocab, listening...)
- **user_exercise_attempts**: Kết quả và feedback

#### **6. Community Features**
- **community_posts**: Bài viết, Q&A, tips
- **community_comments**: Hệ thống comment có nested replies
- **community_likes**: Like/reaction system

#### **7. Gamification**
- **achievement_types**: Định nghĩa các achievement
- **user_achievements**: Progress và completed achievements
- **daily_study_stats**: Thống kê học tập hàng ngày

### 🔄 Key Algorithms Supported

#### **Spaced Repetition (SM-2)**
```sql
-- Cập nhật interval cho flashcard review
UPDATE user_flashcard_progress 
SET 
  ease_factor = CASE 
    WHEN rating >= 3 THEN GREATEST(1.3, ease_factor + (0.1 - (5-rating) * (0.08 + (5-rating) * 0.02)))
    ELSE GREATEST(1.3, ease_factor - 0.2)
  END,
  interval_days = CASE 
    WHEN rating < 3 THEN 1
    WHEN repetitions = 0 THEN 1
    WHEN repetitions = 1 THEN 6
    ELSE ROUND(interval_days * ease_factor)
  END,
  next_review_date = DATE_ADD(CURDATE(), INTERVAL interval_days DAY)
WHERE user_id = ? AND flashcard_id = ?
```

#### **Progress Tracking**
```sql
-- Tính progress percentage cho course
SELECT 
  (COUNT(CASE WHEN ulp.status = 'completed' THEN 1 END) * 100.0 / COUNT(*)) as progress_percentage
FROM lessons l 
JOIN course_modules cm ON l.module_id = cm.id
LEFT JOIN user_lesson_progress ulp ON l.id = ulp.lesson_id AND ulp.user_id = ?
WHERE cm.course_id = ?
```

### 📊 Analytics & Reporting

#### **Daily Stats Collection**
```sql
-- Tự động cập nhật daily stats
INSERT INTO daily_study_stats (user_id, study_date, total_minutes, flashcards_reviewed, words_learned)
SELECT 
  user_id,
  CURDATE(),
  SUM(session_duration),
  COUNT(flashcard_reviews),
  COUNT(DISTINCT new_words)
FROM user_activities 
WHERE DATE(created_at) = CURDATE()
GROUP BY user_id
ON DUPLICATE KEY UPDATE 
  total_minutes = VALUES(total_minutes),
  flashcards_reviewed = VALUES(flashcards_reviewed)
```

### 🔍 Performance Optimization

#### **Strategic Indexes**
- User lookup: `email`, `username`
- Progress tracking: `(user_id, course_id)`, `(user_id, lesson_id)`
- Spaced repetition: `(user_id, next_review_date, status)`
- Content delivery: `(course_id, order_index)`, `(deck_id, difficulty)`

#### **Partitioning Strategy**
```sql
-- Partition daily_study_stats by month
ALTER TABLE daily_study_stats 
PARTITION BY RANGE (TO_DAYS(study_date)) (
  PARTITION p202401 VALUES LESS THAN (TO_DAYS('2024-02-01')),
  PARTITION p202402 VALUES LESS THAN (TO_DAYS('2024-03-01')),
  -- ... continuing monthly partitions
);
```

### 🚀 Scalability Considerations

#### **Read Replicas**
- Separate read operations (progress, statistics) to replicas
- Write operations (progress updates) to master

#### **Caching Strategy**
- Redis cache for:
  - User session data
  - Daily review cards
  - Course progress summaries
  - Community post counts

#### **Data Archival**
```sql
-- Archive old study sessions (>1 year)
CREATE TABLE user_shadowing_sessions_archive LIKE user_shadowing_sessions;

-- Monthly archival job
INSERT INTO user_shadowing_sessions_archive 
SELECT * FROM user_shadowing_sessions 
WHERE started_at < DATE_SUB(CURDATE(), INTERVAL 1 YEAR);
```

### 🔧 Maintenance Procedures

#### **Daily Tasks**
- Update user streaks
- Calculate spaced repetition schedules  
- Generate analytics summaries
- Clean up expired sessions

#### **Weekly Tasks**
- Recompute course ratings
- Update achievement progress
- Community content moderation
- Performance index analysis

#### **Monthly Tasks**
- Archive old data
- User engagement reports
- Course completion analytics
- System performance review

### 📱 Mobile App Support

Database structure fully supports mobile app requirements:
- Offline sync capabilities via `updated_at` timestamps
- Incremental data loading
- Conflict resolution for progress updates
- Efficient pagination for content lists

### 🔒 Security Features

- Password hashing with salt
- Input validation at database level
- Row-level security for user data
- Audit trails for sensitive operations
- Rate limiting support via tracking tables

This database design provides a solid foundation for a comprehensive English learning platform with room for future expansion and optimization.
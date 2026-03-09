# Hướng Dẫn Thêm Model Mới

## Tự Động Tạo Bảng Khi Thêm Model

Hệ thống tự động phát hiện và tạo bảng mới khi bạn thêm model vào `models/__init__.py`

## Ví Dụ: Thêm Model "Department"

### Bước 1: Thêm Model vào `models/__init__.py`

```python
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', backref='managed_department', foreign_keys=[manager_id])
    
    def __repr__(self):
        return f'<Department {self.name}>'
```

### Bước 2: Chạy App hoặc Auto Setup

**Cách 1: Chạy app (tự động)**
```bash
python app.py
```

**Cách 2: Chạy setup script**
```bash
python auto_setup_db.py
```

**Kết quả:**
```
🆕 New tables created: departments
✓ All tables created/verified successfully!

📊 Database Schema:
   ✓ departments (Department)
   ✓ meal_registrations (MealRegistration)
   ✓ overtime_requests (OvertimeRequest)
   ✓ users (User)
```

### Bước 3: Tạo Form (Nếu Cần)

`forms.py`:
```python
class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Department Code', validators=[DataRequired(), Length(max=20)])
    manager_id = SelectField('Manager', coerce=int)
    description = TextAreaField('Description')
```

### Bước 4: Tạo Routes (Nếu Cần)

`app.py`:
```python
@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    form = DepartmentForm()
    
    if form.validate_on_submit():
        dept = Department(
            name=form.name.data,
            code=form.code.data,
            manager_id=form.manager_id.data,
            description=form.description.data
        )
        db.session.add(dept)
        db.session.commit()
        flash('Department created successfully!', 'success')
        return redirect(url_for('departments'))
    
    departments = Department.query.all()
    return render_template('departments.html', form=form, departments=departments)
```

### Bước 5: Thêm vào Admin Panel (Tùy Chọn)

`app.py`:
```python
from models import Department

admin.add_view(ModelView(Department, db.session))
```

## Ví Dụ Khác: Model "Attendance" (Chấm Công)

```python
class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    status = db.Column(db.String(20), default='present')  # present, absent, late, leave
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='attendances')
    
    def __repr__(self):
        return f'<Attendance {self.user_id} - {self.date}>'
```

Chỉ cần thêm vào `models/__init__.py` và chạy app → Bảng tự động được tạo!

## Ví Dụ: Model "Leave Request" (Nghỉ Phép)

```python
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # annual, sick, unpaid
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='leave_requests')
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} - {self.status}>'
```

## Best Practices

### 1. Naming Conventions

```python
# Table names: lowercase, plural, snake_case
__tablename__ = 'leave_requests'

# Column names: lowercase, snake_case
created_at = db.Column(...)

# Class names: PascalCase, singular
class LeaveRequest(db.Model):
```

### 2. Always Add Timestamps

```python
created_at = db.Column(db.DateTime, default=datetime.utcnow)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 3. Use Foreign Keys Properly

```python
# Define foreign key
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# Define relationship
user = db.relationship('User', backref='items')
```

### 4. Add Indexes for Performance

```python
class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    
    # Composite index
    __table_args__ = (
        db.Index('idx_user_date', 'user_id', 'date'),
    )
```

### 5. Add Validation

```python
from sqlalchemy.orm import validates

class Department(db.Model):
    code = db.Column(db.String(20), unique=True, nullable=False)
    
    @validates('code')
    def validate_code(self, key, code):
        if not code.isupper():
            raise ValueError('Department code must be uppercase')
        return code
```

## Migration vs Auto-Create

### Auto-Create (Hiện tại)
✅ Đơn giản, tự động
✅ Phù hợp cho development
❌ Không track changes
❌ Không thể rollback

### Flask-Migrate (Khuyến nghị cho Production)
✅ Track tất cả changes
✅ Có thể rollback
✅ Team collaboration tốt hơn
❌ Phức tạp hơn

**Sử dụng Flask-Migrate:**
```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Add Department model"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

## Kiểm Tra Tables Đã Tạo

```bash
# MySQL command line
mysql -h 10.216.28.11 -u ovnm -p db_hr -e "SHOW TABLES;"

# Python script
python -c "from auto_setup_db import get_existing_tables; print(get_existing_tables())"
```

## Troubleshooting

### Bảng không được tạo tự động?

1. **Kiểm tra model có trong `models/__init__.py`**
2. **Restart app**
3. **Chạy manual**: `python auto_setup_db.py`
4. **Check logs** cho errors

### Lỗi Foreign Key?

```python
# Đảm bảo referenced table tồn tại trước
# Hoặc dùng string reference
user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
```

### Muốn xóa bảng cũ?

```python
# CẢNH BÁO: Mất dữ liệu!
with app.app_context():
    db.drop_all()  # Xóa tất cả
    db.create_all()  # Tạo lại
```

## Example: Complete New Feature

Thêm tính năng "Announcements" (Thông báo):

**1. Model:**
```python
class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_active = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    author = db.relationship('User', backref='announcements')
```

**2. Form:**
```python
class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ])
    expires_at = DateField('Expires At', format='%Y-%m-%d')
```

**3. Route:**
```python
@app.route('/announcements')
@login_required
def announcements():
    announcements = Announcement.query.filter_by(is_active=True).order_by(
        Announcement.published_at.desc()
    ).all()
    return render_template('announcements.html', announcements=announcements)
```

**4. Chạy app → Bảng tự động tạo!**

---

**Kết luận**: Chỉ cần thêm model vào `models/__init__.py`, hệ thống tự động tạo bảng khi chạy app hoặc setup script!

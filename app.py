from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from models import db, User, OvertimeRequest, MealRegistration
from config import Config
from translations import get_translation
from forms import LoginForm, RegisterForm, OvertimeForm, ChangePasswordForm

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Disable template caching for development
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize JWT
jwt = JWTManager(app)

# Register API Blueprint
from api import api_bp
app.register_blueprint(api_bp)

# Initialize Flask-Admin
admin = Admin(app, name='OKI HR Admin', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(OvertimeRequest, db.session))
admin.add_view(ModelView(MealRegistration, db.session))

# Auto-create database and tables on first run
def init_database():
    """
    Initialize database and tables if they don't exist
    Automatically detects and creates new tables when models are added
    """
    try:
        with app.app_context():
            # Get existing tables before creation
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Create all tables (SQLAlchemy automatically detects all models)
            db.create_all()
            
            # Get tables after creation to see what's new
            inspector = db.inspect(db.engine)
            current_tables = inspector.get_table_names()
            new_tables = set(current_tables) - set(existing_tables)
            
            if new_tables:
                print(f"🆕 New tables created: {', '.join(new_tables)}")
            
            # Initialize default positions if positions table is new
            if 'positions' in new_tables or 'positions' not in existing_tables:
                from models import Position
                if Position.query.count() == 0:
                    print("Creating default positions...")
                    default_positions = [
                        {'code': '1', 'name': 'Nhân viên'},
                        {'code': '2', 'name': 'Công nhân'},
                        {'code': '3', 'name': 'Trưởng phòng'},
                        {'code': '4', 'name': 'Phó phòng'},
                        {'code': '5', 'name': 'Giám sát'},
                        {'code': '6', 'name': 'Trưởng nhóm'},
                        {'code': '7', 'name': 'Quản lý'},
                    ]
                    for pos_data in default_positions:
                        position = Position(**pos_data)
                        db.session.add(position)
                    db.session.commit()
                    print("✓ Default positions created")
            
            # Check if we need to create default users
            if User.query.count() == 0:
                print("Creating default users...")
                admin = User(
                    employee_id='ADMIN',
                    name='Administrator',
                    email='admin@okivietnam.com',
                    password=generate_password_hash('admin123'),
                    department='IT',
                    role='admin'
                )
                sample_user = User(
                    employee_id='EMP001',
                    name='Nguyen Van A',
                    email='nguyenvana@okivietnam.com',
                    password=generate_password_hash('password123'),
                    department='production',
                    role='user'
                )
                db.session.add(admin)
                db.session.add(sample_user)
                db.session.commit()
                print("✓ Default users created")
    except Exception as e:
        print(f"Database initialization: {e}")

# Initialize database on startup
init_database()

# Print configuration on startup (for debugging)
if app.config['DEBUG']:
    Config.print_config()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Auto logout middleware - check last activity
@app.before_request
def check_user_activity():
    """Check if user should be logged out due to inactivity"""
    if current_user.is_authenticated:
        # Skip for static files, API endpoints, and logout
        if request.endpoint and (
            request.endpoint.startswith('static') or 
            request.endpoint.startswith('api') or 
            request.endpoint == 'logout'
        ):
            return
        
        # Check last activity
        if current_user.last_activity:
            inactive_duration = datetime.utcnow() - current_user.last_activity
            max_inactive = timedelta(seconds=app.config['AUTO_LOGOUT_DURATION'])
            
            if inactive_duration > max_inactive:
                logout_user()
                session.clear()
                flash('Bạn đã bị đăng xuất do không hoạt động trong 3 tuần', 'warning')
                return redirect(url_for('login'))
        
        # Update last activity
        try:
            current_user.last_activity = datetime.utcnow()
            db.session.commit()
        except:
            db.session.rollback()

# Language middleware
@app.before_request
def set_language():
    if 'lang' not in session:
        session['lang'] = 'vi'  # Default language

@app.context_processor
def inject_translations():
    """Inject translations into all templates"""
    lang = session.get('lang', 'vi')
    
    # Check if user is a manager (has subordinates based on level)
    is_manager = False
    if current_user.is_authenticated:
        # New level-based system: user is manager if they have subordinates
        is_manager = current_user.is_manager() or current_user.role == 'admin'
    
    return dict(t=get_translation(lang), current_lang=lang, is_manager=is_manager)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/set-language/<lang>')
def set_language_route(lang):
    """Thay đổi ngôn ngữ"""
    if lang in ['vi', 'en', 'ja']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(employee_id=form.employee_id.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # Check if account is active
            if not user.is_active:
                flash('Tài khoản của bạn đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên.', 'error')
                return render_template('login.html', form=form)
            
            # Update last activity on login
            user.last_activity = datetime.utcnow()
            db.session.commit()
            
            # Login user with remember me for 3 weeks
            login_user(user, remember=True, duration=timedelta(weeks=3))
            session['user_name'] = user.name
            session.permanent = True  # Make session permanent (3 weeks)
            
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid employee ID or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            employee_id=form.employee_id.data,
            name=form.name.data,
            email=form.email.data,
            department=form.department.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        
        if not identifier:
            flash('Please provide your email or employee ID', 'error')
            return render_template('forgot_password.html')
        
        # TODO: Send reset email
        flash('Password reset instructions have been sent to your email', 'success')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Check if admin
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # Check if user can approve (Trưởng Phòng or has subordinates)
    is_manager = False
    
    # Position code 1 = Trưởng Phòng = can approve
    if current_user.position == '1':
        is_manager = True
    # Or if user has subordinates
    elif current_user.is_manager():
        is_manager = True
    
    return render_template('dashboard.html', user=current_user.name, is_manager=is_manager)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Only admin can access
    if current_user.role != 'admin':
        flash('You do not have permission to access this page', 'error')
        return render_template('dashboard.html', user=current_user.name)
    
    # Calculate stats - exclude resigned users
    total_users = User.query.filter(User.work_status != 'resigned').count()
    working_users = User.query.filter(User.work_status == 'working').count()
    business_trip_users = User.query.filter(User.work_status == 'business_trip').count()
    
    # Calculate overtime stats for today
    from datetime import date
    today = date.today()
    
    today_overtime = OvertimeRequest.query.filter(
        OvertimeRequest.overtime_date == today,
        OvertimeRequest.status == 'approved'
    ).all()
    
    overtime_count = len(today_overtime)
    overtime_hours = sum(float(ot.total_hours) for ot in today_overtime)
    
    # Calculate meal stats for tomorrow
    from datetime import timedelta
    from models import Menu
    tomorrow = today + timedelta(days=1)
    
    # Get all meal registrations for tomorrow
    tomorrow_meals = MealRegistration.query.filter(
        MealRegistration.date == tomorrow,
        MealRegistration.has_meal == True
    ).all()
    
    # Count by meal type (normal vs special/improved)
    total_meals = len(tomorrow_meals)
    special_meals = 0
    normal_meals = 0
    
    for meal in tomorrow_meals:
        if meal.menu and meal.menu.is_special:
            special_meals += 1
        else:
            normal_meals += 1
    
    print("DEBUG: Rendering admin_dashboard.html")
    print(f"DEBUG: User = {current_user.name}")
    print(f"DEBUG: Role = {current_user.role}")
    print(f"DEBUG: Total active users = {total_users}, Working = {working_users}, Business trip = {business_trip_users}")
    print(f"DEBUG: Overtime today = {overtime_count} people, {overtime_hours} hours")
    print(f"DEBUG: Total meals tomorrow = {total_meals}, Normal = {normal_meals}, Special = {special_meals}")
    
    return render_template('admin_dashboard.html', 
                         user=current_user.name,
                         total_users=total_users,
                         working_users=working_users,
                         business_trip_users=business_trip_users,
                         overtime_count=overtime_count,
                         overtime_hours=overtime_hours,
                         total_meals=total_meals,
                         normal_meals=normal_meals,
                         special_meals=special_meals)

@app.route('/admin/users')
@login_required
def admin_users():
    """User management page - admin only"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    from models import Position
    # Get all users and positions
    users = User.query.order_by(User.created_at.desc()).all()
    positions = Position.query.order_by(Position.code).all()
    
    # Create position lookup dictionary for template
    position_dict = {str(pos.code): pos.name for pos in positions}
    
    return render_template('admin_users.html', users=users, positions=positions, position_dict=position_dict)

@app.route('/admin/users/list', methods=['GET'])
@login_required
def admin_users_list():
    """API endpoint to get users list as JSON"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    users = User.query.order_by(User.created_at.desc()).all()
    positions = Position.query.order_by(Position.code).all()
    
    # Create position lookup map (convert both to string for comparison)
    position_map = {str(pos.code): pos.name for pos in positions}
    
    users_data = []
    for user in users:
        # Get position name from map, or 'Chưa xác định' if not found
        position_code = str(user.position) if user.position else None
        position_name = position_map.get(position_code, 'Chưa xác định') if position_code else 'Chưa xác định'
        users_data.append({
            'id': user.id,
            'employee_id': user.employee_id,
            'name': user.name,
            'email': user.email,
            'department': user.department,
            'position': user.position,
            'position_name': position_name,
            'role': user.role,
            'is_active': user.is_active,
            'work_status': user.work_status,
            'avatar_url': user.avatar_url,
            'gender': user.gender,
            'phone': user.phone,
            'citizen_id': user.citizen_id,
            'hometown': user.hometown
        })
    
    return {'success': True, 'users': users_data}

@app.route('/admin/approvals')
@login_required
def admin_approvals():
    """Request approval page - admin only"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('admin_approvals.html')

@app.route('/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
def toggle_user_active(user_id):
    """Toggle user active status"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        return {'success': False, 'message': 'Không thể vô hiệu hóa tài khoản của chính mình'}, 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'kích hoạt' if user.is_active else 'vô hiệu hóa'
    return {'success': True, 'message': f'Đã {status} user {user.name}', 'is_active': user.is_active}

@app.route('/admin/users/<int:user_id>/change-role', methods=['POST'])
@login_required
def change_user_role(user_id):
    """Change user role"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from changing their own role
    if user.id == current_user.id:
        return {'success': False, 'message': 'Không thể thay đổi quyền của chính mình'}, 400
    
    new_role = request.json.get('role')
    if new_role not in ['admin', 'user']:
        return {'success': False, 'message': 'Quyền không hợp lệ'}, 400
    
    user.role = new_role
    db.session.commit()
    
    return {'success': True, 'message': f'Đã thay đổi quyền của {user.name} thành {new_role}', 'role': user.role}

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        return {'success': False, 'message': 'Không thể xóa tài khoản của chính mình'}, 400
    
    user_name = user.name
    db.session.delete(user)
    db.session.commit()
    
    return {'success': True, 'message': f'Đã xóa user {user_name}'}

@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
@login_required
def edit_user(user_id):
    """Edit user information"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    from werkzeug.utils import secure_filename
    import os
    from datetime import datetime
    
    user = User.query.get_or_404(user_id)
    
    # Handle both JSON and FormData
    try:
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email already exists
            existing = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing:
                return {'success': False, 'message': 'Email đã tồn tại'}, 400
            user.email = data['email']
        if 'employee_id' in data:
            # Check if employee_id already exists
            existing = User.query.filter(User.employee_id == data['employee_id'], User.id != user_id).first()
            if existing:
                return {'success': False, 'message': 'Mã nhân viên đã tồn tại'}, 400
            user.employee_id = data['employee_id']
        
        # Handle department - just set the string field
        if 'department' in data:
            user.department = data['department']
        
        # Handle position - store CODE in position field
        if 'position' in data:
            pos_value = data['position']  # This is the code (1, 2, 3, 4...)
            user.position = pos_value  # Store code directly
        
        if 'role' in data:
            user.role = data['role']
        if 'work_status' in data:
            user.work_status = data['work_status']
        if 'is_active' in data:
            # Convert string 'true'/'false' to boolean
            user.is_active = data['is_active'] in ['true', 'True', True, 1, '1']
        
        # Handle personal information fields
        if 'gender' in data:
            user.gender = data['gender'] if data['gender'] else None
        if 'phone' in data:
            user.phone = data['phone'] if data['phone'] else None
        if 'citizen_id' in data:
            user.citizen_id = data['citizen_id'] if data['citizen_id'] else None
        if 'hometown' in data:
            user.hometown = data['hometown'] if data['hometown'] else None
        
        # Handle password update
        if 'password' in data and data['password']:
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(data['password'])
        
        # Handle avatar upload
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename:
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                filename = secure_filename(avatar_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                
                if file_ext in allowed_extensions:
                    # Create upload folder if not exists
                    upload_folder = os.path.join('static', 'uploads', 'avatars')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Generate unique filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_filename = f"{user.employee_id}_{timestamp}.{file_ext}"
                    filepath = os.path.join(upload_folder, new_filename)
                    
                    # Save file
                    avatar_file.save(filepath)
                    
                    # Update user avatar_url
                    user.avatar_url = f"/static/uploads/avatars/{new_filename}"
        
        db.session.commit()
        
        return {'success': True, 'message': f'Đã cập nhật thông tin {user.name}'}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error in edit_user: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'message': f'Lỗi: {str(e)}'}, 500


@app.route('/users/<int:user_id>/clear-avatar', methods=['POST'])
@login_required
def clear_avatar(user_id):
    """Clear user avatar"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    try:
        user = User.query.get_or_404(user_id)
        
        # Delete old avatar file if exists
        if user.avatar_url:
            import os
            old_file = user.avatar_url.lstrip('/')
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except Exception as e:
                    print(f"Error deleting file: {e}")
        
        # Clear avatar_url in database
        user.avatar_url = None
        db.session.commit()
        
        return {'success': True, 'message': 'Đã xóa ảnh đại diện'}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error in clear_avatar: {e}")
        return {'success': False, 'message': f'Lỗi: {str(e)}'}, 500


@app.route('/admin/users/add', methods=['POST'])
@login_required
def add_user():
    """Add new user"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    from werkzeug.utils import secure_filename
    import os
    from datetime import datetime
    
    # Handle both JSON and FormData
    try:
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        # Validate required fields
        required_fields = ['employee_id', 'name', 'email', 'password', 'department', 'position']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'success': False, 'message': f'Thiếu thông tin: {field}'}, 400
        
        # Check if employee_id already exists
        if User.query.filter_by(employee_id=data['employee_id']).first():
            return {'success': False, 'message': 'Mã nhân viên đã tồn tại'}, 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return {'success': False, 'message': 'Email đã tồn tại'}, 400
        
        # Create new user - store code directly in position field
        new_user = User(
            employee_id=data['employee_id'],
            name=data['name'],
            email=data['email'],
            department=data['department'],  # Department name
            position=data['position'],  # Position code (1, 2, 3, 4...)
            role=data.get('role', 'user'),
            work_status=data.get('work_status', 'working'),
            is_active=data.get('is_active', True) if isinstance(data.get('is_active'), bool) else data.get('is_active') in ['true', 'True', True, 1, '1'],
            gender=data.get('gender') if data.get('gender') else None,
            phone=data.get('phone') if data.get('phone') else None,
            citizen_id=data.get('citizen_id') if data.get('citizen_id') else None,
            hometown=data.get('hometown') if data.get('hometown') else None
        )
        new_user.set_password(data['password'])
        
        # Handle avatar upload
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename:
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                filename = secure_filename(avatar_file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                
                if file_ext in allowed_extensions:
                    # Create upload folder if not exists
                    upload_folder = os.path.join('static', 'uploads', 'avatars')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Generate unique filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_filename = f"{new_user.employee_id}_{timestamp}.{file_ext}"
                    filepath = os.path.join(upload_folder, new_filename)
                    
                    # Save file
                    avatar_file.save(filepath)
                    
                    # Update user avatar_url
                    new_user.avatar_url = f"/static/uploads/avatars/{new_filename}"
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'success': True, 'message': f'Đã thêm nhân viên {new_user.name}'}
    
    except Exception as e:
        db.session.rollback()
        print(f"Error in add_user: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'message': f'Lỗi: {str(e)}'}, 500

@app.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
def reset_user_password(user_id):
    """Reset user password to default (123456)"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    user = User.query.get_or_404(user_id)
    
    # Reset password to default
    user.password = generate_password_hash('123456')
    db.session.commit()
    
    return {'success': True, 'message': f'Đã reset mật khẩu của {user.name} về 123456'}

# ============= POSITION MANAGEMENT ROUTES =============
@app.route('/admin/positions')
@login_required
def admin_positions():
    """Position management page - admin only"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    from models import Position
    
    # Auto-create positions table and default data if not exists
    try:
        db.create_all()
        if Position.query.count() == 0:
            default_positions = [
                {'code': '1', 'name': 'Nhân viên'},
                {'code': '2', 'name': 'Công nhân'},
                {'code': '3', 'name': 'Trưởng phòng'},
                {'code': '4', 'name': 'Phó phòng'},
                {'code': '5', 'name': 'Giám sát'},
                {'code': '6', 'name': 'Trưởng nhóm'},
                {'code': '7', 'name': 'Quản lý'},
            ]
            for pos_data in default_positions:
                position = Position(**pos_data)
                db.session.add(position)
            db.session.commit()
            flash('Đã tạo 7 chức vụ mặc định', 'success')
    except Exception as e:
        print(f"Error creating positions: {e}")
    
    positions = Position.query.order_by(Position.code).all()
    return render_template('admin_positions.html', positions=positions)

@app.route('/admin/positions/list')
@login_required
def list_positions():
    """Get positions list as JSON"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    positions = Position.query.order_by(Position.code).all()
    return {
        'success': True,
        'positions': [{'id': p.id, 'code': p.code, 'name': p.name} for p in positions]
    }

@app.route('/admin/positions/add', methods=['POST'])
@login_required
def add_position():
    """Add new position"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    data = request.json
    code = data.get('code', '').strip().upper()
    name = data.get('name', '').strip()
    
    if not code or not name:
        return {'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}, 400
    
    # Check if code already exists
    existing = Position.query.filter_by(code=code).first()
    if existing:
        return {'success': False, 'message': 'Mã chức vụ đã tồn tại'}, 400
    
    position = Position(code=code, name=name)
    db.session.add(position)
    db.session.commit()
    
    return {'success': True, 'message': f'Đã thêm chức vụ {name}'}

@app.route('/admin/positions/<int:position_id>/edit', methods=['POST'])
@login_required
def edit_position(position_id):
    """Edit position"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    position = Position.query.get_or_404(position_id)
    
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return {'success': False, 'message': 'Vui lòng điền tên chức vụ'}, 400
    
    position.name = name
    db.session.commit()
    
    return {'success': True, 'message': f'Đã cập nhật chức vụ {name}'}

@app.route('/admin/positions/<int:position_id>/delete', methods=['POST'])
@login_required
def delete_position(position_id):
    """Delete position"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Position
    position = Position.query.get_or_404(position_id)
    
    # Check if any users are using this position
    users_count = User.query.filter_by(position=position.name).count()
    if users_count > 0:
        return {'success': False, 'message': f'Không thể xóa. Có {users_count} nhân viên đang sử dụng chức vụ này'}, 400
    
    db.session.delete(position)
    db.session.commit()
    
    return {'success': True, 'message': f'Đã xóa chức vụ {position.name}'}

# ============= END POSITION MANAGEMENT ROUTES =============

# ============= DEPARTMENT MANAGER ROUTES - REMOVED =============
# Old department_managers system has been replaced with level-based hierarchy
# No longer need to manually manage department managers
# Users with lower level automatically become approvers for their subordinates
# ============= END DEPARTMENT MANAGER ROUTES =============

# ============= OVERTIME APPROVAL ROUTES =============
@app.route('/admin/overtime-approvals')
@login_required
def admin_overtime_approvals():
    """Admin overtime approvals page"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('admin_overtime_approvals.html')

@app.route('/admin/overtime-requests/list')
@login_required
def list_overtime_requests():
    """Get all overtime requests for admin"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    status_filter = request.args.get('status', 'all')
    
    query = OvertimeRequest.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    requests = query.order_by(OvertimeRequest.created_at.desc()).all()
    
    return {
        'success': True,
        'requests': [{
            'id': r.id,
            'employee_name': r.employee_name,
            'employee_id': r.employee_id,
            'department': r.department,
            'position': r.position,
            'overtime_date': r.overtime_date.strftime('%Y-%m-%d'),
            'start_time': r.start_time.strftime('%H:%M'),
            'end_time': r.end_time.strftime('%H:%M'),
            'total_hours': float(r.total_hours),
            'reason': r.reason,
            'status': r.status,
            'manager_comment': r.manager_comment,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
        } for r in requests]
    }

# ============= END OVERTIME APPROVAL ROUTES =============

# ============= MANAGER OVERTIME APPROVAL ROUTES =============
@app.route('/manager/overtime-approvals')
@login_required
def manager_overtime_approvals():
    """Manager overtime approvals page"""
    # Admin always has access
    if current_user.role == 'admin':
        return render_template('manager_overtime_approvals.html')
    
    # Position code 1 (Trưởng Phòng) can approve
    if current_user.position == '1':
        return render_template('manager_overtime_approvals.html')
    
    # Or if user has subordinates
    if current_user.is_manager():
        return render_template('manager_overtime_approvals.html')
    
    flash('Bạn không có quyền truy cập trang này', 'error')
    return redirect(url_for('dashboard'))

@app.route('/manager/overtime-requests')
@login_required
def get_manager_overtime_requests():
    """Get overtime requests that this user can approve (based on level hierarchy)"""
    # Admin always has access
    if current_user.role == 'admin':
        # Admin can see all requests
        requests = OvertimeRequest.query.order_by(
            OvertimeRequest.created_at.desc()
        ).all()
    else:
        # Position code 1 (Trưởng Phòng) can approve
        can_approve = (current_user.position == '1') or current_user.is_manager()
        
        if not can_approve:
            return {'success': False, 'message': 'Không có quyền'}, 403
        
        # Get subordinate user IDs
        subordinates = current_user.get_subordinates()
        subordinate_ids = [sub.id for sub in subordinates]
        
        # If Trưởng Phòng (position 1), include own requests
        if current_user.position == '1':
            subordinate_ids.append(current_user.id)
        
        # Get requests from subordinates (and self if Trưởng Phòng)
        requests = OvertimeRequest.query.filter(
            OvertimeRequest.user_id.in_(subordinate_ids)
        ).order_by(OvertimeRequest.created_at.desc()).all() if subordinate_ids else []
    
    return {
        'success': True,
        'requests': [{
            'id': r.id,
            'employee_name': r.employee_name,
            'employee_id': r.employee_id,
            'department': r.department,
            'position': r.position,
            'overtime_date': r.overtime_date.strftime('%Y-%m-%d'),
            'start_time': r.start_time.strftime('%H:%M'),
            'end_time': r.end_time.strftime('%H:%M'),
            'total_hours': float(r.total_hours),
            'reason': r.reason,
            'status': r.status,
            'manager_comment': r.manager_comment,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
        } for r in requests]
    }

@app.route('/manager/overtime-requests/<int:request_id>/approve', methods=['POST'])
@login_required
def approve_overtime_request(request_id):
    """Approve overtime request (level-based authorization)"""
    overtime_request = OvertimeRequest.query.get_or_404(request_id)
    requester = User.query.get(overtime_request.user_id)
    
    # Check authorization
    can_approve = False
    
    # Admin can approve all
    if current_user.role == 'admin':
        can_approve = True
    # Can approve subordinates
    elif current_user.can_approve_for(requester):
        can_approve = True
    # Can approve own request if highest level in department
    elif requester.id == current_user.id:
        if current_user.position:
            try:
                my_position_code = int(current_user.position)
                users_in_dept = User.query.filter(
                    User.department == current_user.department,
                    User.work_status != 'resigned',
                    User.position.isnot(None)
                ).all()
                
                lowest_code = my_position_code
                for user in users_in_dept:
                    try:
                        user_code = int(user.position)
                        if user_code < lowest_code:
                            lowest_code = user_code
                    except (ValueError, TypeError):
                        continue
                
                if my_position_code == lowest_code:
                    can_approve = True
            except (ValueError, TypeError):
                pass
    
    if not can_approve:
        return {'success': False, 'message': 'Bạn không có quyền duyệt yêu cầu này'}, 403
    
    # Check if already processed
    if overtime_request.status != 'pending':
        return {'success': False, 'message': 'Yêu cầu đã được xử lý'}, 400
    
    data = request.json
    comment = data.get('comment', '').strip()
    
    overtime_request.status = 'approved'
    overtime_request.manager_id = current_user.id
    overtime_request.manager_approved_at = datetime.utcnow()
    if requester.id == current_user.id:
        overtime_request.manager_comment = 'Tự duyệt (cấp cao nhất trong phòng)'
    else:
        overtime_request.manager_comment = comment if comment else None
    
    db.session.commit()
    
    return {'success': True, 'message': f'Đã duyệt yêu cầu tăng ca của {overtime_request.employee_name}'}

@app.route('/manager/overtime-requests/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_overtime_request(request_id):
    """Reject overtime request (level-based authorization)"""
    overtime_request = OvertimeRequest.query.get_or_404(request_id)
    requester = User.query.get(overtime_request.user_id)
    
    # Check authorization
    can_reject = False
    
    # Admin can reject all
    if current_user.role == 'admin':
        can_reject = True
    # Can reject subordinates
    elif current_user.can_approve_for(requester):
        can_reject = True
    # Can reject own request if highest level in department
    elif requester.id == current_user.id:
        if current_user.position:
            try:
                my_position_code = int(current_user.position)
                users_in_dept = User.query.filter(
                    User.department == current_user.department,
                    User.work_status != 'resigned',
                    User.position.isnot(None)
                ).all()
                
                lowest_code = my_position_code
                for user in users_in_dept:
                    try:
                        user_code = int(user.position)
                        if user_code < lowest_code:
                            lowest_code = user_code
                    except (ValueError, TypeError):
                        continue
                
                if my_position_code == lowest_code:
                    can_reject = True
            except (ValueError, TypeError):
                pass
    
    if not can_reject:
        return {'success': False, 'message': 'Bạn không có quyền xử lý yêu cầu này'}, 403
    
    # Check if already processed
    if overtime_request.status != 'pending':
        return {'success': False, 'message': 'Yêu cầu đã được xử lý'}, 400
    
    data = request.json
    comment = data.get('comment', '').strip()
    
    if not comment:
        return {'success': False, 'message': 'Vui lòng nhập lý do từ chối'}, 400
    
    overtime_request.status = 'rejected'
    overtime_request.manager_id = current_user.id
    overtime_request.manager_approved_at = datetime.utcnow()
    overtime_request.manager_comment = comment
    
    db.session.commit()
    
    return {'success': True, 'message': f'Đã từ chối yêu cầu tăng ca của {overtime_request.employee_name}'}

# ============= END MANAGER OVERTIME APPROVAL ROUTES =============

# ============= OVERTIME REPORTS ROUTES =============
@app.route('/overtime/reports')
@login_required
def overtime_reports():
    """Overtime reports page - admin only"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('overtime_reports.html')

@app.route('/overtime/reports/data')
@login_required
def get_overtime_reports_data():
    """Get overtime reports data"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from sqlalchemy import func, extract
    from datetime import datetime, timedelta
    
    period_type = request.args.get('period_type', 'month')
    period_value = int(request.args.get('period_value', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))
    
    # Calculate date range
    if period_type == 'month':
        start_date = datetime(year, period_value, 1).date()
        if period_value == 12:
            end_date = datetime(year, 12, 31).date()
        else:
            end_date = (datetime(year, period_value + 1, 1) - timedelta(days=1)).date()
    elif period_type == 'quarter':
        start_month = (period_value - 1) * 3 + 1
        start_date = datetime(year, start_month, 1).date()
        end_month = start_month + 2
        if end_month == 12:
            end_date = datetime(year, 12, 31).date()
        else:
            end_date = (datetime(year, end_month + 1, 1) - timedelta(days=1)).date()
    else:  # year
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
    
    # Get approved requests in period
    requests = OvertimeRequest.query.filter(
        OvertimeRequest.overtime_date >= start_date,
        OvertimeRequest.overtime_date <= end_date,
        OvertimeRequest.status == 'approved'
    ).all()
    
    # Calculate summary
    total_hours = sum(float(r.total_hours) for r in requests)
    unique_employees = len(set(r.employee_id for r in requests))
    total_requests = len(requests)
    avg_hours = total_hours / unique_employees if unique_employees > 0 else 0
    
    # Group by department
    dept_data = {}
    for r in requests:
        if r.department not in dept_data:
            dept_data[r.department] = 0
        dept_data[r.department] += float(r.total_hours)
    
    by_department = [
        {'department': dept, 'total_hours': hours}
        for dept, hours in sorted(dept_data.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Trend data
    trend_data = []
    if period_type == 'month':
        # Daily trend
        current_date = start_date
        while current_date <= end_date:
            day_requests = [r for r in requests if r.overtime_date == current_date]
            day_hours = sum(float(r.total_hours) for r in day_requests)
            trend_data.append({
                'label': f'{current_date.day}/{current_date.month}',
                'total_hours': day_hours
            })
            current_date += timedelta(days=1)
    elif period_type == 'quarter':
        # Monthly trend
        for month in range(start_month, end_month + 1):
            month_requests = [r for r in requests if r.overtime_date.month == month]
            month_hours = sum(float(r.total_hours) for r in month_requests)
            trend_data.append({
                'label': f'T{month}',
                'total_hours': month_hours
            })
    else:
        # Quarterly trend
        for q in range(1, 5):
            q_start_month = (q - 1) * 3 + 1
            q_end_month = q_start_month + 2
            q_requests = [r for r in requests if q_start_month <= r.overtime_date.month <= q_end_month]
            q_hours = sum(float(r.total_hours) for r in q_requests)
            trend_data.append({
                'label': f'Q{q}',
                'total_hours': q_hours
            })
    
    # Top employees
    emp_data = {}
    for r in requests:
        key = r.employee_id
        if key not in emp_data:
            emp_data[key] = {
                'employee_id': r.employee_id,
                'employee_name': r.employee_name,
                'department': r.department,
                'total_hours': 0,
                'request_count': 0
            }
        emp_data[key]['total_hours'] += float(r.total_hours)
        emp_data[key]['request_count'] += 1
    
    top_employees = sorted(emp_data.values(), key=lambda x: x['total_hours'], reverse=True)[:10]
    
    return {
        'success': True,
        'summary': {
            'total_hours': total_hours,
            'total_employees': unique_employees,
            'total_requests': total_requests,
            'avg_hours': avg_hours
        },
        'by_department': by_department,
        'trend': trend_data,
        'top_employees': top_employees
    }

@app.route('/overtime/reports/export')
@login_required
def export_overtime_reports():
    """Export overtime reports to Excel"""
    if current_user.role != 'admin':
        flash('Bạn không có quyền', 'error')
        return redirect(url_for('dashboard'))
    
    from datetime import datetime, timedelta
    import io
    from flask import send_file
    
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
    except ImportError:
        flash('Vui lòng cài đặt openpyxl: pip install openpyxl', 'error')
        return redirect(url_for('overtime_reports'))
    
    period_type = request.args.get('period_type', 'month')
    period_value = int(request.args.get('period_value', datetime.now().month))
    year = int(request.args.get('year', datetime.now().year))
    
    # Calculate date range
    if period_type == 'month':
        start_date = datetime(year, period_value, 1).date()
        if period_value == 12:
            end_date = datetime(year, 12, 31).date()
        else:
            end_date = (datetime(year, period_value + 1, 1) - timedelta(days=1)).date()
        period_name = f"Tháng {period_value}/{year}"
    elif period_type == 'quarter':
        start_month = (period_value - 1) * 3 + 1
        start_date = datetime(year, start_month, 1).date()
        end_month = start_month + 2
        if end_month == 12:
            end_date = datetime(year, 12, 31).date()
        else:
            end_date = (datetime(year, end_month + 1, 1) - timedelta(days=1)).date()
        period_name = f"Quý {period_value}/{year}"
    else:
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        period_name = f"Năm {year}"
    
    # Get data
    requests = OvertimeRequest.query.filter(
        OvertimeRequest.overtime_date >= start_date,
        OvertimeRequest.overtime_date <= end_date,
        OvertimeRequest.status == 'approved'
    ).order_by(OvertimeRequest.overtime_date.desc()).all()
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Báo cáo tăng ca"
    
    # Header
    ws['A1'] = f"BÁO CÁO TĂNG CA - {period_name}"
    ws['A1'].font = Font(size=14, bold=True)
    ws.merge_cells('A1:H1')
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Column headers
    headers = ['STT', 'Mã NV', 'Họ tên', 'Phòng ban', 'Ngày', 'Giờ bắt đầu', 'Giờ kết thúc', 'Tổng giờ']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')
    
    # Data rows
    for idx, req in enumerate(requests, 1):
        ws.cell(row=idx+3, column=1, value=idx)
        ws.cell(row=idx+3, column=2, value=req.employee_id)
        ws.cell(row=idx+3, column=3, value=req.employee_name)
        ws.cell(row=idx+3, column=4, value=req.department)
        ws.cell(row=idx+3, column=5, value=req.overtime_date.strftime('%d/%m/%Y'))
        ws.cell(row=idx+3, column=6, value=req.start_time.strftime('%H:%M'))
        ws.cell(row=idx+3, column=7, value=req.end_time.strftime('%H:%M'))
        ws.cell(row=idx+3, column=8, value=float(req.total_hours))
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 25
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 10
    
    # Save to BytesIO
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"BaoCaoTangCa_{period_name.replace('/', '_').replace(' ', '_')}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

# ============= END OVERTIME REPORTS ROUTES =============

# ============= MEAL MANAGEMENT ROUTES =============
@app.route('/admin/meals')
@login_required
def admin_meals():
    """Admin meal management page"""
    if current_user.role != 'admin':
        flash('Không có quyền truy cập', 'error')
        return redirect(url_for('dashboard'))
    
    from datetime import datetime, timedelta
    
    # Get current week (Monday to Sunday)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    
    days_of_week = []
    day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        days_of_week.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day_names[i],
            'day_num': day.day
        })
    
    return render_template('admin_meals.html', 
                         days_of_week=days_of_week,
                         current_lang=session.get('lang', 'vi'),
                         t=get_translation())

@app.route('/admin/stats')
@login_required
def admin_stats():
    """Admin statistics and reports page"""
    if current_user.role != 'admin':
        flash('Không có quyền truy cập', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('admin_stats.html')

@app.route('/admin/stats/data')
@login_required
def get_stats_data():
    """Get meal statistics data"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from datetime import datetime, timedelta
    from sqlalchemy import func
    from models import Menu
    
    period = request.args.get('period', 'tomorrow')  # tomorrow, week, month
    
    # Calculate date range
    today = datetime.now().date()
    if period == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        start_date = tomorrow
        end_date = tomorrow
    elif period == 'week':
        # Current week (Monday to Sunday)
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    else:  # month
        start_date = today.replace(day=1)
        # Last day of month
        if today.month == 12:
            end_date = today.replace(day=31)
        else:
            end_date = (today.replace(month=today.month + 1, day=1) - timedelta(days=1))
    
    # Get registrations for the period
    registrations = MealRegistration.query.filter(
        MealRegistration.date >= start_date,
        MealRegistration.date <= end_date,
        MealRegistration.has_meal == True
    ).all()
    
    # Calculate summary
    total_meals = len(registrations)
    normal_meals = sum(1 for r in registrations if r.menu and not r.menu.is_special)
    special_meals = sum(1 for r in registrations if r.menu and r.menu.is_special)
    
    # Get daily breakdown for chart (for week period)
    daily_data = []
    if period == 'week':
        for i in range(7):
            day = start_date + timedelta(days=i)
            day_regs = [r for r in registrations if r.date == day]
            normal = sum(1 for r in day_regs if r.menu and not r.menu.is_special)
            special = sum(1 for r in day_regs if r.menu and r.menu.is_special)
            
            day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
            daily_data.append({
                'day': day_names[i],
                'date': day.strftime('%d/%m'),
                'normal': normal,
                'special': special
            })
    
    # Get detailed registration list with user info
    registration_list = []
    for reg in registrations:
        registration_list.append({
            'id': reg.id,
            'user_name': reg.user.name,
            'employee_id': reg.user.employee_id,
            'department': reg.user.department,
            'date': reg.date.strftime('%d/%m/%Y'),
            'meal_name': reg.menu.dish_name if reg.menu else 'N/A',
            'meal_type': 'Cải Thiện' if (reg.menu and reg.menu.is_special) else 'Bình Thường',
            'is_special': reg.menu.is_special if reg.menu else False,
            'notes': reg.notes or ''
        })
    
    return {
        'success': True,
        'period': period,
        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
        'summary': {
            'total': total_meals,
            'normal': normal_meals,
            'special': special_meals
        },
        'daily_data': daily_data,
        'registrations': registration_list
    }

@app.route('/admin/meals/list')
@login_required
def list_meals():
    """Get all meals"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Menu
    menus = Menu.query.filter_by(is_active=True).all()
    
    return {
        'success': True,
        'menus': [{
            'id': m.id,
            'date': m.date.strftime('%Y-%m-%d'),
            'meal_type': m.meal_type,
            'dish_name': m.dish_name,
            'description': m.description,
            'image_url': m.image_url,
            'is_special': m.is_special,
            'is_vegetarian': m.is_vegetarian
        } for m in menus]
    }

@app.route('/admin/meals/add', methods=['POST'])
@login_required
def add_meal():
    """Add new meal to menu"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Menu
    from datetime import datetime
    
    data = request.json
    date_str = data.get('date')
    meal_type = data.get('meal_type')
    dish_name = data.get('dish_name', '').strip()
    description = data.get('description', '').strip()
    image_url = data.get('image_url', '').strip()
    is_special = data.get('is_special', False)
    is_vegetarian = data.get('is_vegetarian', False)
    
    if not date_str or not meal_type or not dish_name:
        return {'success': False, 'message': 'Vui lòng điền đầy đủ thông tin'}, 400
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return {'success': False, 'message': 'Ngày không hợp lệ'}, 400
    
    menu = Menu(
        date=date,
        meal_type=meal_type,
        dish_name=dish_name,
        description=description,
        image_url=image_url if image_url else None,
        is_special=is_special,
        is_vegetarian=is_vegetarian
    )
    
    db.session.add(menu)
    db.session.commit()
    
    return {'success': True, 'message': f'Đã thêm món {dish_name}'}

@app.route('/admin/meals/<int:meal_id>/edit', methods=['POST'])
@login_required
def edit_meal(meal_id):
    """Edit meal"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Menu
    from datetime import datetime
    
    menu = Menu.query.get_or_404(meal_id)
    data = request.json
    
    date_str = data.get('date')
    if date_str:
        try:
            menu.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return {'success': False, 'message': 'Ngày không hợp lệ'}, 400
    
    menu.meal_type = data.get('meal_type', menu.meal_type)
    menu.dish_name = data.get('dish_name', menu.dish_name).strip()
    menu.description = data.get('description', menu.description).strip()
    menu.is_special = data.get('is_special', menu.is_special)
    menu.is_vegetarian = data.get('is_vegetarian', menu.is_vegetarian)
    
    # Update image_url if provided
    if 'image_url' in data:
        menu.image_url = data['image_url'] if data['image_url'] else None
    
    db.session.commit()
    
    return {'success': True, 'message': f'Đã cập nhật món {menu.dish_name}'}

@app.route('/admin/meals/upload-image', methods=['POST'])
@login_required
def upload_meal_image():
    """Upload meal image"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    import os
    from werkzeug.utils import secure_filename
    
    if 'image' not in request.files:
        return {'success': False, 'message': 'Không có file ảnh'}, 400
    
    file = request.files['image']
    
    if file.filename == '':
        return {'success': False, 'message': 'Không có file được chọn'}, 400
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext not in allowed_extensions:
        return {'success': False, 'message': 'Định dạng file không hợp lệ'}, 400
    
    # Create upload directory if not exists
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'meals')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(upload_dir, new_filename)
    
    # Save file
    try:
        file.save(file_path)
        image_url = f"/static/uploads/meals/{new_filename}"
        return {'success': True, 'image_url': image_url, 'message': 'Tải ảnh lên thành công'}
    except Exception as e:
        return {'success': False, 'message': f'Lỗi khi lưu file: {str(e)}'}, 500

@app.route('/admin/meals/<int:meal_id>/delete', methods=['POST'])
@login_required
def delete_meal(meal_id):
    """Delete meal"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    from models import Menu
    menu = Menu.query.get_or_404(meal_id)
    
    dish_name = menu.dish_name
    db.session.delete(menu)
    db.session.commit()
    
    return {'success': True, 'message': f'Đã xóa món {dish_name}'}

# ============= END MEAL MANAGEMENT ROUTES =============

@app.route('/overtime', methods=['GET', 'POST'])
@login_required
def overtime():
    if request.method == 'POST':
        from datetime import datetime
        
        # Get form data
        selected_date = request.form.get('selected_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        reason = request.form.get('reason')
        
        if not all([selected_date, start_time, end_time, reason]):
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return redirect(url_for('overtime'))
        
        # Parse date and time
        try:
            overtime_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            flash('Định dạng ngày giờ không hợp lệ', 'error')
            return redirect(url_for('overtime'))
        
        # Calculate total hours
        start_datetime = datetime.combine(overtime_date, start_time_obj)
        end_datetime = datetime.combine(overtime_date, end_time_obj)
        total_hours = (end_datetime - start_datetime).total_seconds() / 3600
        
        if total_hours <= 0:
            flash('Giờ kết thúc phải sau giờ bắt đầu', 'error')
            return redirect(url_for('overtime'))
        
        # Create overtime request
        overtime_request = OvertimeRequest(
            user_id=current_user.id,
            employee_id=current_user.employee_id,
            employee_name=current_user.name,
            department=current_user.department,
            position=current_user.position,
            overtime_date=overtime_date,
            start_time=start_time_obj,
            end_time=end_time_obj,
            total_hours=round(total_hours, 2),
            reason=reason,
            status='pending'
        )
        
        db.session.add(overtime_request)
        db.session.commit()
        
        flash('Đã gửi yêu cầu tăng ca thành công!', 'success')
        return redirect(url_for('overtime'))
    
    # GET request - show form
    return render_template('overtime.html')

@app.route('/overtime/my-requests')
@login_required
def get_my_overtime_requests():
    """Get current user's overtime requests"""
    requests = OvertimeRequest.query.filter_by(user_id=current_user.id).order_by(OvertimeRequest.created_at.desc()).all()
    
    return {
        'success': True,
        'requests': [{
            'id': r.id,
            'overtime_date': r.overtime_date.strftime('%Y-%m-%d'),
            'start_time': r.start_time.strftime('%H:%M'),
            'end_time': r.end_time.strftime('%H:%M'),
            'total_hours': float(r.total_hours),
            'reason': r.reason,
            'status': r.status,
            'manager_comment': r.manager_comment,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
        } for r in requests]
    }

@app.route('/overtime/<int:request_id>/cancel', methods=['POST'])
@login_required
def cancel_overtime_request(request_id):
    """Cancel overtime request (only if pending)"""
    overtime_request = OvertimeRequest.query.get_or_404(request_id)
    
    # Check if user owns this request
    if overtime_request.user_id != current_user.id:
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    # Can only cancel pending requests
    if overtime_request.status != 'pending':
        return {'success': False, 'message': 'Chỉ có thể hủy yêu cầu đang chờ duyệt'}, 400
    
    db.session.delete(overtime_request)
    db.session.commit()
    
    return {'success': True, 'message': 'Đã hủy yêu cầu tăng ca'}

@app.route('/overtime/<int:request_id>/self-approve', methods=['POST'])
@login_required
def self_approve_overtime_request(request_id):
    """Self-approve overtime request (only for highest level users)"""
    overtime_request = OvertimeRequest.query.get_or_404(request_id)
    
    # Check if user owns this request
    if overtime_request.user_id != current_user.id:
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    # Can only approve pending requests
    if overtime_request.status != 'pending':
        return {'success': False, 'message': 'Yêu cầu này đã được xử lý'}, 400
    
    # Check if user is highest level in department (lowest position code)
    if not current_user.position:
        return {'success': False, 'message': 'Không xác định được chức vụ'}, 400
    
    try:
        my_position_code = int(current_user.position)
        # Find lowest position code in department (highest authority)
        users_in_dept = User.query.filter(
            User.department == current_user.department,
            User.work_status != 'resigned',
            User.position.isnot(None)
        ).all()
        
        lowest_code = my_position_code
        for user in users_in_dept:
            try:
                user_code = int(user.position)
                if user_code < lowest_code:
                    lowest_code = user_code
            except (ValueError, TypeError):
                continue
        
        if my_position_code != lowest_code:
            return {'success': False, 'message': 'Chỉ người có cấp cao nhất mới có thể tự duyệt'}, 403
    except (ValueError, TypeError):
        return {'success': False, 'message': 'Chức vụ không hợp lệ'}, 400
    
    # Approve the request
    overtime_request.status = 'approved'
    overtime_request.manager_id = current_user.id
    overtime_request.manager_approved_at = datetime.utcnow()
    overtime_request.manager_comment = 'Tự duyệt (cấp cao nhất trong phòng)'
    
    db.session.commit()
    
    return {'success': True, 'message': 'Đã duyệt yêu cầu tăng ca'}

@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    from datetime import datetime, timedelta
    
    if request.method == 'POST':
        date = request.form.get('date')
        meal_id = request.form.get('meal_id')
        
        if not date or not meal_id:
            flash('Vui lòng chọn món ăn', 'error')
            return redirect(url_for('meals'))
        
        # Check if registration already exists
        existing = MealRegistration.query.filter_by(
            user_id=current_user.id,
            date=date
        ).first()
        
        if existing:
            # Update existing registration
            existing.meal_id = meal_id
            existing.updated_at = datetime.utcnow()
        else:
            # Create new registration
            meal_registration = MealRegistration(
                user_id=current_user.id,
                date=date,
                meal_id=meal_id,
                has_meal=True
            )
            db.session.add(meal_registration)
        
        db.session.commit()
        flash('Đăng ký suất ăn thành công!', 'success')
        return redirect(url_for('meals'))
    
    # Get current week (Monday to Sunday)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    
    days_of_week = []
    day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        days_of_week.append({
            'date': day.strftime('%Y-%m-%d'),
            'day_name': day_names[i],
            'day_num': day.day
        })
    
    # Get user's meal registrations
    registrations = MealRegistration.query.filter_by(user_id=current_user.id).order_by(MealRegistration.date.desc()).all()
    
    return render_template('meals.html', 
                         days_of_week=days_of_week,
                         registrations=registrations)

@app.route('/meals/menu/<date>')
@login_required
def get_menu_for_date(date):
    """Get menu for specific date"""
    from models import Menu
    from datetime import datetime
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return {'success': False, 'message': 'Ngày không hợp lệ'}, 400
    
    menus = Menu.query.filter_by(date=date_obj, is_active=True).all()
    
    # Get user's registration for this date
    registration = MealRegistration.query.filter_by(
        user_id=current_user.id,
        date=date_obj
    ).first()
    
    # Check if registration is locked (after 4 PM for next day)
    now = datetime.now()
    today = now.date()
    current_hour = now.hour
    
    # If it's after 4 PM (16:00) and the selected date is tomorrow, lock registration
    is_locked = False
    if current_hour >= 16:
        from datetime import timedelta
        tomorrow = today + timedelta(days=1)
        if date_obj == tomorrow:
            is_locked = True
    
    # Also lock if the date is in the past
    if date_obj < today:
        is_locked = True
    
    return {
        'success': True,
        'menus': [{
            'id': m.id,
            'dish_name': m.dish_name,
            'description': m.description,
            'image_url': m.image_url,
            'meal_type': m.meal_type,
            'is_special': m.is_special,
            'is_vegetarian': m.is_vegetarian
        } for m in menus],
        'selected_meal_id': registration.meal_id if registration else None,
        'is_locked': is_locked
    }

@app.route('/meals/week-registrations')
@login_required
def get_week_registrations():
    """Get user's meal registrations for the current week"""
    from datetime import datetime, timedelta
    from models import Menu
    
    # Get week offset from query params
    week_offset = int(request.args.get('offset', 0))
    
    # Calculate week start (Monday)
    today = datetime.now().date()
    today_with_offset = today + timedelta(days=week_offset * 7)
    week_start = today_with_offset - timedelta(days=today_with_offset.weekday())
    
    # Get registrations for the week
    registrations = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        
        reg = MealRegistration.query.filter_by(
            user_id=current_user.id,
            date=day
        ).first()
        
        if reg and reg.menu:
            registrations[day_str] = {
                'has_registration': True,
                'is_special': reg.menu.is_special
            }
        else:
            registrations[day_str] = {
                'has_registration': False,
                'is_special': False
            }
    
    return {'success': True, 'registrations': registrations}

@app.route('/meals/register', methods=['POST'])
@login_required
def register_meal():
    """Register meal for user"""
    from datetime import datetime, timedelta
    
    data = request.json
    date_str = data.get('date')
    meal_id = data.get('meal_id')
    
    if not date_str or not meal_id:
        return {'success': False, 'message': 'Thiếu thông tin'}, 400
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return {'success': False, 'message': 'Ngày không hợp lệ'}, 400
    
    # Check if registration is locked
    now = datetime.now()
    today = now.date()
    current_hour = now.hour
    
    # If it's after 4 PM (16:00) and trying to register for tomorrow, deny
    if current_hour >= 16:
        tomorrow = today + timedelta(days=1)
        if date_obj == tomorrow:
            return {'success': False, 'message': 'Đã quá thời gian đăng ký cho ngày mai (sau 16h)'}, 403
    
    # Don't allow registration for past dates
    if date_obj < today:
        return {'success': False, 'message': 'Không thể đăng ký cho ngày đã qua'}, 403
    
    # Check if registration exists
    existing = MealRegistration.query.filter_by(
        user_id=current_user.id,
        date=date_obj
    ).first()
    
    if existing:
        existing.meal_id = meal_id
        existing.has_meal = True
        existing.updated_at = datetime.utcnow()
    else:
        registration = MealRegistration(
            user_id=current_user.id,
            date=date_obj,
            meal_id=meal_id,
            has_meal=True
        )
        db.session.add(registration)
    
    db.session.commit()
    
    return {'success': True, 'message': 'Đăng ký thành công!'}

@app.route('/meals/cancel', methods=['POST'])
@login_required
def cancel_meal():
    """Cancel meal registration"""
    from datetime import datetime, timedelta
    
    data = request.json
    date_str = data.get('date')
    
    if not date_str:
        return {'success': False, 'message': 'Thiếu thông tin'}, 400
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return {'success': False, 'message': 'Ngày không hợp lệ'}, 400
    
    # Check if cancellation is locked
    now = datetime.now()
    today = now.date()
    current_hour = now.hour
    
    # If it's after 4 PM (16:00) and trying to cancel for tomorrow, deny
    if current_hour >= 16:
        tomorrow = today + timedelta(days=1)
        if date_obj == tomorrow:
            return {'success': False, 'message': 'Đã quá thời gian hủy đăng ký cho ngày mai (sau 16h)'}, 403
    
    # Don't allow cancellation for past dates
    if date_obj < today:
        return {'success': False, 'message': 'Không thể hủy đăng ký cho ngày đã qua'}, 403
    
    # Find and delete registration
    existing = MealRegistration.query.filter_by(
        user_id=current_user.id,
        date=date_obj
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return {'success': True, 'message': 'Đã hủy đăng ký!'}
    else:
        return {'success': False, 'message': 'Không tìm thấy đăng ký'}, 404

@app.route('/profile')
@login_required
def profile():
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Calculate total overtime hours for current year
    current_year = datetime.now().year
    total_overtime_hours = db.session.query(
        func.sum(OvertimeRequest.total_hours)
    ).filter(
        OvertimeRequest.user_id == current_user.id,
        OvertimeRequest.status == 'approved',
        func.year(OvertimeRequest.overtime_date) == current_year
    ).scalar() or 0
    
    # Count total meals registered this year
    total_meals = MealRegistration.query.filter(
        MealRegistration.user_id == current_user.id,
        func.year(MealRegistration.date) == current_year
    ).count()
    
    # Check if today has special meal registration
    today = datetime.now().date()
    today_meal = MealRegistration.query.filter(
        MealRegistration.user_id == current_user.id,
        MealRegistration.date == today
    ).first()
    
    has_special_meal_today = False
    if today_meal and today_meal.menu:
        has_special_meal_today = today_meal.menu.is_special
    
    return render_template('profile.html', 
                         user=current_user,
                         total_overtime_hours=float(total_overtime_hours),
                         total_meals=total_meals,
                         has_special_meal_today=has_special_meal_today,
                         now=datetime.now(),
                         timedelta=timedelta)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect', 'error')
            return render_template('change_password.html', form=form)
        
        # Update password
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('change_password.html', form=form)

@app.route('/logout')
def logout():
    """Logout user and clear all session data"""
    # Force remove user from session
    session.pop('_user_id', None)
    session.pop('user_name', None)
    session.pop('_fresh', None)
    
    # Logout user
    if current_user.is_authenticated:
        logout_user()
    
    # Clear all session data
    session.clear()
    
    # Create response with redirect
    response = redirect(url_for('login'))
    
    # Delete all cookies
    response.set_cookie('remember_token', '', expires=0, path='/')
    response.set_cookie('session', '', expires=0, path='/')
    
    return response

# PWA Routes
@app.route('/static/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/static/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

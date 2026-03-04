from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.user import User
from controllers.auth_controller import AuthController
from translations import get_translation

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Language middleware
@app.before_request
def set_language():
    if 'lang' not in session:
        session['lang'] = 'vi'  # Default language

@app.context_processor
def inject_translations():
    """Inject translations into all templates"""
    lang = session.get('lang', 'vi')
    return dict(t=get_translation(lang), current_lang=lang)

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
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
    if request.method == 'POST':
        return AuthController.login(request)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        full_name = request.form.get('full_name')
        employee_id = request.form.get('employee_id')
        email = request.form.get('email')
        department = request.form.get('department')
        password = request.form.get('password')
        
        if not all([full_name, employee_id, email, department, password]):
            flash(t['required_fields'], 'error')
            return render_template('register.html')
        
        # TODO: Save to database
        flash(t['register_success'], 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        identifier = request.form.get('identifier')
        
        if not identifier:
            flash(t['required_fields'], 'error')
            return render_template('forgot_password.html')
        
        # TODO: Send reset email
        flash(t['reset_success'], 'success')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if admin
    if session.get('user_id') == 'ADMIN':
        return redirect(url_for('admin_dashboard'))
    
    return render_template('dashboard.html', user=session.get('user_name'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Only admin can access
    if session.get('user_id') != 'ADMIN':
        flash('Bạn không có quyền truy cập trang này', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('admin_dashboard.html', user=session.get('user_name'))

@app.route('/overtime', methods=['GET', 'POST'])
def overtime():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        reason = request.form.get('reason')
        meal = request.form.get('meal')
        
        if not all([start_time, end_time, reason]):
            flash(t['required_fields'], 'error')
            return render_template('overtime.html')
        
        # TODO: Save to database
        flash('Yêu cầu tăng ca đã được gửi thành công!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('overtime.html')

@app.route('/meals', methods=['GET', 'POST'])
def meals():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        meal_id = request.form.get('meal_id')
        
        if not meal_id:
            flash(t['required_fields'], 'error')
            return render_template('meals.html')
        
        # TODO: Save to database
        flash('Đã đăng ký suất ăn thành công!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('meals.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            flash(t['required_fields'], 'error')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash(t['password_mismatch'], 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 8:
            flash(t['password_too_short'], 'error')
            return render_template('change_password.html')
        
        # TODO: Verify current password and update in database
        flash(t['password_changed'], 'success')
        return redirect(url_for('profile'))
    
    return render_template('change_password.html')

@app.route('/logout')
def logout():
    return AuthController.logout()

# PWA Routes
@app.route('/static/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/static/service-worker.js')
def service_worker():
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

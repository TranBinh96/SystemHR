from flask import request, redirect, url_for, session, flash, render_template
from models.user import User
from translations import get_translation

class AuthController:
    @staticmethod
    def login(request):
        """Xử lý đăng nhập"""
        lang = session.get('lang', 'vi')
        t = get_translation(lang)
        
        employee_id = request.form.get('employee_id')
        password = request.form.get('password')
        
        if not employee_id or not password:
            flash(t['required_fields'], 'error')
            return render_template('login.html')
        
        user = User.authenticate(employee_id, password)
        
        if user:
            session['user_id'] = user.employee_id
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash(t['login_error'], 'error')
            return render_template('login.html')
    
    @staticmethod
    def logout():
        """Xử lý đăng xuất"""
        session.clear()
        return redirect(url_for('login'))

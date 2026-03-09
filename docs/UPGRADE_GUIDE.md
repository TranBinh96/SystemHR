# Flask Upgrade Guide - SQLAlchemy & Flask-Login

## What's New

The application has been upgraded with the following Flask extensions:

- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Flask-Admin**: Admin panel for database management
- **Flask-WTF**: Form handling with CSRF protection
- **Flask-Migrate**: Database migration tool

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
FLASK_ENV=development

# Database Configuration
DB_HOST=10.216.28.11
DB_PORT=3306
DB_USER=ovnm
DB_PASSWORD=P@ssw0rd
DB_NAME=db_hr

# Application Settings
APP_NAME=OKI VIETNAM HR
DEFAULT_LANGUAGE=vi
TIMEZONE=Asia/Ho_Chi_Minh
```

### 3. Initialize Database

Run the initialization script to create tables and default users:

```bash
python init_db.py
```

This will create:
- All database tables (users, overtime_requests, meal_registrations)
- Admin user: `ADMIN` / `admin123`
- Sample user: `EMP001` / `password123`

### 4. (Optional) Use Flask-Migrate for Database Migrations

If you want to use migrations instead of direct table creation:

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## Key Changes

### Authentication
- Now uses Flask-Login for session management
- All protected routes use `@login_required` decorator
- Access current user with `current_user` object

### Database Operations
- SQLAlchemy models in `models/__init__.py`
- No more raw SQL queries
- Use `db.session.add()`, `db.session.commit()` for operations

### Forms
- WTForms with built-in validation
- CSRF protection enabled
- Form classes in `forms.py`

### Admin Panel
- Access at `/admin` route
- Manage users, overtime requests, and meal registrations
- Only accessible to users with `role='admin'`

## Testing

### 1. Start the Application

```bash
python app.py
```

### 2. Login

- Admin: `ADMIN` / `admin123`
- User: `EMP001` / `password123`

### 3. Test Features

- Register new users
- Submit overtime requests
- Register for meals
- Change password
- Admin panel (admin only)

## Database Schema

### Users Table
- `id`: Primary key
- `employee_id`: Unique employee identifier
- `name`: Full name
- `email`: Email address (unique)
- `password`: Hashed password
- `department`: Department name
- `role`: 'user' or 'admin'
- `is_active`: Account status
- `created_at`: Registration timestamp

### Overtime Requests Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `date`: Overtime date
- `start_time`: Start time
- `end_time`: End time
- `reason`: Reason for overtime
- `status`: 'pending', 'approved', or 'rejected'
- `approved_by`: Foreign key to users (approver)
- `approved_at`: Approval timestamp
- `created_at`, `updated_at`: Timestamps

### Meal Registrations Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `date`: Meal date
- `meal_type`: Type of meal
- `has_meal`: Boolean flag
- `notes`: Additional notes
- `created_at`, `updated_at`: Timestamps

## Troubleshooting

### Database Connection Error
- Check MySQL server is running
- Verify credentials in `.env` file
- Ensure database `db_hr` exists

### Import Errors
- Run `pip install -r requirements.txt`
- Activate virtual environment

### Migration Issues
- Delete `migrations` folder and reinitialize
- Or use `init_db.py` for direct table creation

## Next Steps

1. Update templates to use WTForms syntax (add CSRF tokens)
2. Implement overtime approval workflow
3. Add email notifications
4. Implement forgot password functionality
5. Add more admin features

## Deployment

For Railway deployment:
- Ensure all environment variables are set in Railway dashboard
- Database will be created automatically on first run
- Run `python init_db.py` after deployment to create tables

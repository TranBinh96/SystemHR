class User:
    def __init__(self, employee_id, password, name=None):
        self.employee_id = employee_id
        self.password = password
        self.name = name
    
    @staticmethod
    def authenticate(employee_id, password):
        """Xác thực người dùng - Demo với dữ liệu mẫu"""
        # TODO: Thay thế bằng database thực tế
        demo_users = {
            'binh337': {'password': 'binh3011', 'name': 'Administrator'},
            'binhtt': {'password': 'binh3011', 'name': 'Nguyễn Văn A'},
            'EMP002': {'password': 'password456', 'name': 'Trần Thị B'}
        }
        
        if employee_id in demo_users:
            user_data = demo_users[employee_id]
            if user_data['password'] == password:
                return User(employee_id, password, user_data['name'])
        return None
    
    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name
        }

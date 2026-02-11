import bcrypt

class User:
    def __init__(self, username, password, role, active=1):
        self.id = None
        self.username = username
        self.password = password
        self.role = role
        self.active = active

    def is_active(self):
        return self.active == 1

    def is_admin(self):
        return self.role == 'admin'

    def is_staff(self):
        return self.role == 'staff'

    def verify_password(self, password):
        if not self.is_active():
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except (ValueError, AttributeError):
            # Fallback for legacy plain-text passwords
            return self.password == password

    def deactivate(self):
        self.active = 0

    def reactivate(self):
        self.active = 1

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'active': self.active
        }

    @staticmethod
    def from_dict(data):
        user = User(data['username'], data['password'], data['role'], data.get('active', 1))
        user.id = data.get('id')
        return user

    @staticmethod
    def create_with_hashed_password(username, plain_password, role):
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return User(username, hashed_password.decode('utf-8'), role, active=1)

    def __repr__(self):
        status = "Active" if self.is_active() else "Inactive"
        return f"User(ID: {self.id}, {self.username}, {self.role}, {status})"
class User:
    def __init__(self, username, password, role, active=1):
        self.id = None
        self.username = username
        self.password = password
        self.role = role
        self.active = active

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

    def __repr__(self):
        return f"User(ID: {self.id}, {self.username}, {self.role}, Active: {self.active})"
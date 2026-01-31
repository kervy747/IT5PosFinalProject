class User:
    def __init__(self, username, password, role):
        self.id = None  # NEW: Will be set when loading from database
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'id': self.id,  # NEW: Include id
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(data):
        user = User(data['username'], data['password'], data['role'])
        user.id = data.get('id')  # NEW: Load id if present
        return user

    def __repr__(self):
        return f"User(ID: {self.id}, {self.username}, {self.role})"
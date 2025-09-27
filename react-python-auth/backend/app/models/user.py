class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # In a real application, ensure to hash this password

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    # Add methods for user-related operations, such as saving to a database, etc.
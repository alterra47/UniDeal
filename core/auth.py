import bcrypt

def Password_Hasher(password):
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt
    salt = bcrypt.gensalt()
    
    # Hash password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

def verify_password(password, hashed_password):
    """Verify a password against a hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    )
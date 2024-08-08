import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')

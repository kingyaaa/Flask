import hashlib

def hash_password(password):
    # 将密码编码为 UTF-8 字节串
    password_bytes = password.encode('utf-8')

    # 使用 SHA-256 哈希函数计算密码的哈希值
    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return hashed_password

def verify_password(password, hashed_password):
    # 将密码编码为 UTF-8 字节串
    password_bytes = password.encode('utf-8')

    # 使用 SHA-256 哈希函数计算输入密码的哈希值
    input_hash = hashlib.sha256(password_bytes).hexdigest()

    # 比较输入密码的哈希值与存储的哈希值是否相同
    if input_hash == hashed_password:
        return True
    else:
        return False

# 示例使用
stored_hash = hash_password('my_password')
password = 'my_password'

# 验证密码是否与存储的哈希值匹配
result = verify_password(password, stored_hash)
print(result)  # 输出: True
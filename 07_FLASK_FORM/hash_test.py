from werkzeug.security import generate_password_hash, check_password_hash

password = "123"
password_hash = generate_password_hash(password)
print("hased_password: ", password_hash)

correct_password = "123"
check_result = check_password_hash(password_hash, correct_password)
print("check_ password_hash: ", check_result)

wrong_password = "abc"
check_result = check_password_hash(password_hash, wrong_password)
print("check_ password_hash: ", check_result)
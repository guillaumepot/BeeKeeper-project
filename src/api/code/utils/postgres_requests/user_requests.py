#api/utils/postgres_requests/user_requests.py


# Lib
###


"""
REQUESTS
- Contains POSTGRES requests for the API
"""



"""
Queries that return data
"""


 # Params: $1: username (str)
query_get_username:str = (
    "SELECT u.username " \
    "FROM users u " \
    "WHERE username = $1;"
    )

# Params: $1: username (str)
query_get_user_credentials_in_database:str = (
    "SELECT username, password, verified " \
    "FROM users " \
    "WHERE username = $1"
    )


 # Params: $1: username (str)
query_get_user_secure_data:str = (
    "SELECT u.id, u.username, u.role, r.role AS role_name, ul.created_at AS created_at, ul.updated_at AS updated_at, ul.last_login as last_login " \
    "FROM users u " \
    "JOIN roles r ON u.role = r.id " \
    "JOIN user_logs ul ON u.id = ul.user_id " \
    "WHERE username = $1"
    )


# Params: $1: username (str)
query_get_user_info_data:str = (
    "SELECT u.username, ui.address, ui.zipcode, ui.city, ui.country, ui.phone, ui.email " \
    "FROM users u " \
    "JOIN user_infos ui ON u.id = ui.user_id " \
    "WHERE username = $1"
    )



# ---------------------------------------------------------------------------------------------------- #

"""
Queries that write data
"""
# Params: $1: id (uuid4), $2: username (str), $3: password (str), $4: role (int), $5: verified (bool)
query_insert_new_user:str = (
    "INSERT INTO users (id, username, password, role, verified) " \
    "VALUES ($1, $2, $3, $4, $5);"
)

# Params: $1: id (uuid4), $2: address (str), $3: zipcode (str), $4: city (str), $5: country (str), $6: phone (str), $7: email (str)
query_insert_user_info:str = (
    "INSERT INTO user_infos (user_id, address, zipcode, city, country, phone, email) " \
    "VALUES ($1, $2, $3, $4, $5, $6, $7);"
)

# Params: $1: id (uuid4), $2: created_at (datetime), $3: updated_at (datetime), $4: last_login (datetime)
query_insert_user_log:str = (
    "INSERT INTO user_logs (user_id, created_at, updated_at, last_login) " \
    "VALUES ($1, $2, $3, $4);"
)


# Params: $1: username (str), $2: updated_informations (dict)
def query_update_user_info_data(user_id_to_update:str, info_to_update:dict) -> None:
    """
    
    """
    values_to_set = ", ".join([f"{key} = '{value}'" for key, value in info_to_update.items()])
        
    query: str = f"""
    UPDATE user_infos
    SET {values_to_set}
    WHERE user_id = '{user_id_to_update}';
    """

    return query



# Params: $1: username (str)
query_force_user_verified_true:str = (
    "UPDATE users " \
    "SET verified = True " \
    "WHERE username = $1;"
)

# Params: $1: password (hashed str), $2: username (str)
query_update_user_password:str = (
    "UPDATE users " \
    "SET password = $1 " \
    "WHERE username = $2;"
)

# Params: $1: username (str)
query_update_user_last_login = (
    "UPDATE user_logs " \
    "SET last_login = NOW() " \
    "WHERE user_id = (SELECT id FROM users WHERE username = $1);"
)
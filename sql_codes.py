import sqlite3

def sql_code(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    return con , cur

def insert_item_into_users(email, password):
    con,cur = sql_code("database/Users.db")
    cur.execute("INSERT INTO user(email, password) VALUES (?, ?)", (email, password))
    con.commit()

def email_exist(email):
    con,cur = sql_code("database/Users.db")
    cur.execute("SELECT * FROM user WHERE email = ?", [email])
    con.commit()
    data = cur.fetchall()
    return data

def tokens(tuple_token):
    con,cur = sql_code("database/Users.db")
    cur.execute("INSERT INTO token VALUES (?, ?, ?, ?, ?, ?)", tuple_token)
    con.commit()

def token_check(email, token):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    SELECT CASE 
        WHEN token1 = ? THEN "ok"
        WHEN token2 = ? THEN "ok"
        WHEN token3 = ? THEN "ok"
        WHEN token4 = ? THEN "ok"
        WHEN token5	= ? THEN "ok"
        ELSE "nop"
    END AS stu_token
    FROM token
    WHERE email = ?
    """
    , (token, token, token, token, token, email))
    con.commit()
    stu = cur.fetchall()
    return stu

def remove_token(token):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    UPDATE token
    SET 
    token1 = CASE WHEN token1 = ? THEN 'Finished' ELSE token1 END,
    token2 = CASE WHEN token2 = ? THEN 'Finished' ELSE token2 END,
    token3 = CASE WHEN token3 = ? THEN 'Finished' ELSE token3 END,
    token4 = CASE WHEN token4 = ? THEN 'Finished' ELSE token4 END,
    token5 = CASE WHEN token5 = ? THEN 'Finished' ELSE token5 END
    """
    , (token, token, token, token, token))
    con.commit()

def update_pass(email,h_password):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    UPDATE user
    set password = ?
    WHERE email = ?
    """
    , (h_password, email))
    con.commit()

def load_post(post_id):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    SELECT * FROM product WHERE product_id = ?
    """
    , (post_id,))
    con.commit()
    stu = cur.fetchall()
    return stu

def add_product_to_basket(email, product_id):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    INSERT INTO product_basket(email, product_id) VALUES (?,?)
    """
    , (email, product_id))
    con.commit()

def orders(email):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    SELECT product_id FROM product_basket WHERE email = ?
    """
    , (email,))
    con.commit()
    stu = cur.fetchall()
    item = []
    for i in stu:
        item.append(i[0])
    item = list(set(item))
    return item

def remove_product(email,product_id):
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    DELETE FROM product_basket
    WHERE email = ? and product_id = ?
    """
    , (email, product_id))
    con.commit()

def product_maker():
    con,cur = sql_code("database/Users.db")
    cur.execute(
    """
    SELECT * FROM product
    """
    )
    con.commit()
    stu = cur.fetchall()
    return stu

def adding_product(all_item):
    con, cur = sql_code("database/Users.db")
    cur.execute(
    """
    INSERT INTO product(name, desc, image, price, pre) VALUES (?,?,?,?,?)
    """
    , (all_item[0], all_item[1], all_item[2], all_item[3], all_item[4]))
    con.commit()

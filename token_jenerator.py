from sql_codes import tokens
from random import sample

def maker(email):
    jenerated = []
    for everything in range(5):
        string = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
        jenerator = sample(string, k=20)
        jenerated.append("".join(jenerator))

    with open(f"token/token({email}).txt", "w") as file:
        for everything in jenerated:
            file.write(everything + "\n")
    
    tuple_token = (email, jenerated[0], jenerated[1], jenerated[2], jenerated[3], jenerated[4])
    tokens(tuple_token)

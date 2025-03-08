import string
import secrets

class GlobalFunction:
    '''this is use to our register class,member,trainor id to make random id
        so we wont repeat our selves
    
    '''
    def generate_random_id(length=8):
        length = 8
        random_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        return ''.join(random_string)

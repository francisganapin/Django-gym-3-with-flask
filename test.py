import random
import string

def generate_random_id(length=8):
    """Generate a random alphanumeric ID of a given length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_id_card(class_name, school_name, student_name):
    """Generate a formatted ID card for a student."""
    id_number = generate_random_id()
    id_card = f"""
    ------------------------------
    | School: {school_name}
    | Class: {class_name}
    | Student: {student_name}
    | ID Number: {id_number}
    ------------------------------
    """
    return id_card

# Example usage
class_name = "Gimik-Ujhasd"
school_name = "Example School"
student_name = "John Doe"

id_card = generate_id_card(class_name, school_name, student_name)
print(id_card)

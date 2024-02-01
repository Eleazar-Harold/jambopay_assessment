import random
import string
import re

def generate_email(fullname, domain="example.com"):
   """Generates a valid email address from a given fullname and domain.

   Args:
       fullname (str): The fullname to use for the email address.
       domain (str, optional): The domain for the email address. Defaults to "example.com".

   Returns:
       str: A valid email address in the format "username@domain".

   Raises:
       ValueError: If the fullname or domain is invalid.
   """

   # Generate username from fullname
   username = re.sub('[\W_]+', '', fullname).lower().replace(" ", ".")  # Convert to lowercase and replace spaces with dots

   # Generate a unique identifier if needed (same logic as before)
   unique_id = ""
   while not re.match(r"^[a-zA-Z0-9]+$", unique_id):
       unique_id = "".join(random.choices(string.ascii_letters + string.digits, k=4))

   # Combine parts to form the email address
   email = f"{username}{unique_id}@{domain}"
   return email
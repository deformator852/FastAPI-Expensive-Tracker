from dotenv import dotenv_values

JWT_SECRET: str = dotenv_values(".env")["JWT_SECRET"]  # pyright:ignore
SESSION_SECRET: str = dotenv_values(".env")["SESSION_SECRET"]  # pyright:ignore
if not JWT_SECRET:
    print("[-]JWT SECRET IS EMPTY[-]")
    exit(0)
if not SESSION_SECRET:
    print("[-]SESSION SECRET IS EMPTY[-]")
    exit(0)
JWT_ALGORITHM = "HS256"

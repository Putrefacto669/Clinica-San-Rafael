# app.py
from login import SistemaLogin

if __name__ == "__main__":
    # Iniciar con el sistema de login
    app_login = SistemaLogin()
    app_login.login_window.mainloop()

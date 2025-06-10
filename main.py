from src.utils.Auth import initialize_session_state, check_auth
from src.utils.LoginPage import show_login_page
from src.utils.Homepage import show_homepage


def main():
    initialize_session_state()

    if check_auth():
        show_homepage()
    else:
        show_login_page()


if __name__ == "__main__":
    main()

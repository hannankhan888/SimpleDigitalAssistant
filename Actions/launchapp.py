import os


def launch_app(program_name: str):
    try:
        first_word = program_name.split(' ', 1)[0]
        app_name = program_name.split(' ', 1)[1]
        print(first_word)
        print(app_name)
        if first_word == "Open" or "Launch":
            os.system(app_name)
    except:
        print("The application cannot be found or opened.")


if __name__ == "__main__":
    launch_app(input("Enter the application you would like to launch: "))
    launch_app("Open notepad")

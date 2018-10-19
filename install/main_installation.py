import sys
import build_main_yaml
import install_creds_json
import installation_finished

steps = [
         build_main_yaml,
         install_creds_json,
         installation_finished
        ]

def serve_user_options(options, response, finished=False):
    """
    Gives user menu
    """
    next_option = 'Continue       - (c)'
    quit_option = 'Quit           - (q)'
    print("Please choose from Options: ")
    print("---------------------------")
    for option in options:
        print(option)
    print(next_option)
    print(quit_option)
    inpt = input("Selection: ").lower()
    print("---------------------------")
    finished, inpt_accepted = response(inpt)
    if inpt == 'q':
        print("Exiting...")
        finished = True
        sys.exit()
    elif inpt == 'c':
        finished = True
    elif not inpt_accepted:
        print("Sorry, input not recognized, please try again.")
        finished = False
    return finished

def run_step(step):
    finished = False
    step.prompt()
    while not finished:
        finished = serve_user_options(step.OPTIONS, step.response)

if __name__ == "__main__":
    print("Beginning Installation of GPyUpload...")
    for step in steps:
        if not step.LAST:
            run_step(step)
        else:
            print("Installation finished.")
            sys.exit()

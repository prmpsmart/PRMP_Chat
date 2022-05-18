import os, subprocess


class PRMP_Reloader:
    """reload ability of a gui app.
    subclass this class and bind Reloader.reload() to an event, or manually call it.
    """

    def __init__(self, app: type):
        self.app = app()
        self.start_reload()

    def runner(self):
        """
        the brain.
        exits the first process, call another process with the environments variables of the current one.
        and sets the PRMP environ variable
        """
        args, env = [os.sys.executable] + os.sys.argv, os.environ
        env["PRMP"] = "RUNNING"
        while True:
            exit_code = subprocess.call(args, env=env, close_fds=False)

            try:
                os.system("cls")
            except:
                try:
                    os.system("clear")
                except:
                    ...

            print(f"{exit_code=}, reloading\n")

    def start_reload(self):
        """
        This is the entry point
        func: function to execute if reloaded

        if PRMP environment variable is not set, it call Reloader.runner
        """
        try:
            if os.environ.get("PRMP") == "RUNNING":
                self.app.start()
            else:
                os.sys.exit(self.runner())
        except Exception as E:
            pass

from prmp_reloader import PRMP_Reloader, os
from server import ServerApp


if "r" in os.sys.argv:
    app = ServerApp()
    app.start()
else:
    PRMP_Reloader(ServerApp)

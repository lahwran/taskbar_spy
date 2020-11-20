
touch update.trigger
watchexec.exe -r -s SIGINT -e py,trigger "C:/Users/Lauren/PycharmProjects/py_inspect/venv3.6.8/Scripts/python.exe update.py" &
watchexec.exe -w server.py "C:/Users/Lauren/PycharmProjects/py_inspect/venv3.6.8/Scripts/hypercorn.exe server:app --reload --bind localhost:9559"
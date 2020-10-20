# Python FastApi on Windows for PDF annotator

## How To Build the service on Windows

```
pyinstaller --hidden-import=win32timezone --additional-hooks-dir=C:\inetpub\utilspython\.hooks ApiPdfConsole.py
```

then you can run the build result in dist\ApiPdfConsole.exe on the background process by using task scheduler windows

then if you want to test the app before create the windows service you can run the ApiPdfConsole.py itself on terminal. But you need to create your virtual environment first and install the requirement on requirements.txt. as the example code below.

```
py virtualenvoronment venv
```
```
venv\Scripts\activate
```
```
pip install -r requirements.txt
```
```
py ApiPdfConsole.py
```

Open new terminal, then run the scirpt tester

```
testservice.py
```

Thank you so much
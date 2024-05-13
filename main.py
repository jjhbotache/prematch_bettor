import webview
import threading

def say_hi_from_python():
    print('Hello from Python!')
    



if __name__ == '__main__':


    window = webview.create_window( title='Simple browser', url="./reactUI/prematch_bettor/dist/index.html", )
    window.expose(
        # functions
        say_hi_from_python,
    )
    webview.start(
        debug=True,
    )
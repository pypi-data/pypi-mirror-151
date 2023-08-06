from flask import *
import time
import random
import json
import logging
import click
import os

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho

def CreateAPI(ip,port,db):
    print("[+] Restarting CreateAPI", end = '')
    time.sleep(1)
    print(".", end = '')
    time.sleep(1)
    print(".", end = '')
    time.sleep(1)
    print(".")
    time.sleep(0.5)
    print("[+] CreateAPI Is Ready To Use!")
    print(f"[+] IP: http://{ip}:{port}\n")
    app.run(host=ip, port=port, debug=db)

def RandomName(place):
    @app.route(place, methods=['GET', 'POST'])
    def randomname():
        cwd = os.getcwd()
        with open(rf"{cwd}\makeapi\functions\names.txt", "r") as n:
            allText = n.read()
            words = list(map(str, allText.split()))
        data_set = {'Page': 'RANDOM NAME', "name": f"{random.choice(words)}", "Timestamp": time.time()}
        json123 = json.dumps(data_set)
        return json123

def RandomJoke(place):
    @app.route(place, methods=['GET', 'POST'])
    def randomjoke():
        cwd = os.getcwd()
        print("[+] This Error Will Be Fixed Soon!")
        with open(rf"{cwd}\makeapi\functions\jokes.txt", "r") as n:
            allText = n.read()
            words = list(map(str, allText.split()))
        data_set = {'Page': 'RANDOM JOKES', "joke": f"{random.choice(words)}", "Timestamp": time.time()}
        json123 = json.dumps(data_set)
        return json123

def OwnPage(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage1(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage1():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage1():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage1():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage2(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage2():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage2():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage2():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage3(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage3():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage3():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage3():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage4(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage4():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage4():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage4():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage5(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage5():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage5():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage5():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage6(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage6():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage6():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage6():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage7(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage7():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage7():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage7():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage8(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage8():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage8():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage8():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage9(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage9():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage9():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage9():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage10(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage10():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage10():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage10():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage11(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage11():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage11():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage11():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage12(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage12():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage12():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage12():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage13(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage13():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage13():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage13():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage14(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage14():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage14():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage14():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage15(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage15():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage15():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage15():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage16(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage16():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage16():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage16():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage17(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage17():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage17():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage17():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage18(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage18():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage18():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage18():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage19(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage19():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage19():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage19():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

def OwnPage20(place,name,what_to_show,name2=None,what_to_show2=None,name3=None,what_to_show3=None):
    if name2 is not None and name3 is None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage20():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    elif name2 is not None and name3 is not None:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage20():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, name2: what_to_show2, name3: what_to_show3,"Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123
    else:
        @app.route(place, methods=['GET', 'POST'])
        def ownpage20():
            data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
            json123 = json.dumps(data_set)
            return json123

@app.route('/', methods=['GET', 'POST'])
def home():
  data_set = {'Page': 'HOME', "Timestamp": time.time()}
  json123 = json.dumps(data_set)
  return json123




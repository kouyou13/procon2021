import subprocess

def submit():
    subprocess.run(["python3","procon32.py","submit","--token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73","-f","solution.txt"])

if __name__ == '__main__':
    # download()
    submit()
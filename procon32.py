# coding: utf-8
import sys
# print(sys.path)
import io
import time
import urllib.parse
import click
import requests

# URL = "https://procon32-practice.kosen.work"  #テスト
URL = "https://procon32-akita.kosen.work"  #本選
# URL = "https://procon32-sub.kosen.work"  #予備
@click.group()

def cli() -> None:
    pass

# python procon32.py download --token=37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73
@cli.command()
@click.option("--url", envvar="PROCON32_URL", default=URL)
@click.option("--token", envvar="PROCON32_TOKEN", required=True)
@click.option("--wait", type=bool, default=False, help="問題が有効になるまで繰り返し取得します")
@click.option("--interval", type=int, default=5, help="--wait が指定されている場合の問題の取得間隔(秒)")
@click.option(
    "-o", type=click.File(mode="wb"), default="problem.ppm", help="取得した問題の出力先"
)
def download(url: str, token: str, wait: bool, interval: int, o: io.BytesIO) -> None:
    # print("hello")
    # token="37a76c1de6d25f4b30d248f44062166811c9d0d4df361d7cad32336ed712ef73"
    endpoint = urllib.parse.urljoin(url, "problem.ppm")
    while True:
        r = requests.get(endpoint, headers={"procon-token": token})
        if r.status_code == 200:
            o.write(r.content)
            return

        click.echo(f"{r.status_code} {r.text.strip()}", err=True)
        if not wait:
            return

        time.sleep(_get_interval(r.status_code, r.text, interval))

@cli.command()
@click.option("--url", envvar="PROCON32_URL", default=URL)
@click.option("--token", envvar="PROCON32_TOKEN", required=True)
@click.option("-f", type=click.File("r"), default="-")
def submit(url: str, token: str, f: io.StringIO) -> None:
    endpoint = url
    fdata=f.read()
    # print(fdata)
    r = requests.post(endpoint, headers={"procon-token": token}, data=fdata)
    # r = requests.post(endpoint, headers={"procon-token": token}, data=fdata, encording="utf-8")
    # r = requests.post(endpoint, headers={"procon-token": token}, data=fdata.encode('utf-8'))
    # print(r.encoding)
    if r.status_code == 200:
        click.echo(r.text.strip())
        return
    click.echo(f"{r.headers['procon-request-id']} {r.status_code} {r.text.strip()}")


def _get_interval(status_code: int, text: str, interval: int) -> int:
    """
    >>> _get_interval(400, "AccessTimeError 30", 5)
    30
    >>> _get_interval(400, "AccessTimeError", 5)
    5
    >>> _get_interval(500, "InternalServerError", 10)
    10
    """
    if status_code != 400:
        return interval
    tokens = text.split(" ")
    if tokens[0] != "AccessTimeError":
        return interval
    if len(tokens) != 2:
        return interval
    return int(tokens[1])

def hello():
    print("hello")
    
if __name__ == "__main__":
    cli()
    # click.option("--token")
    # download()
    # print(" 1!!!")
    # hello()
    

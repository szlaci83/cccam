from bs4 import BeautifulSoup
from config import CLINE_URL, DEFAULT_NO, CONFIG_FILE
import requests
from paramiko import SSHClient
from scp import SCPClient
import config as p


'''
    Script to get CCCam c-lines from free provider and create the CCcam.cfg file to upload to the
    DVB-s unit via scp. It gets 6 c-lines for redundancy.
'''


def _get_cline():
    html = requests.get(CLINE_URL)
    data = html.text
    soup = BeautifulSoup(data, features="html.parser")
    cline = soup.find('h1').contents[0]
    return cline


def _write_cfg(clines):
    with open(CONFIG_FILE, "w+") as f:
        for cline in clines:
            f.write(cline[1:-1] + "\n")
    f.close()


def _get_clines(no_of_clines = DEFAULT_NO):
    clines = []
    for i in range(no_of_clines):
        clines.append(_get_cline())
    return clines


def create_config_file():
    _write_cfg(_get_clines())


def upload_config_file(filename):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(p.SAT_HOST, p.SAT_SSH_PORT, p.USER, p.PASS)
    scp = SCPClient(ssh.get_transport())
    scp.put(filename, remote_path=p.CONF_PATH)
    scp.close()


def _example():
    #create_config_file()
    upload_config_file(CONFIG_FILE)


if __name__ == "__main__":
    _example()

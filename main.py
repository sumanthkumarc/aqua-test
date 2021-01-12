import requests
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt
import time
from subprocess import Popen, PIPE

API_URL = os.environ.get("API_URL", "https://rest.coinapi.io")
RESOURCE_URI = os.environ.get("RESOURCE_URI", "v1/exchangerate")
SRC_CURRENCY_CODE = os.environ.get("SRC_CURRENCY_CODE", "BTC")
DEST_CURRENCY_CODE = os.environ.get("DEST_CURRENCY_CODE", "USD")
API_KEY = os.environ.get("API_KEY", "9D572214-1DE2-44D0-A4F0-29A944203BF7")
DATE_TIME_LOG_FORMAT = os.environ.get("DATE_TIME_LOG_FORMAT", "%Y-%m-%d-%H-%M-%S")
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "/tmp/bitcoin-app.log")
LOG_FREQUENCY = os.environ.get("LOG_FREQUENCY", "1")
S3_BUCKET = os.environ.get("S3_BUCKET", "")


def get_exchange_rate():
    url = f"{API_URL}/{RESOURCE_URI}/{SRC_CURRENCY_CODE}/{DEST_CURRENCY_CODE}"
    headers = {'X-CoinAPI-Key' : API_KEY}
    # response = requests.get(url, headers=headers)

    response = {
      "time": "2021-01-11T15:19:06.2089000Z",
      "asset_id_base": "BTC",
      "asset_id_quote": "USD",
      "rate": 32807.852049416152513191739688
    }
    return response


def get_logger(log_file_path=None):
    """
    Get the file logger object to write logs to.

    :param log_file_path:
        Absolute path to write the log files.
    :return:
        File logger object
    """
    if not log_file_path:
        logging.basicConfig()
        return logging.getLogger()

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        handlers=[
            # 10 MB for each log file and rotated after this with extra number appended as .1, .2 etc
            RotatingFileHandler(
                log_file_path,
                maxBytes=10000000,
                backupCount=10)],
        format="%(message)s",
        level=logging.INFO)

    return logging.getLogger(log_file_path)

def send_logs_to_s3():
    command = f"aws s3 cp {LOG_FILE_PATH} s3://"
    with Popen(command,
               stdin=PIPE,
               stdout=PIPE,
               stderr=PIPE,
               universal_newlines=True,
               shell=True) as proc:
        stdout, stderr = proc.communicate()
        print(stderr)
        print(stdout)

if __name__ == '__main__':
    data = get_exchange_rate()
    logger = get_logger(LOG_FILE_PATH)

    i = 0
    while i <= 30:
        log_dt = dt.now().strftime(DATE_TIME_LOG_FORMAT)
        logger.info(f"{log_dt} - {round(data['rate'], 3)} {DEST_CURRENCY_CODE}")
        time.sleep(int(LOG_FREQUENCY))

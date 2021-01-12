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
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", f"/tmp/bitcoin-app-{dt.now().strftime('%Y-%m-%d-%H-%M')}.log")
LOG_FREQUENCY = int(os.environ.get("LOG_FREQUENCY", "1"))
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", "30"))
S3_BUCKET = os.environ.get("S3_BUCKET", "aqua-test-logs")


def get_exchange_rate(logger):
    url = f"{API_URL}/{RESOURCE_URI}/{SRC_CURRENCY_CODE}/{DEST_CURRENCY_CODE}"
    headers = {'X-CoinAPI-Key' : API_KEY}
    response = requests.get(url, headers=headers)

    try:
        if response.status_code == 200:
            data = response.json()
        elif response.status_code == 429:
            logger.info("Exceeded rate limit for the service")
            return {}
        else:
            return {}
    except Exception as e:
        print(e)
        return {}

    # return {
    #   "time": "2021-01-11T15:19:06.2089000Z",
    #   "asset_id_base": "BTC",
    #   "asset_id_quote": "USD",
    #   "rate": 32807.852049416152513191739688
    # }
    return data


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
    command = f"aws s3 cp {LOG_FILE_PATH} s3://{S3_BUCKET}/{dt.now().strftime('%Y-%m-%d')}/{LOG_FILE_PATH.split('/')[-1]}"
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
    logger = get_logger(LOG_FILE_PATH)

    start_time = time.perf_counter()
    while True:
        log_dt = dt.now().strftime(DATE_TIME_LOG_FORMAT)
        data = get_exchange_rate(logger)
        if data.get("rate", ""):
            logger.info(f"{log_dt} - {round(data['rate'], 3)} {DEST_CURRENCY_CODE}")
        time.sleep(int(LOG_FREQUENCY))

        if int(time.perf_counter() - start_time) >= RUN_TIMEOUT:
            break

    print(f"Took {round((time.perf_counter() - start_time),2)} seconds to complete.")

    send_logs_to_s3()
    exit(0)

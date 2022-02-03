
### File layout

```
.
├── Dockerfile          # Dockerfile for bitcoin app
├── Dockerfile.agent    # Dockerfile for Jenkins agent
├── Jenkinsfile         # Jenksinfile with build pipeline steps
├── main.py             # Bitcoin python entrypoint file
├── README.md           # The doc you are currently reading :P  
└── requirements.txt    # Python app dependencies
```

### Python environment
- Tested with python 3.7 version, with only requests library as dependency.
- Uses https://docs.coinapi.io/#exchange-rates api. Rate limited at 100 requests per day. 
- Uses Rotating file handler for logs.

Environment vars available:
```
API_URL                - The api url to fetch the exchange rates - Default - https://rest.coinapi.io
RESOURCE_URI           - The exchange rate uri Default - v1/exchangerate
SRC_CURRENCY_CODE      - The source currenct code. Default - BTC
DEST_CURRENCY_CODE     - The destination currency code. Default - USD
API_KEY                - API key to autheticate with exchange service
DATE_TIME_LOG_FORMAT   - Date time format to put in the log file. Uses Python datetime formats. Default - %Y-%m-%d-%H-%M-%S Ex: 2021-01-13-12-30-20
LOG_FILE_PATH          - Log file to write the logs. Expects absolute path. Default - /tmp/bitcoin-app-<CURRENT_DATE_TIME>.log
LOG_FREQUENCY          - Frequency to fetch and write the logs. Default - 1s
RUN_TIMEOUT            - The time for the script to run. Default - 30s
S3_BUCKET              - The S3 bucket to write the logs to. Defailt - aqua-test-logs
```

General invocation of code is install dependencies using `pip3 install -r requirements.txt` and then do `python main.py`. This fetches the exchange rate and write the logs to /tmp folder for 30s and pushes log file  to S3 bucket specified.

### coinapi exchange  service

API doc at https://docs.coinapi.io/#exchange-rates

```
HTTP GET - https://rest.coinapi.io/v1/exchangerate/USD/INR?apikey=<API_KEY>
{
  "time": "2021-01-12T19:05:39.6799889Z",
  "asset_id_base": "USD",
  "asset_id_quote": "INR",
  "rate": 79.30543665151342662665043346,
  "intermediaries_in_the_path": [
    "USD",
    "ETH",
    "INR"
  ]
}

HTTP GET - https://rest.coinapi.io/v1/exchangerate/BTC/USD?apikey=<API_KEY>
{
  "time": "2021-01-12T19:08:14.4732048Z",
  "asset_id_base": "BTC",
  "asset_id_quote": "USD",
  "rate": 34817.93150349165305558467255
}
 
```
### Installation steps
1. Install docker from https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
   ```
   docker run -d -p 8080:8080 -p 50000:50000 --restart unless-stopped -v /var/jenkins_home:/var/jenkins_home jenkins/jenkins:lts
   ```
2. Post docker install steps - https://docs.docker.com/engine/install/linux-postinstall/
3. Install jenkins master - https://github.com/jenkinsci/docker/blob/master/README.md#usage use bind mount for persistence and jnlp port open    
4. Install jenkins agent - https://github.com/jenkinsci/remoting/blob/master/docs/inbound-agent.md
   ```
   docker run -d --restart unless-stopped -v /var/run/docker.sock:/var/run/docker.sock --init 963063218698.dkr.ecr.us-east-2.amazonaws.com/jenkins-agent:latest -disableHttpsCertValidation -url http://10.0.1.43:8080 -workDir=/home/jenkins/agent 641c1d28934bbfcc51d71a98c2871a1f7a4cf3311c5c6d8fa964eefe46d6f4d7 agent
   ```
5. Build custom jenkins agent - docker build -f Dockerfile.agent -t test:1.0 . and push to ecr.
6. Ensure proper IAM role for ec2 instances to pull images and push to S3.



### Problems faced:
1. Connecting jenkins agent to master. Getting the secret.
2. Custom Jenkins agent creation.
3. Ensuring docker cli in agent has access to underlying host docker daemon.
4. Ambigious terminology in assignment :P  

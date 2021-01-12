

Jenkins master:

1. install docker from https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
    docker run -d -p 8080:8080 -p 50000:50000 --restart unless-stopped -v /var/jenkins_home:/var/jenkins_home jenkins/jenkins:lts

2. Post docker install steps - https://docs.docker.com/engine/install/linux-postinstall/
3. install jenkins master - https://github.com/jenkinsci/docker/blob/master/README.md#usage use bind mount for persistence and jnlp port open    
4. Install jenkins agent - https://github.com/jenkinsci/remoting/blob/master/docs/inbound-agent.md
    docker run -d --restart unless-stopped --init jenkins/inbound-agent -disableHttpsCertValidation -url http://10.0.1.43:8080 -workDir=/home/jenkins/agent 641c1d28934bbfcc51d71a98c2871a1f7a4cf3311c5c6d8fa964eefe46d6f4d7 agent
5. Build custom jenkins agent - docker build -f Dockerfile.agent -t test:1.0 . and push to ecr

IAM role for ec2 instances
docker sock permissions


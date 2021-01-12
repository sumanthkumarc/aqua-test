pipeline {
    agent { label 'agent'}
    stages {
        stage('Build') {
            steps {
                // Private repo, accessed using creds
                git credentialsId: '1545b435-a486-4ef8-98f4-fe45ab544209', url: 'https://github.com/sumanthkumarc/aqua-test.git'

                sh """
                docker image build -t aqua:1.0 .
                docker container run -d aqua:1.0
                """
            }
        }
    }
}

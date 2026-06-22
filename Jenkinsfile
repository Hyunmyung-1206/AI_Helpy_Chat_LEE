pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        BASE_UI_URL = 'https://qaproject-temp.app.elice.io/ai-helpy-chat'
        BASE_API_URL = 'https://dev-v2-community-api.dev.elicer.io'
        TEST_USER_ID = 'qa5team1-02@elicer.com'
        JIRA_BASE_URL = 'https://gusaud1328.atlassian.net'
        JIRA_EMAIL = 'gusaud1328@gmail.com'
        JIRA_PROJECT_KEY = 'QA'
        DEFAULT_API_TIMEOUT = '10'
        HEADLESS = 'true'
        JAVA_TOOL_OPTIONS = '-Dfile.encoding=UTF-8'
    }

    stages {
        stage('Build Docker Test Image') {
            steps {
                bat '''
                chcp 65001
                docker compose build tests
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'test-user-password', variable: 'TEST_USER_PW'),
                    string(credentialsId: 'jira-api-token', variable: 'JIRA_API_TOKEN'),
                    string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK_URL'),
                    string(credentialsId: 'slack-webhook-failures', variable: 'SLACK_WEBHOOK_FAILURES_URL')
                ]) {
                    bat '''
                    chcp 65001
                    if not exist reports mkdir reports
                    if not exist logs mkdir logs
                    docker compose up --build --abort-on-container-exit --exit-code-from tests tests
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
            archiveArtifacts allowEmptyArchive: true, artifacts: 'logs/**, reports/**, allure-results/**'
            bat 'docker compose down --remove-orphans'
        }
    }
}

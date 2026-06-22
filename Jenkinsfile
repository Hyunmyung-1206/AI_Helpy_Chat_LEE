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
        stage('Install Dependencies') {
            steps {
                bat '''
                py -3 -m venv .venv
                .venv\\Scripts\\python -m pip install --upgrade pip
                .venv\\Scripts\\pip install -r requirements.txt
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
                    if not exist reports mkdir reports
                    .venv\\Scripts\\pytest tests\\test_quiz_create.py tests\\test_ppt_create.py tests\\test_deep_create.py -n 3 --browser chrome --junitxml=reports\\junit.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'logs/**, reports/**'
        }
    }
}

pipeline {
    parameters
    {
        string(name: 'REPOSITORY_URL', defaultValue: 'https://github.com/dockerbaby/check-conn.git', description: '<BR><font color=RED>*</font> URL to GIT repository')
        string(name: 'GIT_REPO_CRED', defaultValue: 'dockerbaby', description: '<BR><font color=RED>*</font> Credential name of GIT user')
        string(name: 'BRANCH', defaultValue: 'releasee/check-conn-app-1.0', description: '<BR>release/check-conn-app-1.0 (default: release/check-conn-app-1.0)')
        string(name: 'PYTHON_TEST_SCRIPT_FILE', defaultValue: 'test_check_conn.py', description: '<BR><font color=RED>*</font> test_check_conn.py')
        string(name: 'PYTHON_APP_SCRIPT_FILE', defaultValue: 'check_conn.py', description: '<BR><font color=RED>*</font> check_conn.py')
        text(name: 'GROOVY_SCRIPT', defaultValue: '', description: '<BR>Insert a groovy script text to run.<BR>e.g.:<br>env.PARAM1=&quot;value1&quot;<br>env.PARAM2=&quot;value2&quot;')
    }

    options
    {
        buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '3'))
        timestamps()
    }

    agent any

    stages {
        stage('Test Script Stage') {
            steps {
                script {
                    sh "python ./${PYTHON_TEST_SCRIPT_FILE}"
                }
            }
        }
        stage('Test App Stage') {
            steps {
                script {
                    sh "python ./${PYTHON_APP_SCRIPT_FILE} -p 80 www.google.com"
                }
            }
        }
        stage ('List job dir') {
            steps {
                sh 'echo $(pwd)'
                sh 'ls .'
                sh 'ls $(pwd)'
            }
        }
    }

    post {
        success {
            sh '[ -d /var/www/html/Release ] || mkdir /var/www/html/Release'
            sh 'rm -f /var/www/html/Release/*'
            sh 'cp $PYTHON_APP_SCRIPT_FILE /var/www/html/Release/'
        }
    }
}

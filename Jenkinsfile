#!groovy​

echo 'Sovrin test...'

parallel 'ubuntu-test':{
    node('ubuntu') {
        try {
            stage('Ubuntu Test: Checkout csm') {
                checkout scm
            }

            stage('Ubuntu Test: Build docker image') {
                sh 'ln -sf ci/sovrin-common-ubuntu.dockerfile Dockerfile'
                def testEnv = docker.build 'sovrin-common-test'
                
                testEnv.inside {
                    stage('Ubuntu Test: Install dependencies') {
                        sh 'virtualenv -p python3.5 test'
                        def plenum = sh 'grep "plenum.*==.*\'" setup.py'
                        plenum = sh "sed -r \"s/plenum.*==(.+)'/\1/\" <<< ${plenum}"
                        plenum = plenum[0..-1]
                        sh 'test/bin/pip install ${plenum}'
                        sh 'test/bin/python setup.py install'
                        sh 'test/bin/pip install pytest'
                    }

                    stage('Ubuntu Test: Test') {
                        try {
                            sh 'cd sovrin_common && ../test/bin/python -m pytest --junitxml=../test-result.xml'
                        }
                        finally {
                            junit 'test-result.xml'
                        }
                    }
                }
            }
        }
        finally {
            stage('Ubuntu Test: Cleanup') {
                step([$class: 'WsCleanup'])
            }
        }
    }   
}, 
'windows-test':{
    echo 'TODO: Implement me'
}

echo 'Sovrin Common test: done'

if (env.BRANCH_NAME != 'master' && env.BRANCH_NAME != 'stable') {
    echo "Sovrin Common ${env.BRANCH_NAME}: skip publishing"
    return
}

echo 'Sovrin Common build...'

node('ubuntu') {
    try {
        stage('Publish: Checkout csm') {
            checkout scm
        }

        stage('Publish: Prepare package') {
        	sh 'chmod -R 777 ci'
        	sh 'ci/prepare-package.sh . $BUILD_NUMBER'
        }
        
        stage('Publish: Publish pipy') {
            sh 'chmod -R 777 ci'
            withCredentials([file(credentialsId: 'pypi_credentials', variable: 'FILE')]) {
                sh 'ln -sf $FILE $HOME/.pypirc' 
                sh 'ci/upload-pypi-package.sh .'
                sh 'rm -f $HOME/.pypirc'
            }
        }

        stage('Publish: Build debs') {
            withCredentials([usernameColonPassword(credentialsId: 'evernym-githib-user', variable: 'USERPASS')]) {
                sh 'git clone https://$USERPASS@github.com/evernym/sovrin-packaging.git'
            }
            echo 'TODO: Implement me'
            // sh ./sovrin-packaging/pack-sovrin-common.sh $BUILD_NUMBER
        }

        stage('Publish: Publish debs') {
            echo 'TODO: Implement me'
            // sh ./sovrin-packaging/upload-build.sh $BUILD_NUMBER
        }
    }
    finally {
        stage('Publish: Cleanup') {
            step([$class: 'WsCleanup'])
        }
    }
}

echo 'Sovrin build: done'

stage('QA notification') {
    echo 'TODO: Add email sending'
    // emailext (template: 'qa-deploy-test')
}
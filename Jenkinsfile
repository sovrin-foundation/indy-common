#!groovy​

@NonCPS
def plenumVersion(text) {
    echo "plenumVersion -> input ${text}"
    def pattern = /.*(plenum.*==.*)'/
    def plenumMatcher = (text =~ pattern)
    echo "plenumVersion -> output ${plenumMatcher[0][1]}"
    return plenumMatcher[0][1]
}

stage('Test') {
    parallel 'ubuntu-test':{
        node('ubuntu') {
            stage('Ubuntu Test') {
                try {
                    echo 'Ubuntu Test: Checkout csm'
                    checkout scm

                    echo 'Ubuntu Test: Build docker image'
                    sh 'ln -sf ci/sovrin-common-ubuntu.dockerfile Dockerfile'
                    def testEnv = docker.build 'sovrin-common-test'
                    
                    testEnv.inside {
                        echo 'Ubuntu Test: Install dependencies'
                        sh 'cd /home/sovrin && virtualenv -p python3.5 test'
                        def plenum = sh(returnStdout: true, script: 'grep "plenum.*==.*\'" setup.py').trim()
                        plenum = plenumVersion(plenum)
                        sh "/home/sovrin/test/bin/pip install ${plenum}"
                        plenumMatcher = null
                        sh '/home/sovrin/test/bin/python setup.py install'
                        sh '/home/sovrin/test/bin/pip install pytest'

                        echo 'Ubuntu Test: Test'
                        try {
                            sh '/home/sovrin/test/bin/python -m pytest --junitxml=test-result.xml'
                        }
                        finally {
                            junit 'test-result.xml'
                        }
                    }
                }
                finally {
                    echo 'Ubuntu Test: Cleanup'
                    step([$class: 'WsCleanup'])
                }
            }
        }   
    }, 
    'windows-test':{
        echo 'TODO: Implement me'
    }
}

if (env.BRANCH_NAME != 'master' && env.BRANCH_NAME != 'stable') {
    echo "Sovrin Common ${env.BRANCH_NAME}: skip publishing"
    return
}

stage('Publish to pypi') {
    node('ubuntu') {
        try {
            echo 'Publish to pypi: Checkout csm'
            checkout scm

            echo 'Publish to pypi: Prepare package'
            sh 'chmod -R 777 ci'
            sh 'ci/prepare-package.sh . $BUILD_NUMBER'

            echo 'Publish to pypi: Publish'
            withCredentials([file(credentialsId: 'pypi_credentials', variable: 'FILE')]) {
                sh 'ln -sf $FILE $HOME/.pypirc'
                sh 'ci/upload-pypi-package.sh .'
                sh 'rm -f $HOME/.pypirc'
            }
        }
        finally {
            echo 'Publish to pypi: Cleanup'
            step([$class: 'WsCleanup'])
        }
    }
}

stage('Build packages') {
    parallel 'ubuntu-build':{
        node('ubuntu') {
            stage('Build deb packages') {
                try {
                    echo 'Build deb packages: Checkout csm'
                    checkout scm

                    echo 'Build deb packages: Prepare package'
                    sh 'chmod -R 777 ci'
                    sh 'ci/prepare-package.sh . $BUILD_NUMBER'

                    echo 'Build deb packages: Build debs'
                    withCredentials([usernameColonPassword(credentialsId: 'evernym-githib-user', variable: 'USERPASS')]) {
                        sh 'git clone https://$USERPASS@github.com/evernym/sovrin-packaging.git'
                    }
                    echo 'TODO: Implement me'
                    // sh ./sovrin-packaging/pack-ledger.sh $BUILD_NUMBER


                    echo 'Build deb packages: Publish debs'
                    echo 'TODO: Implement me'
                    // sh ./sovrin-packaging/upload-build.sh $BUILD_NUMBER
                }
                finally {
                    echo 'Build deb packages: Cleanup'
                        step([$class: 'WsCleanup'])
                    }
                }
        }
    },
    'windows-build':{
        stage('Build msi packages') {
            echo 'TODO: Implement me'
        }
    }
}

stage('System tests') {
    echo 'TODO: Implement me'
}

if (env.BRANCH_NAME != 'stable') {
    return
}

stage('QA notification') {
    emailext (
        subject: "New release candidate '${JOB_NAME}' (${BUILD_NUMBER}) is waiting for input",
        body: "Please go to ${BUILD_URL} and verify the build",
        to: 'alexander.sherbakov@dsr-company.com'
    )
}

def qaApproval
stage('QA approval') {
    try {
        input(message: 'Do you want to publish this package?')
        qaApproval = true
        echo 'QA approval granted'
    }
    catch (Exception err) {
        qaApproval = false
        echo 'QA approval denied'
    }
}
if (!qaApproval) {
    return
}

stage('Release packages') {
    echo 'TODO: Implement me'
}

stage('System tests') {
    echo 'TODO: Implement me'
}

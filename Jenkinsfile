#!groovy​

@Library('SovrinHelpers') _

def name = 'sovrin-common'

def testUbuntu = {
    try {
        echo 'Ubuntu Test: Checkout csm'
        checkout scm

        echo 'Ubuntu Test: Build docker image'
        def testEnv = docker.build('sovrin-common-test', "--build-arg uid=${getUserUid()} -f ci/ubuntu.dockerfile ci")

        testEnv.inside {
            echo 'Ubuntu Test: Install dependencies'
            
            plenum = helpers.extractVersion('plenum')
            sh "/home/sovrin/test/bin/pip install ${plenum}"
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

def testWindows = {
    echo 'TODO: Implement me'
}

testAndPublish(name, [ubuntu: testUbuntu, windows: testWindows])

def publishToPypi() {
    try {
        echo 'Publish to pypi: Checkout csm'
        checkout scm

        echo 'Publish to pypi: Prepare package'
        sh 'chmod -R 777 ci'
        //gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
        version = sh(returnStdout: true, script: 'ci/get-package-version.sh sovrin_common $BUILD_NUMBER').trim()

        sh 'ci/prepare-package.sh . $BUILD_NUMBER'

        echo 'Publish to pypi: Publish'
        withCredentials([file(credentialsId: 'pypi_credentials', variable: 'FILE')]) {
            sh 'ln -sf $FILE $HOME/.pypirc'
            sh 'ci/upload-pypi-package.sh .'
            sh 'rm -f $HOME/.pypirc'
        }

        return version
    }
    finally {
        echo 'Publish to pypi: Cleanup'
        step([$class: 'WsCleanup'])
    }
}

def buildDeb() {
    try {
        echo 'Build deb packages: Checkout csm'
        checkout scm

        echo 'Build deb packages: Prepare package'
        sh 'chmod -R 777 ci'
        sh 'ci/prepare-package.sh . $BUILD_NUMBER'

        dir('sovrin-packaging') {
            echo 'Build deb packages: get packaging code'
            git branch: 'jenkins', credentialsId: 'evernym-githib-user', url: 'https://github.com/evernym/sovrin-packaging'

            echo 'Build deb packages: Build debs'
            def sourcePath = sh(returnStdout: true, script: 'readlink -f ..').trim()
            sh "./pack-debs $BUILD_NUMBER sovrin-common $sourcePath"

            echo 'Build deb packages: Publish debs'
            def repo = env.BRANCH_NAME == 'stable' ? 'rc' : 'master'
            sh "./upload-debs $BUILD_NUMBER sovrin-common $repo"
        }
    }
    finally {
        echo 'Build deb packages: Cleanup'
        dir('sovrin-packaging') {
            deleteDir()
        }
        step([$class: 'WsCleanup'])
    }
}

def buildMsi() {
    echo 'TODO: Implement me'
}

def ubuntuSystemTests() {
    echo 'TODO: Implement me'
}

def windowsSystemTests() {
    echo 'TODO: Implement me'
}

def notifyQA(version) {
    emailext (
        subject: "New release candidate 'sovrin-common-$version' is waiting for approval",
        body: "Please go to ${BUILD_URL}console and verify the build",
        to: 'alexander.sherbakov@dsr-company.com'
    )
}

def approveQA() {
    def qaApproval
    try {
        input(message: 'Do you want to publish this package?')
        qaApproval = true
        echo 'QA approval granted'
    }
    catch (Exception err) {
        qaApproval = false
        echo 'QA approval denied'
    }
    return qaApproval
}


def notifyFail() {
    emailext (
        body: '$DEFAULT_CONTENT',
        recipientProviders: [
            [$class: 'CulpritsRecipientProvider'],
            [$class: 'DevelopersRecipientProvider'],
            [$class: 'RequesterRecipientProvider']
        ],
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS'
       )
}

def notifySuccess() {
    emailext (
        body: '$DEFAULT_CONTENT',
        recipientProviders: [
            [$class: 'CulpritsRecipientProvider'],
            [$class: 'DevelopersRecipientProvider'],
            [$class: 'RequesterRecipientProvider']
        ],
        replyTo: '$DEFAULT_REPLYTO',
        subject: "New ${BRANCH_NAME} build 'sovrin-common-$version'",
        to: '$DEFAULT_RECIPIENTS'
       )
}

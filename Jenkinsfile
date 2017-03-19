#!groovy​

@Library('SovrinHelpers') _

def name = 'sovrin-common'

def testUbuntu = {
    try {
        echo 'Ubuntu Test: Checkout csm'
        checkout scm

        echo 'Ubuntu Test: Build docker image'
        def testEnv = docker.build('sovrin-common-test', "--build-arg uid=${helpers.getUserUid()} -f ci/ubuntu.dockerfile ci")

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
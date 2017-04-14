#!groovy

@Library('SovrinHelpers') _

def name = 'sovrin-common'

def testUbuntu = {
    try {
        echo 'Ubuntu Test: Checkout csm'
        checkout scm

        echo 'Ubuntu Test: Build docker image'
        def testEnv = dockerHelpers.build(name)

        testEnv.inside {
            echo 'Ubuntu Test: Install dependencies'

            def deps = []
            deps.push(helpers.extractVersion('plenum'))
            testHelpers.installDeps(deps)

            echo 'Ubuntu Test: Test'
            testHelpers.testJunit()
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

def testWindowsNoDocker = {
    try {
        echo 'Windows No Docker Test: Checkout csm'
        checkout scm

        testHelpers.createVirtualEnvAndExecute({ python, pip ->
            echo 'Windows No Docker Test: Install dependencies'
            testHelpers.installDepsBat(python, pip)

            echo 'Windows No Docker Test: Test'
            testHelpers.testJunitBat(python, pip)
        })
    }
    finally {
        echo 'Windows No Docker Test: Cleanup'
        step([$class: 'WsCleanup'])
    }
}


//testAndPublish(name, [ubuntu: testUbuntu, windows: testWindowsNoDocker, windowsNoDocker: testWindowsNoDocker])
testAndPublish(name, [ubuntu: testUbuntu], false) // run tests only

if (env.BRANCH_NAME == '3pc-batch') { // not PR
    def releaseVersion = ''
    stage('Get release version') {
        node('ubuntu-master') {
            releaseVersion = getReleaseVersion()
        }
    }

    testAndPublish.publishPypi('Publish to pypi', [:], releaseVersion)
}

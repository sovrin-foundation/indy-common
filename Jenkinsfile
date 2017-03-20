#!groovy​

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
    echo 'TODO: Implement me'
}



testAndPublish(name, [ubuntu: testUbuntu, windows: testWindows, windowsNoDocker: testWindowsNoDocker])
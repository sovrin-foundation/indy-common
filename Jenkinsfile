#!groovy​

@Library('SovrinHelpers') _

def name = 'sovrin-common'

def testUbuntu = {
    try {
        echo 'Ubuntu Test: Checkout csm'
        checkout scm

        echo 'Ubuntu Test: Build docker image'
        def testEnv = helpers.docker.build(name)

        testEnv.inside {
            echo 'Ubuntu Test: Install dependencies'

            def deps = []
            deps.push(helpers.common.extractVersion('plenum'))
            helpers.test.installDeps(deps)

            echo 'Ubuntu Test: Test'
            helpers.test.testJunit()
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

scripts.testAndPublish(name, [ubuntu: testUbuntu, windows: testWindows])
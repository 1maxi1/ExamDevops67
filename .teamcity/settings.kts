import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.vcs.GitVcsRoot

version = "2025.11"

project {
    params {
        param("student.tag", "StudentIO")
        param("env.DOCKER_IMAGE", "replace-me/travel-card-service")
        param("env.DOCKER_USER", "")
        password("env.DOCKER_PASSWORD", "credentialsJSON:******")
        param("env.PROD_COMPOSE_PATH", "/opt/travel-card-service")
    }

    vcsRoot(ExamDevops6Vcs)
    buildType(StudentIOMainBuild)
    buildType(StudentIOFeatureBuild)
}

object ExamDevops6Vcs : GitVcsRoot({
    name = "ExamDevops6_VCS_%student.tag%"
    url = "https://github.com/1maxi1/ExamDevops67.git"
    branch = "refs/heads/main"
    branchSpec = """
        +:refs/heads/main
        +:refs/heads/feature/*
        +:refs/heads/fix/*
    """.trimIndent()
})

object StudentIOMainBuild : BuildType({
    name = "Docker_build_%student.tag%_Main"
    vcs {
        root(ExamDevops6Vcs)
        branchFilter = """
            +:refs/heads/main
        """.trimIndent()
    }
    steps {
        pythonChecks()
        script {
            name = "Docker_push_%student.tag%"
            scriptContent = """
                docker build -t %env.DOCKER_IMAGE%:%build.number% .
                docker tag %env.DOCKER_IMAGE%:%build.number% %env.DOCKER_IMAGE%:latest
                echo %env.DOCKER_PASSWORD% | docker login -u %env.DOCKER_USER% --password-stdin
                docker push %env.DOCKER_IMAGE%:%build.number%
                docker push %env.DOCKER_IMAGE%:latest
            """.trimIndent()
        }
        script {
            name = "Deploy_prod_%student.tag%"
            scriptContent = """
                cd %env.PROD_COMPOSE_PATH%
                docker compose pull || exit 1
                docker compose up -d --force-recreate
            """.trimIndent()
        }
    }
    triggers {
        vcs {
            branchFilter = """
                +:refs/heads/main
            """.trimIndent()
        }
    }
})

object StudentIOFeatureBuild : BuildType({
    name = "Docker_build_%student.tag%_Feature"
    vcs {
        root(ExamDevops6Vcs)
        branchFilter = """
            +:refs/heads/feature/*
            +:refs/heads/fix/*
        """.trimIndent()
    }
    steps {
        pythonChecks()
        script {
            name = "Docker_build_only_%student.tag%"
            scriptContent = "docker build -t %env.DOCKER_IMAGE%:%build.number% ."
        }
    }
    triggers {
        vcs {
            branchFilter = """
                +:refs/heads/feature/*
                +:refs/heads/fix/*
            """.trimIndent()
        }
    }
})

fun BuildType.pythonChecks() {
    steps {
        script {
            name = "Install_dependencies_%student.tag%"
            scriptContent = """
                python -m pip install --upgrade pip
                python -m pip install -r requirements-dev.txt
            """.trimIndent()
        }
        script {
            name = "Lint_%student.tag%"
            scriptContent = "python -m ruff check ."
        }
        script {
            name = "SAST_%student.tag%"
            scriptContent = "python -m bandit -r app"
        }
        script {
            name = "Tests_%student.tag%"
            scriptContent = "python -m pytest"
        }
    }
}

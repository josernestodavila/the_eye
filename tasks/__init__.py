import os
import subprocess

from invoke import task


def _ensure_docker_network_exists(ctx):
    """
    Ensures default Docker network exists and creates it if needed.
    """
    result = ctx.run(
        "docker network ls | grep theeye",
        hide=True,
        warn=True,
    )
    exit_code = result.exited
    if exit_code == 1:
        ctx.run("docker network create theeye")


def _is_running_in_docker():
    """
    Determines whether or not we're already in a Docker container. We can do
    this by looking at init cgroup list and seeing if 'docker' is in the
    output. We'll also look to make sure a particular directoris mounted,
    just in case we're n a Docker-in-Docker scenario.
    """

    # Macs don't have /proc/1/cgroup, so let's check first to see if
    # we're on a Mac.
    uname = str(subprocess.check_output(["uname", "-a"]))
    if "Darwin" in uname:
        return False

    init_cgroup_list = str(subprocess.check_output(["cat", "/proc/1/cgroup"]))
    in_docker = "docker" in init_cgroup_list and os.path.exists("/var/task/the_eye")

    return in_docker


def _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker):

    if not run_in_docker or _is_running_in_docker():
        return

    _ensure_docker_network_exists(ctx)
    ctx.run("docker compose up -d", hide=True)


def _maybe_get_dockerized_command(cmd, run_in_docker):
    """
    If we don't _want_ to run in Docker, or if we're already in Docker,
    just run the command.
    """

    if not run_in_docker or _is_running_in_docker():
        return cmd

    return f"docker compose exec -T theeye /bin/bash -l -c '{cmd}'"


@task
def black(ctx, check=False, run_in_docker=True):
    """
    Runs black for code formatting.
    """
    if check:
        cmd = "black --check ."
    else:
        cmd = "black ."

    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    cmd = _maybe_get_dockerized_command(cmd, run_in_docker)
    ctx.run(cmd)


@task
def build(ctx):
    """
    Build the docker container(s) for the project.
    """
    _ensure_docker_network_exists(ctx)
    ctx.run("docker compose build")


@task
def kill(ctx):
    """
    Kill all the docker containers for the project.
    """
    ctx.run("docker compose kill")


@task
def connect(ctx):
    """
    Opens a bash shell on the running container.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, True)
    os.system("docker compose exec theeye /bin/bash")


@task
def collectstatic(ctx, run_in_docker=True):
    """
    Collect static assets.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    ctx.run(
        _maybe_get_dockerized_command("python manage.py collectstatic", run_in_docker)
    )


@task
def makemigrations(ctx, run_in_docker=True):
    """
    Create database migrations.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    ctx.run(
        _maybe_get_dockerized_command("python manage.py makemigrations", run_in_docker)
    )


@task
def migrate(ctx, run_in_docker=True):
    """
    Execute database migrations.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    ctx.run(_maybe_get_dockerized_command("python manage.py migrate", run_in_docker))


@task
def pip_compile(ctx, run_in_docker=True):
    """
    Updates requirements files.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    requirements_files = [
        "requirements/production.in",
        "requirements/development.in",
    ]

    for requirements_file in requirements_files:
        ctx.run(
            _maybe_get_dockerized_command(
                f"pip-compile {requirements_file}", run_in_docker
            )
        )


@task
def pip_sync(ctx, run_in_docker=True):
    """
    Install dependencies from requirement files.
    """
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    requirements_files = [
        "requirements/production.txt",
        "requirements/development.txt",
    ]

    for requirements_file in requirements_files:
        ctx.run(
            _maybe_get_dockerized_command(
                f"pip-sync {requirements_file}", run_in_docker
            )
        )


@task
def run(ctx, run_in_docker=True):
    """
    Run a UVICorn application server.
    """
    uvicorn_cmd = " ".join(
        [
            "uvicorn the_eye.asgi:application",
            "--host 0.0.0.0",
            "--port 6543",
            "--reload",
            "--lifespan off",
        ]
    )
    kill_command = _maybe_get_dockerized_command(
        'kill -9 $(pgrep -P $(pgrep uvicorn)) ; pkill -9 "(guni|uvi)corn"',
        run_in_docker,
    )
    _maybe_bring_up_detached_compose_cluster(ctx, run_in_docker)
    ctx.run(kill_command, warn=True, hide=True)
    ctx.run(_maybe_get_dockerized_command(uvicorn_cmd, run_in_docker))

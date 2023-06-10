"""Tasks for use with Invoke.

Collection of tasks to us for development/testing
"""
from distutils.util import strtobool
from invoke import Collection, task as invoke_task
import os
from glob import glob as g


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_division_xxx
namespace = Collection("faildruid")
namespace.configure(
    {
        "faildruid": {
            "project_name": "faildruid",
            "python_ver": "3.10",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": ["docker-compose.requirements.yml", "docker-compose.base.yml", "docker-compose.dev.yml"],
            "compose_http_timeout": "86400",
        }
    }
)


def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker-compose command with all appropriate parameters and environment.

    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker-compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        # Note: 'docker-compose logs' will stop following after 60 seconds by default,
        # so we are overriding that by setting this environment variable.
        "COMPOSE_HTTP_TIMEOUT": context.faildruid.compose_http_timeout,
        "PYTHON_VER": context.faildruid.python_ver,
    }
    compose_command = (
        f'docker-compose --project-name {context.faildruid.project_name} --project-directory "{context.faildruid.compose_dir}"'
    )
    for compose_file in context.faildruid.compose_files:
        compose_file_path = os.path.join(context.faildruid.compose_dir, compose_file)
        compose_command += f' -f "{compose_file_path}"'
    compose_command += f" {command}"
    print(f'Running docker-compose command "{command}"')
    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, **kwargs):
    """Wrapper to run a command locally or inside the faildruid container."""
    if is_truthy(context.faildruid.local):
        context.run(command, **kwargs)
    else:
        # Check if faildruid is running, no need to start another faildruid container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if "api" in results.stdout:
            compose_command = f"exec api {command}"
        else:
            compose_command = f"run --entrypoint '{command}' api"

        docker_compose(context, compose_command, pty=True)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    }
)
def build(context, force_rm=False, cache=True):
    """Build faildruid docker image."""
    command = "build"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(f"Building Container Contexts with Python {context.faildruid.python_ver}...")
    docker_compose(context, command)


@task
def generate_packages(context):
    """Generate all Python packages inside docker and copy the file locally under dist/."""
    command = "poetry build"
    run_command(context, command)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG / VSCODE
# ------------------------------------------------------------------------------
@task
def debug(context):
    """Start dev context and its dependencies in debug mode."""
    print("Starting Division 2 DB containers in debug mode...")
    docker_compose(context, "up")


@task
def start(context):
    """Start dev context and its dependencies in detached mode."""
    print("Starting Division 2 DB containers in detached mode...")
    docker_compose(context, "up --detach")


@task
def restart(context):
    """Gracefully restart all containers."""
    print("Restarting Division 2 DB containers...")
    docker_compose(context, "restart")


@task
def stop(context):
    """Stop dev context and its dependencies."""
    print("Stopping Division 2 DB containers...")
    docker_compose(context, "down")


@task
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying Division 2 DB containers...")
    docker_compose(context, "down --volumes")


@task(
    help={
        "service": "Docker-compose service name to view (default: api)",
        "follow": "Follow logs",
        "tail": "Tail N number of lines or 'all'",
    }
)
def logs(context, service="api", follow=False, tail=None):
    """View the logs of a docker-compose service."""
    command = "logs "

    if follow:
        command += "--follow "
    if tail:
        command += f"--tail={tail} "

    command += service
    docker_compose(context, command)


@task
def vscode(context):
    """Launch Visual Studio Code with the appropriate Environment variables to run in a container."""
    command = "code code.code-workspace"

    context.run(command)


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task
def cli(context):
    """Launch a bash shell inside the running Development container."""
    run_command(context, "zsh")


@task(
    help={
        "user": "name of the superuser to create (default: admin)",
    }
)
def createsuperuser(context, user="admin@psm.dev"):
    """Create a new Development superuser account (default: "admin"), will prompt for password."""
    command = f"division-server createsuperuser --email {user}"

    run_command(context, command)


@task(
    help={
        "name": "name of the migration to be created; if unspecified, will autogenerate a name",
    }
)
def collectstatic(context, name=""):
    """Perform makemigrations operation in Django."""
    command = "division-server collectstatic"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task(
    help={
        "name": "name of the migration to be created; if unspecified, will autogenerate a name",
    }
)
def makemigrations(context, name=""):
    """Perform makemigrations operation in Django."""
    command = "division-server makemigrations"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task
def migrate(context):
    """Perform migrate operation in Django."""
    command = "division-server migrate"

    run_command(context, command)


@task
def seed(context):
    """Perform load operation in Django using fixtures in the seed folder."""
    filenames = " ".join(g("seed/*.json"))
    command = f"division-server loaddata {filenames}"

    run_command(context, command)


# ------------------------------------------------------------------------------
# DOCS
# ------------------------------------------------------------------------------
@task
def docs(context):
    """Build and serve docs locally for development."""
    command = "mkdocs serve -v"

    if is_truthy(context.dev, context.local):
        print("Serving Documentation...")
        run_command(context, command)
    else:
        print("Only used when developing locally (i.e. context.dev context.local=True)!")


# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
@task(
    help={
        "autoformat": "Apply formatting recommendations automatically, rather than failing if formatting is incorrect.",
    }
)
def black(context, autoformat=False):
    """Check Python code style with Black."""
    if autoformat:
        black_command = "black"
    else:
        black_command = "black --check --diff"

    command = f"{black_command} ."

    run_command(context, command)


@task
def flake8(context):
    """Check for PEP8 compliance and other style issues."""
    command = "flake8 . --config .flake8"
    run_command(context, command)

@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting adheres to NTC defined standards."""
    # We exclude the /migrations/ directory since it is autogenerated code
    command = "pydocstyle ."
    run_command(context, command)


@task
def e2e(context):
    """Run end-2-end functional teests."""
    command = "division-server test e2e"
    run_command(context, command)


@task
def yamllint(context):
    """Run yamllint to validate formating adheres to NTC defined YAML standards.

    Args:
        context (obj): Used to run specific commands
    """
    command = "yamllint . --format standard"
    run_command(context, command)


@task
def unittest(context, keepdb=False, label="division", verbose=False, append=False, failfast=False, buffer=True):
    """Run  unit tests."""
    append_arg = " --append" if append else ""
    command = f"coverage run{append_arg} --module division.core.cli test {label}"
    command += " --config=division/core/tests/division_config.py"

    if keepdb:
        command += " --keepdb"
    if failfast:
        command += " --failfast"
    if buffer:
        command += " --buffer"
    if verbose:
        command += " --verbosity 2"
    run_command(context, command)


@task(
    help={
        "failfast": "fail as soon as a single test fails don't run the entire test suite",
    }
)
def tests(context, failfast=False):
    """Run all tests for this plugin."""
    # If we are not running locally, start the docker containers so we don't have to for each test
    if not is_truthy(context.dev, context.local):
        print("Starting Docker Containers...")
        start(context)
    # Sorted loosely from fastest to slowest
    print("Running black...")
    black(context)
    print("Running flake8...")
    flake8(context)
    print("Running pydocstyle...")
    pydocstyle(context)
    print("Running yamllint...")
    yamllint(context)
    print("Running unit tests...")
    unittest(context)
    # print("Running e2e tests...")
    # e2e(context)
    print("All tests have passed!")

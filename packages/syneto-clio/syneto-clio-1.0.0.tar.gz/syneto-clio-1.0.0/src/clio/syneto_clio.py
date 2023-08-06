import json
import os
import signal
import subprocess
import sys

import click

from clio.config import Config
from clio.prerequisites.remote_connections_utilities import RemoteConnectionsUtilities
from clio.shell import Shell
from clio.kube.container import Container
from clio.path import Path
from clio.sync import generate_command, generate_pantheon_command, sync_options
from clio import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


def handle_keyboard_interrupt(signal, frame):
    print("\nKeyboardInterrupt has been caught. Cleaning up...")
    return 0


@cli.command(help="Check status of all containers")
def check():
    command = "kubectl get pods"
    result = Shell.run(command).stdout
    click.echo(result)


@cli.command(help="Get the logs of the specified container")
@click.argument("name")
def logs(name):
    if name in ("giove", "diana"):
        command = f"journalctl -fu syneto-{name}"
    else:
        Container.check_existence(name)
        command = f"kubectl logs -f deployment/{name} -c {name}"
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    try:
        return Shell.run(command, without_stdout=True)
    except KeyboardInterrupt:
        return 0


@cli.command(help="Enter the specified container")
@click.argument("name")
def enter(name):
    if name in ("giove", "diana"):
        command = f"cd /usr/share/syneto-{name}"
    else:
        Container.check_existence(name)
        command = f"kubectl exec -it deployment/{name} -c {name} -- /bin/sh"
    return Shell.run(command, without_stdout=True)


@cli.command(help="Restart the specified container")
@click.argument("name")
def restart(name):
    if name in ("giove", "diana"):
        command = f"systemctl restart syneto-{name}.service"
    else:
        Container.check_existence(name)
        container_id = Container.get_id(name)
        command = f"docker container restart {container_id}"
    return Shell.run(command, without_stdout=True)


@cli.group(help="Cleanup development stuff not used anymore")
def cleanup():
    pass


@cleanup.command(help="Cleanup unnecessary docker images & containers")
def docker():
    Shell.run_cleanup_command("image")
    Shell.run_cleanup_command("container")


@cli.command(help="Save your remote SSH credentials for easier use of sync commands")
@click.option("--username", prompt=True, default="")
@click.option("--password", prompt=True, default="", hide_input=True)
@click.option("--ip", prompt=True, default="")
def config(username, password, ip):
    config_file = Config.create_file()
    if username is None or password is None or ip is None:
        click.echo("Missing SSH credentials. Please try again.")
        return
    if username == "" or password == "" or ip == "":
        click.echo("SSH credentials cannot be empty. Please try again.")
        return
    credentials = {"username": username, "password": password, "ip": ip}
    json.dump(credentials, config_file)
    try:
        subprocess.run([f"sudo sshpass -p {password} ssh {username}@{ip}"], shell=True)
    except Exception as e:
        raise Exception("Could not validate ssh credentials. Please try again.")


@cli.group(help="Synchronize your code")
def sync():
    pass


@sync.command(help="Sync giove code")
@sync_options
@click.argument("path")
@click.pass_context
def giove(ctx, path, username=None, password=None, ip=None):
    __check_config(ctx, username, password, ip)
    ip, username, password = __get_credentials()
    __check_remote_path_exists(username, ip, password, path)
    command = f"sshpass -p {password} rsync -azvh -e ssh {username}@{ip}:{path} /usr/share/syneto-giove"
    return Shell.run(command)


@sync.command(help="Sync minerva code")
@sync_options
@click.argument("path")
@click.pass_context
def minerva(ctx, path, username=None, password=None, ip=None):
    __check_config(ctx, username, password, ip)
    ip, username, password = __get_credentials()
    __check_remote_path_exists(username, ip, password, path)
    if not RemoteConnectionsUtilities.are_installed("minerva"):
        RemoteConnectionsUtilities.install("minerva")
    command = generate_command(username=username, ip=ip, password=password, path=path, service_name="minerva")
    return Shell.run(command)


@sync.command(help="Sync doorman code")
@sync_options
@click.argument("path")
@click.pass_context
def doorman(ctx, path, username=None, password=None, ip=None):
    __check_config(ctx, username, password, ip)
    ip, username, password = __get_credentials()
    __check_remote_path_exists(username, ip, password, path)
    if not RemoteConnectionsUtilities.are_installed("doorman"):
        RemoteConnectionsUtilities.install("doorman")
    command = generate_command(username=username, ip=ip, password=password, path=path, service_name="doorman")
    return Shell.run(command)


@sync.command(help="Sync diana code")
@sync_options
@click.argument("path")
@click.pass_context
def diana(ctx, path, username=None, password=None, ip=None):
    __check_config(ctx, username, password, ip)
    ip, username, password = __get_credentials()
    __check_remote_path_exists(username, ip, password, path)
    command = f"sshpass -p {password} rsync -azvh -e ssh {username}@{ip}:{path} /usr/share/syneto-diana"
    return Shell.run(command)


@sync.command(help="Sync pantheon code")
@sync_options
@click.argument("path")
@click.argument("project")
@click.pass_context
def pantheon(ctx, path, project, username=None, password=None, ip=None):
    __check_config(ctx, username, password, ip)
    ip, username, password = __get_credentials()
    __check_remote_path_exists(username, ip, password, path)
    if project == "minerva":
        if not RemoteConnectionsUtilities.are_installed(project):
            RemoteConnectionsUtilities.install(project)
        command = generate_pantheon_command(
            username=username, ip=ip, password=password, path=path, service_name=project
        )
    if project in ("giove", "diana"):
        command = f"sshpass -p {password} rsync -azvh -e ssh {username}@{ip}:{path} /usr/share/syneto-{project}/.venv/lib/python3.8/site-packages/pantheon/"

    return Shell.run(command)


def __check_config(ctx, username=None, password=None, ip=None):
    if (
        not os.path.isfile("/usr/config/syneto_clio_config.json")
        or os.path.getsize("/usr/config/syneto_clio_config.json") == 0
    ):
        if username is None or password is None or ip is None:
            click.echo("Missing SSH credentials. Please run the config command and try again.")
            sys.exit()
        ctx.invoke(config, username=username, password=password, ip=ip)


def __get_credentials():
    try:
        ip, username, password = Config.get_ssh_credentials()
        return ip, username, password
    except Exception as e:
        click.echo(f"Error encountered while trying to get credentials: {e}")
        sys.exit()


def __check_remote_path_exists(username, ip, password, path):
    if path == "":
        click.echo("Path cannot be empty.")
        sys.exit()
    if not Path.exists_remote(username + "@" + ip, password, path):
        click.echo("The given remote path does not exist. Plase try again.")
        sys.exit()


if __name__ == "__main__":
    cli()

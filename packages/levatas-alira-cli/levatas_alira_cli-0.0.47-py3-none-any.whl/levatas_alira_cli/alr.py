import os
import logging
import sys

from pathlib import Path

import click
from cryptography.hazmat.backends import default_backend
import docker

from click.utils import echo
from dateutil import tz

from alira_licensing.license import verify as verify_license
from levatas_alira_cli.diagnostics import Diagnostics

logging.basicConfig(level=logging.INFO)

HELP_TEXT_VOLUME = "Host's folder containing the configuration of the application"
HELP_TEXT_DOCKER = "Custom docker options to start the containers"
HELP_TEXT_PORT = "Starting port number"
HELP_TEXT_LOAD_FROM_FOLDER = "Local folder containing the docker images"
HELP_TEXT_SAVE_TO_FOLDER = "Folder where the images will be saved"
HELP_TEXT_LOCAL = "Whether cloud synchronization will be disabled"

DEFAULT_PORT = 21000
DEFAULT_VOLUME_PATH = Path(os.path.abspath(""))
NETWORK_NAME = "alira"


class CLI(object):
    """Class containing all of the command line interface commands."""

    def __init__(self, license_data, platform_version, descriptors, client, volume):
        self.platform_version = platform_version
        self.descriptors = descriptors
        self.client = client
        self.volume = volume
        self.github_user = license_data["metadata"]["GITHUB_REPOSITORY_ACCESS_USER"]
        self.github_token = license_data["metadata"]["GITHUB_REPOSITORY_ACCESS_TOKEN"]
        self.not_valid_after = license_data["not_valid_after"]

    def status(self):
        """Displays the status of the installation."""

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = self.not_valid_after.replace(tzinfo=from_zone)
        local_datetime = utc.astimezone(to_zone)

        if self.platform_version:
            click.echo(f"Platform version: ", nl=False)
            click.secho(f"{self.platform_version}", fg="cyan")

        click.echo("License valid until: ", nl=False)
        click.secho(f"{local_datetime.strftime('%b %d, %Y')}\n", fg="cyan")

        upgrade_messages = []

        for descriptor in self.descriptors.values():
            if descriptor["image"]:
                click.echo(f"* {descriptor['name']} {descriptor['version']}", nl=False)

                container = self._get_container(descriptor)
                if container and container.status == "running":
                    ports = self._get_container_ports(descriptor, container=container)
                    click.secho(
                        f" (running on {self._format_ports(ports)})", fg="green"
                    )
                else:
                    click.secho(" (not running)", fg="yellow")

                # If we find that any of the modules is not upgraded, we need
                # to prepare a message to display to the user.
                if self._is_upgrade_warning_necessary(descriptor):
                    upgrade_messages.append(
                        f"* {descriptor['name']} from version {descriptor['version']} to {descriptor['license_version']}"
                    )

            else:
                click.echo(f"* {descriptor['name']}", nl=False)
                click.secho(" (not installed)", fg="cyan")

        click.echo()

        if len(upgrade_messages) > 0:
            click.secho("WARNING ", fg="red", nl=False)
            click.echo(
                "The installed version of the following modules doesn't match the version"
            )
            click.echo(
                "specified in the license file and should be upgraded. Use ", nl=False
            )
            click.secho("alr setup ", fg="bright_yellow", nl=False)
            click.echo("to upgrade")
            click.echo("to the latest version:")
            click.echo()
            for message in upgrade_messages:
                click.echo(message)

            click.echo()

    def setup(self, ctx, folder):
        """Installs or upgrades the application."""

        self.stop(ctx, silent=True)

        # for image_name, descriptor in self.descriptors.items():
        #     if descriptor["version"] is not None:
        #         self._remove_container(
        #             image_name,
        #             descriptor,
        #             outdated_only=True,
        #             remove_image=True,
        #             silent=False,
        #         )

        self._install_packages(folder, force_upgrade=True)

        self._update_system_status(ctx)
        self.status()

    def start(self, ctx, local, port, docker_client, silent=False):
        """Starts the application."""

        if not self._is_every_package_installed():
            click.echo("The application is not installed. Use ", nl=False)
            click.secho("alr setup ", fg="bright_yellow", nl=False)
            click.echo("to install it.")
            return

        port_number = port
        for image_name, descriptor in self.descriptors.items():

            ports_mapping = {}
            if descriptor["binding"]:
                for port in descriptor["ports"]:
                    ports_mapping[port] = port_number
                    port_number += 1

            docker_params = [
                params[len(f"{descriptor['name']} ") :]
                for params in docker_client
                if params.startswith(f"{descriptor['name']} ")
            ]

            redis_params = list(filter(lambda p: "-e REDIS=" in p, docker_params))

            if len(docker_params) > 0 and len(redis_params) == 0 and not local:
                docker_params[0] += " -e REDIS=redis://redis:6379/1"

            self._start_container(
                image_name, descriptor, local, ports_mapping, docker_params
            )

        if not silent:
            click.echo()
            self._update_system_status(ctx)
            self.status()

    def stop(self, ctx, silent=False):
        """Stops the application."""

        for container in self._get_running_containers():
            click.echo(f"Stopping {container.name}...")

            try:
                container.stop()
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(f"Unexpected error occurred when stopping {container.name}")

        if not silent:
            click.echo()
            self._update_system_status(ctx)
            self.status()

    def restart(self, ctx, local, port, docker_client):
        """Restarts the application."""

        self.stop(ctx, silent=True)
        self.start(ctx, local, port, docker_client, silent=True)

        click.echo()
        self._update_system_status(ctx)
        self.status()

    def uninstall(self, ctx):
        """Uninstalls the solution."""

        self.stop(ctx, silent=True)

        for image_name, descriptor in self.descriptors.items():
            self._remove_container(
                image_name, descriptor, outdated_only=False, remove_image=True
            )

        try:
            network = self.client.networks.get(NETWORK_NAME)
            network.remove()
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError:
            click.echo(
                f"Couldn't remove network {NETWORK_NAME}. Remove the network manually "
                "after removing any attached containers."
            )
        except Exception:
            pass

        click.echo()
        self._update_system_status(ctx)
        self.status()

    def remove(self, ctx):
        """Removes any container related to the solution."""

        self.stop(ctx, silent=True)

        for image_name, descriptor in self.descriptors.items():
            self._remove_container(
                image_name, descriptor, outdated_only=False, remove_image=False
            )

        click.echo()
        self._update_system_status(ctx)
        self.status()

    def save(self, folder):
        """Saves the application packages as tar files."""

        if folder is None:
            folder = ""

        if not self._is_every_package_installed():
            click.echo("The application is not installed. Use ", nl=False)
            click.secho("alr setup ", fg="bright_yellow", nl=False)
            click.echo("to install it.")
            return

        try:
            for descriptor in self.descriptors.values():
                click.echo(f"Saving {descriptor['name']} to {folder}...")

                if not descriptor["image"]:
                    continue

                try:
                    image = self.client.images.get(CLI._registry(descriptor["image"]))
                    f = open(os.path.join(folder, f"{descriptor['name']}.tar"), "wb")
                    for chunk in image.save():
                        f.write(chunk)
                    f.close()
                except docker.errors.APIError as exception:
                    logging.exception(exception)
                    click.echo(
                        f"Unexpected error ocurred when saving image "
                        f"{descriptor['name']}"
                    )
        except Exception as exception:
            logging.exception(exception)
            click.echo("There was an unexpected error when saving images.")

    def diagnose(self, ctx):
        """
        Runs the configured diagnostics and displays the results.
        """

        volume = ctx.obj["volume"]
        configuration = os.path.join(volume, "diagnostics.yml")

        if not os.path.isfile(configuration):
            click.echo('The file "diagnostics.yml" doesn\'t exist.')
            click.echo()
            return

        result = Diagnostics(configuration=configuration).run()
        if not result:
            click.echo("There aren't any diagnostics configured.")
            click.echo()
            return

        click.secho("Platform diagnostics", fg="cyan", bold=True)
        click.echo()

        for diagnostic in result:
            status = "OKAY" if diagnostic["status"] else "FAILED"
            click.echo(f"• {diagnostic['label']: <50}", nl=False)
            click.secho(status, fg="green" if diagnostic["status"] else "red")

        click.echo()

    def _is_upgrade_warning_necessary(self, descriptor):
        """
        Returns True if there's a version mistmatch between the module installed
        and the version specified in the license file.

        Returns False if we can't determine whether upgrading is necessary. For
        example, if the license specifies `latest`, we can't determine whether
        the current version needs to be upgraded.
        """

        if not descriptor["version"]:
            return False

        license_version_components = descriptor["license_version"].split(".")
        installed_version_components = descriptor["version"].split(".")
        # ignore v if present in license but not in installed version
        if license_version_components[0].startswith("v") and not installed_version_components[0].startswith("v"):
            license_version_components[0] = license_version_components[0][1:]

        if len(license_version_components) == len(installed_version_components):
            if license_version_components != installed_version_components:
                return True

        if len(license_version_components) > len(installed_version_components):
            return True

        return False

    def _is_latest_version_installed(self, descriptor):
        if not descriptor["version"]:
            return False

        if descriptor["license_version"] != descriptor["version"]:
            return False

        return True

    def _install_packages(self, folder, container=None, force_upgrade=False):
        """Download and install the specified container. If the container is not
        specified, install all the containers specified in the license."""

        if folder is None:
            if self._login(user=self.github_user, token=self.github_token):
                self._download(container, force_upgrade)
            else:
                click.echo("An error ocurred while authenticating with docker.")
        else:
            self._load(folder)

        try:
            networks = self.client.networks.list(names=[NETWORK_NAME])

            if len(networks) == 0:
                self.client.networks.create(NETWORK_NAME, driver="bridge")
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo(f"Unexpected error ocurred when creating network {NETWORK_NAME}")

    def _is_every_package_installed(self):
        """Checks if all packages specified in the license are installed."""

        for descriptor in self.descriptors.values():
            if not descriptor["image"]:
                return False

        return True

    def _start_container(
        self, image_name, descriptor, local, ports_mapping, docker_params
    ):
        container = self._get_container(descriptor)
        if container and container.status == "running":
            return

        self._remove_container(
            image_name, descriptor, outdated_only=False, remove_image=False, silent=True
        )

        click.echo(f"Starting {descriptor['name']}...")

        if len(docker_params):
            ports = (
                [
                    f"-p {external}:{internal.split('/')[0]}"
                    for internal, external in ports_mapping.items()
                ]
                if ports_mapping is not None
                else []
            )

            params = [
                "docker",
                "container",
                "run",
                "-it",
                "--detach",
                "--name",
                descriptor["name"],
                f"--network {NETWORK_NAME}",
                f"--network-alias {descriptor['name']}",
            ]

            for package_volume in descriptor["volumes"]:
                params.extend(["-v", f"{package_volume[0]}:{package_volume[1]}"])

            for env in descriptor["environment"]:
                params.extend(["-e", env])

            params.extend(
                [
                    *ports,
                    *" ".join(docker_params).split(" "),
                    "--restart=always",
                    descriptor["registry"],
                ]
            )

            try:
                print(" ".join(params))
                result = os.system(" ".join(params))
                print(result)
            except Exception as e:
                logging.exception(e)
                click.echo(f"Unexpected error occurred starting {descriptor['name']}")
        else:
            try:
                volumes = dict()
                for package_volume in descriptor["volumes"]:
                    volumes[package_volume[0]] = {
                        "bind": package_volume[1],
                        "mode": "rw",
                    }

                environment = ["REDIS=redis://redis:6379/1"] if not local else []
                environment.extend(descriptor["environment"])

                self.client.containers.run(
                    name=descriptor["name"],
                    image=descriptor["registry"],
                    detach=True,
                    remove=False,
                    restart_policy={"Name": "always"},
                    volumes=volumes,
                    ports=ports_mapping,
                    stdin_open=True,
                    stdout=True,
                    stderr=True,
                    tty=True,
                    environment=environment,
                )
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(f"Unexpected error occurred starting {descriptor['name']}")

            try:
                networks = self.client.networks.list(names=[NETWORK_NAME])
                if len(networks) > 0:
                    network = networks[0]
                    network.connect(descriptor["name"], aliases=[descriptor["name"]])
            except docker.errors.APIError as exception:
                # This exception is expected if the container is already connected
                # to the network.
                pass

        ports = self._get_container_ports(descriptor)
        if len(ports) > 0:
            click.echo(
                f"Successfully started {descriptor['name']} using {self._format_ports(ports)}"
            )
        else:
            click.echo(f"Successfully started {descriptor['name']}")

    def _remove_container(
        self,
        image_name,
        descriptor,
        outdated_only=False,
        remove_image=False,
        silent=False,
    ):
        if outdated_only and self._is_latest_version_installed(descriptor):
            return

        if not silent:
            click.echo(f"Removing {descriptor['name']} {descriptor['version']}...")

        try:
            container = self.client.containers.get(descriptor["name"])
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo(
                f"Unexpected error ocurred when removing container {descriptor['name']}"
            )

        if remove_image:
            images = self.client.images.list(name=image_name)
            for image in images:
                try:
                    self.client.images.remove(image.id, force=True)
                except docker.errors.APIError as exception:
                    logging.exception(exception)
                    click.echo(
                        "Unexpected error ocurred when removing "
                        f"image {descriptor['name']}"
                    )

        try:
            networks = self.client.networks.list(names=[NETWORK_NAME])
            if len(networks) > 0:
                network = networks[0]
                network.disconnect(descriptor["name"], force=True)
        except docker.errors.APIError as exception:
            # This exception is expected if the container is already disconnected
            # from the network.
            pass

    def _get_container_ports(self, descriptor, container=None):
        ports = []

        if container is None:
            container = self._get_container(descriptor)

        if container:
            if descriptor["binding"]:
                port_bindings = container.attrs["HostConfig"]["PortBindings"]
                for binding_key in port_bindings:
                    for binding in port_bindings[binding_key]:
                        ports.append(
                            f'{int(binding["HostPort"])}:{int(binding_key.replace("/tcp", ""))}'
                        )
            else:
                for port in container.attrs["NetworkSettings"]["Ports"].keys():
                    ports.append(int(port.replace("/tcp", "")))

        return ports

    def _get_container(self, descriptor):
        try:
            container = self.client.containers.get(descriptor["name"])
        except docker.errors.NotFound:
            container = None

        if container:
            return container

        for container in self.client.containers.list():
            registry_image_name = CLI._registry(container)
            image_name = registry_image_name.split(":")[0]

            if image_name == descriptor["identifier"]:
                return container

        return None

    def _get_running_containers(self):
        identifiers = [
            descriptor["identifier"] for descriptor in self.descriptors.values()
        ]

        containers = []
        for container in self.client.containers.list():
            registry_image_name = CLI._registry(container)
            image_name = registry_image_name.split(":")[0]

            if image_name in identifiers and container.status == "running":
                containers.append(container)

        return containers

    def _format_ports(self, ports):
        if len(ports) == 1:
            return f"port {ports[0]}"

        return "ports " + ", ".join([str(p) for p in ports])

    def _download(self, container=None, force_upgrade: bool = False):
        for image_name, descriptor in self.descriptors.items():
            if not force_upgrade and descriptor["image"]:
                continue

            if container and descriptor["name"] != container:
                continue

            if self._is_latest_version_installed(descriptor):
                click.echo(
                    f"{descriptor['name']} is up to date. "
                    f"Version: {descriptor['license_version']}"
                )
                continue

            click.echo(
                f"Downloading {descriptor['name']} {descriptor['license_version']}... ",
                nl=False,
            )

            try:
                descriptor_image = descriptor["package"]["image"]
                for line in self.client.api.pull(
                    descriptor_image, stream=True, decode=True
                ):
                    if "progress" in line:
                        message = f"{line['status']} - {line['progress']}"
                        print(message, end="\r")
                    elif "status" in line:
                        message = line["status"]
                        print(message, end="\r")
                    elif "errorDetail" in line:
                        message = line["errorDetail"].get("message", "Error")
                        click.echo(message)
                        sys.exit(1)

                click.echo()

                click.echo(
                    f"{descriptor['name']} version {descriptor['license_version']} was "
                    "successfully downloaded"
                )
                click.echo()
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(
                    f"Unexpected error occurred downloading {descriptor['name']}"
                )

    def _load(self, folder):
        if not os.path.exists(folder):
            click.echo(f"The specified folder {folder} does not exist.")
            return

        for descriptor in self.descriptors.values():
            image_file = os.path.join(folder, f"{descriptor['name']}.tar")

            try:
                with open(image_file, mode="rb") as file:
                    click.echo(
                        f"Loading {descriptor['name']} from file '{image_file}'..."
                    )
                    self.client.images.load(file.read())
                    click.echo(f"{descriptor['name']} successfully loaded.")
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(f"Unexpected error occurred loading {descriptor['name']}")

    def _login(self, user, token):
        try:
            result = self.client.login(
                username=user, password=token, registry="ghcr.io"
            )

            return ("Status" in result and result["Status"] == "Login Succeeded") or (
                result["username"] == user and result["password"] == token
            )
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo("Unexpected error occurred when attempting to login")

    def _update_system_status(self, ctx):
        volume = ctx.obj.get("volume", None)
        docker_client = docker.from_env()
        license_data, platform_version, descriptors = CLI._get_system_status(
            docker_client, volume
        )

        self.platform_version = platform_version
        self.descriptors = descriptors
        self.license_data = license_data

    @staticmethod
    def initialize(ctx, volume=None):
        if volume is None:
            volume = ctx.obj.get("volume", None)

        ctx.obj["volume"] = volume

        try:
            docker_client = docker.from_env()
            license_data, platform_version, descriptors = CLI._get_system_status(
                docker_client, volume
            )
            ctx.obj["CLI"] = CLI(
                license_data=license_data,
                platform_version=platform_version,
                descriptors=descriptors,
                client=docker_client,
                volume=volume,
            )
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo("There was an error trying to access the Docker service.")
            click.secho(exception, err=True, fg="red")
            sys.exit(1)

    @staticmethod
    def _get_system_status(client, volume):
        license_data = CLI._verify(volume)

        platform_version = license_data["metadata"].get("PLATFORM_VERSION", "")

        descriptors = {}

        for item in license_data["metadata"]["PACKAGES"]:
            package_name = item["name"]
            model = item.get("model", None)

            package_volumes = []

            if "volumes" not in item:
                # The license doesn't specify the volumes that we want to map, so we
                # need to set up the default ones.
                if model:
                    # If this package is a model, we need to map the model-specific folder
                    # to /opt/ml/model.
                    package_volumes.append(
                        (os.path.join(volume, model), "/opt/ml/model")
                    )
                else:
                    # If this package is not a model, we need to map the $volume folder
                    # to /opt/ml/model.
                    package_volumes.append((volume, "/opt/ml/model"))
            else:
                volume_descriptor = item["volumes"]
                volume_mappings = volume_descriptor.split(",")
                for volume_mapping in volume_mappings:
                    volume_mapping = volume_mapping.strip()
                    host, container = volume_mapping.split(":")

                    # If the host path uses the $volume variable, we need to replace it
                    # with the actual volume path.
                    if "$volume" in host:
                        host = host.replace("$volume", str(volume))

                    # If the host path uses the $model variable, we need to replace it
                    # with the actual model-specific path.
                    if "$model" in host:
                        host = host.replace("$model", os.path.join(volume, model))

                    package_volumes.append((host, container))

            environment = CLI._get_environment_variables(item.get("environment", []))
            if environment is None:
                sys.exit(1)

            image_name = item["image"].split(":")[0]
            license_version = item["image"].split(":")[1]

            descriptors[image_name] = {
                "identifier": image_name,
                "package": item,
                "name": package_name,
                "license_version": license_version,
                "version": None,
                "volumes": package_volumes,
                "registry": item["image"],
                "image": None,
                "binding": item.get("binding", False),
                "environment": environment,
            }

        if client and client.images:
            images = client.images.list()

            # search for duplicate image names with different versions
            all_images = {}
            for image in images:
                image_name = image.tags[0].split(":")[0]
                if image_name in all_images:
                    all_images[image_name].append(image)
                else:
                    all_images[image_name] = [image]
            # delete images that have more than one version
            # will download the version specified in the license
            for image_name, images in all_images.items():
                if len(images) > 1:
                    click.echo(f"Found {len(images)} versions of {image_name}. Deleting duplicates...")
                    for duplicate_image in images:
                        client.images.remove(duplicate_image.id)

            for container_image in client.images.list():
                if len(container_image.tags) == 0:
                    continue

                image_name = container_image.tags[0].split(":")[0]
                installed_version = container_image.tags[0].split(":")[1]

                if (
                    "Config" in container_image.attrs
                    and container_image.attrs["Config"]
                ):
                    if (
                        "Labels" in container_image.attrs["Config"]
                        and container_image.attrs["Config"]["Labels"]
                    ):
                        if (
                            "org.opencontainers.image.version"
                            in container_image.attrs["Config"]["Labels"]
                        ):
                            installed_version = container_image.attrs["Config"][
                                "Labels"
                            ]["org.opencontainers.image.version"]

                if image_name in descriptors:
                    descriptors[image_name]["image"] = container_image
                    descriptors[image_name]["version"] = installed_version

                    if descriptors[image_name]["binding"]:
                        exposed_ports = (
                            container_image.attrs["Config"]["ExposedPorts"]
                            if "ExposedPorts" in container_image.attrs["Config"]
                            else {}
                        )

                        descriptors[image_name]["ports"] = [
                            port for port in exposed_ports
                        ]
        return license_data, platform_version, descriptors

    @staticmethod
    def _get_environment_variables(environment):
        if len(environment) == 0:
            return environment

        result = []

        for env in environment:

            # If the environment variable comes with a value, we can add it to
            # the list and move on to the next.
            if "=" in env:
                result.append(env)
                continue

            # If the environment variable doesn't come with a value, we need to
            # get it from the current environment.
            env_value = os.environ.get(env, None)
            if env_value is None:
                click.echo("Environment variable ", nl=False)
                click.secho(f"{env}", fg="cyan", nl=False)
                click.secho(
                    " is not set. This variable is needed to run one of the packages specified in the license."
                )
                click.echo("Use ", nl=False)
                click.secho(f'export {env}="[VALUE]" ', fg="cyan", nl=False)
                click.echo("to create the environment variable.")
                return None

            result.append(f"{env}={env_value}")

        return result

    @staticmethod
    def _verify(volume):
        if not os.path.isfile(os.path.join(volume, "license.pem")):
            click.echo(
                "license.pem file not found. You can either copy the license.pem "
                "file in the current directory, or specify its location using the "
                "--volume argument."
            )
            sys.exit(1)

        if not os.path.isfile(os.path.join(volume, "public.pem")):
            click.echo(
                "public.pem file not found. You can either copy the public.pem "
                "file in the current directory, or specify its location using the "
                "--volume argument."
            )
            sys.exit(1)

        return verify_license(directory=volume)

    @staticmethod
    def _registry(package):
        if "RepoTags" in package.attrs and len(package.attrs["RepoTags"]):
            return package.attrs["RepoTags"][0]

        return package.attrs["Config"]["Image"]


@click.group()
@click.option(
    "--volume",
    "-v",
    help=HELP_TEXT_VOLUME,
    envvar="ALIRA_VOLUME",
    default=DEFAULT_VOLUME_PATH,
)
@click.version_option()
@click.pass_context
def cli(ctx, volume):
    ctx.ensure_object(dict)
    CLI.initialize(ctx, volume)


@cli.command()
@click.pass_context
def status(ctx):
    """Display license and version information of each package."""
    ctx.obj["CLI"].status()


@cli.command()
@click.option("--folder", "-f", help=HELP_TEXT_LOAD_FROM_FOLDER, default=None)
@click.pass_context
def setup(ctx, folder):
    """Installs the solution."""
    ctx.obj["CLI"].setup(ctx, folder)


@cli.command()
@click.option("--local/--no-local", help=HELP_TEXT_LOCAL, default=False)
@click.option("--port", "-p", help=HELP_TEXT_PORT, default=DEFAULT_PORT)
@click.option("--docker", "-d", multiple=True, help=HELP_TEXT_DOCKER, default=[])
@click.pass_context
def start(ctx, local, port, docker):
    """Starts the solution."""
    ctx.obj["CLI"].start(ctx, local, port, docker_client=docker)


@cli.command()
@click.option("--local/--no-local", help=HELP_TEXT_LOCAL, default=False)
@click.option("--port", "-p", help=HELP_TEXT_PORT, default=DEFAULT_PORT)
@click.option("--docker", "-d", multiple=True, help=HELP_TEXT_DOCKER, default=[])
@click.pass_context
def restart(ctx, local, port, docker):
    """Restarts the running containers."""
    ctx.obj["CLI"].restart(ctx, local, port, docker_client=docker)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stops the running containers."""
    ctx.obj["CLI"].stop(ctx)


@cli.command()
@click.pass_context
def diagnose(ctx):
    """Diagnoses the current status of the installation."""
    ctx.obj["CLI"].diagnose(ctx)


def uninstall_cancelled_callback(ctx, param, value):
    if not value:
        click.echo("The uninstall operation was cancelled.")
        sys.exit(1)


@cli.command()
@click.option(
    "--yes",
    is_flag=True,
    callback=uninstall_cancelled_callback,
    expose_value=False,
    prompt="Are you sure you want to uninstall the solution?",
)
@click.pass_context
def uninstall(ctx):
    """Uninstalls the solution."""
    ctx.obj["CLI"].uninstall(ctx)


@cli.command()
@click.pass_context
def remove(ctx):
    """Removes the containers."""
    ctx.obj["CLI"].remove(ctx)


@cli.command()
@click.option("--folder", "-f", help=HELP_TEXT_SAVE_TO_FOLDER, default=None)
@click.pass_context
def save(ctx, folder):
    """Saves images as tar files."""
    ctx.obj["CLI"].save(folder)


@cli.command()
@click.argument("subcommand", required=False)
@click.pass_context
def help(ctx, subcommand=None):
    subcommand_obj = cli.get_command(ctx, subcommand)
    if subcommand_obj is None:
        click.echo(cli.get_help(ctx))
    else:
        click.echo(subcommand_obj.get_help(ctx))

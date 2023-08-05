import click

from indico_install.cluster_manager import (
    ClusterManager,
    get_default_namespace
)
from indico_install.config import D_PATH
from indico_install.helm.render import render, render_from_local, _resolve_remote
from indico_install.utils import run_cmd, string_to_tag


default_namespace = get_default_namespace(ClusterManager().cluster_config, "defaultNamespace")

ANCHORE_CLI_URL="https://anchore-engine.indico.domains/anchore/v1/"
ANCHORE_CLI_USER="admin"

def get_scan_result():
    click.echo("In order to get the scan results for these images, youu will need the following")
    click.echo("anchore-cli installed with `pip install anchorecli`")
    click.echo("ENV: ANCHORE_CLI_URL, ANCHORE_CLI_USER, ANCHORE_CLI_PASS")
    click.echo("If the image is from gcr.io/new-indico, it should have a scan result. Run the following:")
    click.echo("anchore-cli image vuln <IMAGE_NAME> all | awk '{print $3}' | grep -e 'Critical' -e 'High' -e 'Medium' -e 'Low' | sort |  uniq -c")
    click.echo("This can be run on all of the images in a table by copying the output to a test.txt file and running:")
    click.echo("for f in $(cat test.txt | awk '{print $2}' | sed 's/\"//g' | sort | uniq); do echo \"$f\"; anchore-cli image vuln \"$f\" all | awk '{print $3}' | grep -e 'Critical' -e 'High' -e 'Medium' -e 'Low' | sort |  uniq -c ; done")

def output_table(results):
    # First get the proper size for the columns
    columns = results[0].keys()
    column_sizes = {}
    for column in columns:
        column_sizes[column] = [len(column)]

    for result in results:
        for column in columns:
            column_sizes[column].append(len(result[column]))

    for column in columns:
        column_sizes[column] = max(column_sizes[column]) + 2

    # Now we make the output

    format_string = ""
    for column in columns:
        format_string += f"{{:<{column_sizes[column]}}} "
    
    print(format_string.format(*list(columns)))
    for result in results:
        values = [result[i] for i in columns]
        print(format_string.format(*values))


@click.group("snapshot")
def snapshot():
    """Manage snapshots of current images"""
    pass


@snapshot.command("current")
@click.pass_context
def current_images(ctx):
    """
    Display images currently in the cluster (deployments/statefulsets/cronjobs)
    """
    click.echo("Gathering Deployments...")
    deployments = run_cmd(
        f"kubectl get deployments --no-headers | awk '{{print $1}}'",
        silent=True
    )
    deployment_array = deployments.split('\n')
    deployment_result = []
    for deployment in deployment_array:
        images = run_cmd(
            f"kubectl get deployment {deployment} -o yaml | grep 'image:' | sed 's/image:/ /g' | sed 's/- //g' | sed 's/ //g' | sort | uniq",
            silent=True
        )
        image_array = images.split('\n')
        for image in image_array:
            deployment_result.append({
                "name": deployment, 
                "image": image,
            })
    click.echo("Gathering Statefulsets...")
    statefulsets = run_cmd(
        f"kubectl get statefulsets --no-headers | awk '{{print $1}}'",
        silent=True
    )
    statefulset_array = statefulsets.split('\n')
    statefulset_result = []
    for statefulset in statefulset_array:
        images = run_cmd(
            f"kubectl get statefulset {statefulset} -o yaml | grep 'image:' | sed 's/image:/ /g' | sed 's/- //g' | sed 's/ //g' | sort | uniq",
            silent=True
        )
        image_array = images.split('\n')
        for image in image_array:
            statefulset_result.append({
                "name": statefulset, 
                "image": image,
            })
    click.echo("Gathering Cronjobs...")
    cronjobs = run_cmd(
        f"kubectl get cronjobs --no-headers | awk '{{print $1}}'",
        silent=True
    )
    cronjob_array = cronjobs.split('\n')
    cronjob_result = []
    for cronjob in cronjob_array:
        images = run_cmd(
            f"kubectl get cronjob {cronjob} -o yaml | grep 'image:' | sed 's/image:/ /g' | sed 's/- //g' | sed 's/ //g' | sort | uniq",
            silent=True
        )
        image_array = images.split('\n')
        for image in image_array:
            cronjob_result.append({
                "name": cronjob, 
                "image": image,
            })

    print()
    output_table(deployment_result)
    print()
    output_table(statefulset_result)
    print()
    output_table(cronjob_result)

    print()
    get_scan_result()

@snapshot.command("configmap")
@click.pass_context
def configmap_images(ctx):
    """
    Display images in the template generated from the cluster's current configmap
    """
    cluster_manager = ClusterManager()
    cluster_manager.set_default_namespace()

    ctx.invoke(
        render,
        cluster_manager=cluster_manager,
        allow_image_overrides=False,
    )

    generated = D_PATH / "generated"

    images = run_cmd(
        f" grep -r 'image:' {generated} | sed 's/ //g' | sed 's/image:/ /g' | sed 's/: / /g' | sort | uniq",
        silent=True
    )
    image_list = images.split('\n')
    result = []
    for image in image_list:
        file_name, image_name = image.split(' ')
        result.append({
            "name": file_name, 
            "image": image_name,
        })
    print()
    output_table(result)

    print()
    get_scan_result()

@snapshot.command("template")
@click.pass_context
@click.option("-v", "--version", required=True, help="Version of IPA that you want the snapshot for")
def template_images(ctx, version):
    """
    Get the images in the template for a particular IPA version
    """
    version = string_to_tag(version) if version else None

    cluster_manager = ClusterManager()
    cluster_manager.set_default_namespace()

    cluster_manager.indico_version = version

    ctx.invoke(
        render,
        cluster_manager=cluster_manager,
        allow_image_overrides=False,
    )

    generated = D_PATH / "generated"

    images = run_cmd(
        f" grep -r 'image:' {generated} | sed 's/ //g' | sed 's/image:/ /g' | sed 's/: / /g' | sort | uniq",
        silent=True
    )
    image_list = images.split('\n')
    result = []
    for image in image_list:
        file_name, image_name = image.split(' ')
        result.append({
            "name": file_name, 
            "image": image_name,
        })
    print()
    output_table(result)

    print()
    get_scan_result()

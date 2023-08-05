import click
from drb_impl_odata.exceptions import OdataRequestException
from requests.auth import HTTPBasicAuth

from download_manager.download_manager import DownloadManager
from download_manager.progress.tdqm_progress_manager import TqdmLoggingHandler
from download_manager.run.trigger import ContinuousTrigger

import logging

logger = logging.getLogger("download_manager")
logger.setLevel(logging.INFO)
logger.addHandler(TqdmLoggingHandler())


'''
TODO::
@click.option('--max-tries', '-m', type=int, default=5,
              help="Number of tries (default: 5).")
@click.option('--retry-wait', type=int, default=15,
              help="Seconds to wait between retries (default: 15s).")
@click.option('--timeout', type=int, default=120,
              help="Connection timeout in seconds (default: 120s).")
@click.option('--quota-max-connections', type=int, default=0,
              help="Maximum of number connections. 0: unlimited (default: 0).")
@click.option('--quota-max-bandwidth', type=int, default=0,
              help="Maximum of bandwidth usage. 0: unlimited (default: 0).")
'''
tool_name = "download_manager"


@click.command(help=f"""
Manage transfer of data from internet. {tool_name} supports parallel and
partial transfers, and it is able to resume interrupted downloads.
It is able to handle all protocol supported by DRB, including OData (CSC,
DataHub and DIAS API declinations) for LTA and AIP.
It authorize limiting the connections to respect the services quota policies.
""")
@click.option('--service', '-s', type=str, help='Service to requests data',
              required=True)
@click.option('--filter', '-f', type=str,
              help="Filter to apply to requests "
                   "products by default only online products are requested.")
@click.option('--order', '-O', type=str, help="Sort query (ASC or DESC).")
@click.option('--username', '-u', type=str,
              help="Service connection username.")
@click.option('--password', '-p', type=str,
              help="Service connection password.")
@click.option('--process_number', '-P', type=int, default=2,
              help="Number of parallel download threads (default:2).")
@click.option('--limit', '-l', type=int,
              help="Limit the number matching products (default: 10)",
              default=10)
@click.option('--output', '-o', type=str, default="",
              help='The directory to store the downloaded files.')
@click.option('--quiet', '-q', is_flag=True,
              help="Silent mode: only errors are reported.")
@click.option('--chunk_size', '-c', type=int, default=4194304,
              help="The size of downloaded chunks (default: 4194304 Bytes).")
@click.option('--verify', '-v', is_flag=True,
              help="Check file integrity by hashes.")
@click.option('--resume', '-r', is_flag=True,
              help="Resume downloading a partially downloaded file.")
@click.option('--database', '-d', type=str, default=None,
              help="Folder to store the database if not present the database"
                   "will be in a folder in the home directory.")
@click.option('--storage_limit_size', '-S', type=int, default=None,
              help="The size max of file to download.")
@click.option('--continuous', '-C', is_flag=True,
              help=" When present the download keep "
                   "going download package by package.")
@click.option('--bulk', '-b', default=None,
              help=" path to a csv file containing "
                   "name of products to downloads")
def cli(service, process_number, username, password, chunk_size,
        filter, limit, quiet, output, order, verify, resume, database,
        storage_limit_size, continuous, bulk):

    if quiet:
        logger.setLevel(logging.WARNING)

    dm = DownloadManager(service=service,
                         auth=HTTPBasicAuth(username, password),
                         database_folder=database,
                         output_folder=output,
                         process_number=process_number,
                         chunk_size=chunk_size,
                         quiet=quiet,
                         verify=verify,
                         resume=resume,
                         storage_limit_size=storage_limit_size)

    dm.start()

    if continuous:
        continuous_trigger = ContinuousTrigger(dm)
        # TBC (run parameter to affine
        continuous_trigger.run(filter)
    else:
        nodes = dm.find_nodes(source=dm.source,
                              filter=filter,
                              limit=limit,
                              order=order,
                              bulk=bulk)

        for node in nodes:
            try:
                logger.info(f"Submitting {node.path.path} - {node.name}")
            except OdataRequestException:
                logger.info(f"Error with node {node}")
                nodes.remove(node)
            try:
                dm.submit(node, verify)
            except Exception as e:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.error(f"Error while submitting {node.name}", e)
                else:
                    logger.error(
                        f"Error while submitting {node.name}: {str(e)}")

    dm.join()
    dm.stop()

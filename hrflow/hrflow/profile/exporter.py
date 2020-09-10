from libs.exporter.exporter.supervisor import Supervisor


class ProfileExporter(object):
    """
    Class that interacts with hrflow API profiles endpoint.
    """

    def __init__(self, client):
        """
        Initialize Exporter object with hrflow client.

        Args:
            client: hrflow client instance <hrflow object>

        Returns
            Exporter instance object.

        """
        self.client = client

    def download(self, source_ids, target, v_level=None, n_worker=3, logfile=None):
        """Use the api to add a new profile using profile_data."""
        export_supervisor = Supervisor(client=self.client, source_ids=source_ids, target=target, v_level=v_level,
                                       n_worker=n_worker, logfile=logfile)
        export_supervisor.start()
        return True

from libs.importer.importer.supervisor import Supervisor


class ProfileImporter(object):
    """
    Class that interacts with hrflow API profiles endpoint.

    """

    def __init__(self, client):
        """
        Initialize Profile object with hrflow client.

        Args:
            client: hrflow client instance <hrflow object>

        Returns
            Profile instance object.

        """
        self.client = client

    def upload(self, source_id, target, timestamp_reception=None, is_recurcive=True, silent=False, verbose=True, sleep=1,
            n_worker=3, logfile=None):
        """
        Use the api to add a new profile using profile_data.
        """
        import_supervisor = Supervisor(client=self.client, source_id=source_id, target=target, is_recurcive=is_recurcive,
                                       sleep=sleep, silent=silent, verbose=verbose, n_worker=n_worker,
                                       timestamp_reception=timestamp_reception, logfile=logfile)
        import_supervisor.start()
        return True

import typing as t

from tqdm import tqdm


def get_all_profiles(
    client: "Hrflow",  # noqa: F821
    source_key: str,
    show_progress: bool = False,
) -> t.List[t.Dict[str, t.Any]]:
    """
    Retrieve all profiles from a source.

    Args:
        client:                 <hrflow.Client>
                                hrflow client
        source_key:             <string>
                                source_key
        show_progress:          <bool>
                                Show the progress bar

    Returns
        <List[Dict]>:
        List of profiles
    """
    max_page = client.profile.storing.list(source_keys=[source_key])["meta"]["maxPage"]
    profile_list = []
    page_range = range(1, max_page + 1)
    if show_progress:
        page_range = tqdm(page_range, "Retrieving profiles")
    for page in page_range:
        profile_list += client.profile.storing.list(
            source_keys=[source_key], page=page, return_profile=True
        )["data"]

    return profile_list


def get_all_jobs(
    client: "Hrflow",  # noqa: F821
    board_key: str,
    show_progress: bool = False,
) -> t.List[t.Dict[str, t.Any]]:
    """
    Retrieve all jobs from a board.

    Args:
        client:                 <hrflow.Client>
                                hrflow client
        board_key:              <string>
                                board_key
        show_progress:          <bool>
                                Show the progress bar

    Returns
        <List[Dict]>:
        List of jobs
    """
    max_page = client.job.storing.list(board_keys=[board_key])["meta"]["maxPage"]
    job_list = []
    page_range = range(1, max_page + 1)
    if show_progress:
        page_range = tqdm(page_range, "Retrieving jobs")
    for page in page_range:
        job_list += client.job.storing.list(
            board_keys=[board_key], page=page, return_job=True
        )["data"]

    return job_list

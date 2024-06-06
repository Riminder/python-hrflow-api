import os
import typing as t
import urllib
from io import BytesIO

from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook

from ..storing import get_all_jobs, get_all_profiles
from .job import TEMPLATE_URL as JOB_TEMPLATE_URL
from .job import fill_work_sheet as fill_job_work_sheet
from .job import parsing_evaluator as job_parsing_evaluator
from .profile import TEMPLATE_URL as PROFILE_TEMPLATE_URL
from .profile import fill_work_sheet as fill_profile_work_sheet
from .profile import parsing_evaluator as profile_parsing_evaluator

STATISTICS_SHEET_NAME = "1. Statistics"


def load_workbook_from_url(url: str) -> Workbook:
    """
    Load an excel file from a url

    Args:
        url:                         <str>
                                     The url of the excel file

    Returns:
        <Workbook>
        The loaded workbook
    """
    file = urllib.request.urlopen(url).read()
    return load_workbook(filename=BytesIO(file))


def prepare_report_path(path: str) -> str:
    """
    Prepare the report path

    Args:
        path:                        <str>
                                     The path of the report
    """
    if os.path.isdir(path):
        return os.path.join(path, "parsing_evaluation.xlsx")
    if not path.endswith(".xlsx"):
        return f"{path}.xlsx"
    return path


def generate_parsing_evaluation_report(
    client: "Hrflow",  # noqa: F821
    report_path: str,
    source_key: t.Optional[str] = None,
    board_key: t.Optional[str] = None,
    show_progress: bool = False,
):
    """
    Generate a parsing evaluation report

    If you want to generate a parsing evaluation report for jobs, you must
    provide the board_key.
    If you want to generate a parsing evaluation report for profiles, you must
    provide the source_key.

    board_key and source_key are optional string, you must provide only one of them.

    Args:
        client:                      <Hrflow>
                                     The client to use
        source_key:                  <Optional[str]>
                                     The source key where the profiles are
        board_key:                   <Optional[str]>
                                     The board key where the jobs are
        report_path:                 <str>
                                     The path of the report
                                     This can be a already existing directory where
                                     the report will be saved as parsing_evaluation.xlsx
                                     This can be directly the path of the report.
                                     If the path is not an excel file (xlsx),
                                     the report will be saved as {path}.xlsx
        show_progress:               <bool>
                                     Show the progress bar
    """

    if not source_key and not board_key:
        raise ValueError("You must provide either source_key or board_key")
    if source_key and board_key:
        raise ValueError("You must provide only one of source_key or board_key")

    if source_key:
        profile_list = get_all_profiles(client, source_key, show_progress)
        evaluation_list = profile_parsing_evaluator(profile_list, show_progress)

        work_book = load_workbook_from_url(PROFILE_TEMPLATE_URL)
        work_sheet = work_book[STATISTICS_SHEET_NAME]
        fill_profile_work_sheet(work_sheet, evaluation_list, show_progress)
    else:
        assert board_key is not None
        job_list = get_all_jobs(client, board_key, show_progress)
        evaluation_list = job_parsing_evaluator(job_list, show_progress)

        work_book = load_workbook_from_url(JOB_TEMPLATE_URL)
        work_sheet = work_book[STATISTICS_SHEET_NAME]
        fill_job_work_sheet(work_sheet, evaluation_list, show_progress)

    report_path = prepare_report_path(report_path)
    work_book.save(report_path)
    work_book.close()

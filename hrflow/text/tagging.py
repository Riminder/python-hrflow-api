import typing as t

from ..core.rate_limit import rate_limiter
from ..core.validation import validate_response


class TextTagging:
    """Manage tagging related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    @rate_limiter
    def post(
        self,
        algorithm_key: str,
        text: t.Optional[str] = None,
        texts: t.Optional[t.List[str]] = None,
        context: t.Optional[str] = None,
        labels: t.Optional[t.List[str]] = None,
        top_n: t.Optional[int] = 1,
        output_lang: t.Optional[str] = "en",
    ) -> t.Dict[str, t.Any]:
        """
                Tag a Text. Predict most likely tags for a text with our library of AI
                algorithms.

                Args:
                    algorithm_key:      <str>
                                        AI tagging algorithm you want to apply to
                                        the input text. Six taggers have been released
                                        through the Tagging API. We are actively working
                                        on bringing out more taggers.
                                        Here is a list of all the currently available
                                        taggers (beaware that the list is subject to
                                        change refer to developers.hrflow.ai for the
                                        latest list):
        - tagger-rome-family: Grand domaines of job the French ROME
        - tagger-rome-subfamily: Domaines of job the French ROME
        - tagger-rome-category: Metiers of job the French ROME
        - tagger-rome-jobtitle: Appellations of job the French ROME
        - tagger-hrflow-skills: Skills referential defined by HrFlow.ai
        - tagger-hrflow-labels: User defined labels, if any

                    texts:              <list[str]>
                                        Tag a list of texts. Each text can be: the
                                        full text of a Job, a Resume, a Profile, an
                                        experience, a Job and more.

                    context:            <optional[str]>
                                        A context for given labels if
                                        algorithm_key="tagger-hrflow-labels".

                    labels:             <optional[list[str]]>
                                        List of output tags if
                                        algorithm_key="tagger-hrflow-labels".

                    top_n:              <optional[int]>
                                        Number of predicted tags that will be returned.

                    output_lang:        <optional[str]>
                                        Language of the returned tags.

                Returns:
                    `/text/tagging` response
        """
        payload = dict(
            algorithm_key=algorithm_key,
            context=context,
            labels=labels,
            output_lang=output_lang,
            top_n=top_n,
        )

        if texts is None and text is not None:
            payload["text"] = text
        elif text is None and texts is not None:
            payload["texts"] = texts
        elif text is None and texts is None:
            raise ValueError("Either text or texts must be provided.")
        else:
            raise ValueError("Only one of text or texts must be provided.")

        response = self.client.post("text/tagging", json=payload)
        return validate_response(response)

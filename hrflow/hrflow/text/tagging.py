from ..utils import validate_response


class TextTagging:
    """Manage tagging related calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def post(self, text, algorithm_key, top_n=1, output_lang="en"):
        """
        Predict most likely tags for a text with our library of AI algorithms.

        Args:
            text:                   <string>
                                    Target text input. Example: the full text of a Job, a Resume , a Profile, an experience, a Job and more
            algorithm_key:          <string>
                                    AI tagging algorithm you want to apply to the input text.
                                    Five taggers have been released through the Tagging API. We are actively working on bringing out more taggers.
                                    Here is a list of all the currently available taggers: (beaware that the list is subject to change refer to developers.hrflow.ai for the latest list)
                                        - tagger-rome-family : Grand domaines of job the French ROME
                                        - tagger-rome-subfamily : Domaines of job the French ROME
                                        - tagger-rome-category	: Metiers of job the French ROME
                                        - tagger-rome-jobtitle : Appellations of job the French ROME
                                        - revealing : Skills referential defined by HrFlow.ai

            top_n:                  <int>
                                    Number of predicted tags that will be returned. Default is 1.
            output_lang:            <string>
                                    Language of the predicted tags. Default is "en" English.
        Returns
            Predictions tags with probabilities

        """
        payload = {
            "text": text,
            "algorithm_key": algorithm_key,
            "top_n": top_n,
            "output_lang": output_lang,
        }

        response = self.client.post("text/tagging", json=payload)
        return validate_response(response)

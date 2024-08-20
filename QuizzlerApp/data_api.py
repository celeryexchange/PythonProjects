import requests

url = "https://opentdb.com/api.php"


def get_quiz_questions(size: int, category: int = None) -> list:
    """
    Fetch quiz questions from an external API.

    This function retrieves a specified number of quiz questions from an API.
    The questions are True/False. An optional category can be
    provided to filter the questions.

    Parameters:
    -----------
    size : int
        The number of quiz questions to retrieve. This is a mandatory parameter.

    category : int, optional
        The ID of the category to filter the questions by. If not provided, the API
        will return questions from any categories.

        - `9` General Knowledge
        - `18` Science - Computers
        - `22` Geography

    Returns:
    --------
    list
        A list of dictionaries containing the quiz questions and related information.
        Each dictionary typically includes fields like 'question', 'correct_answer',
        and 'incorrect_answers'.

    Raises:
    -------
    HTTPError
        If the API request fails (e.g., returns a non-200 status code), an HTTPError
        is raised with details of the failure.

    Example:
    --------
    >>> get_quiz_questions(10)
    [{'question': 'Is the sky blue?', 'correct_answer': 'True', ...}, ...]

    >>> get_quiz_questions(10, category=9)
    [{'question': 'Is Python a programming language?', 'correct_answer': 'True', ...}, ...]
    """
    # mandatory parameters
    payload = {
        "amount": size,
        "type": "boolean"
    }

    # add optional parameter if it's provided
    if category:
        payload["category"] = category

    # Make the API request
    r = requests.get(url, params=payload)

    # Handle the response (for example, returning the JSON data)
    if r.status_code == 200:
        content = r.json()
        return content["results"]
    else:
        r.raise_for_status()

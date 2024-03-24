import typing


def extract_keywords(input: str) -> typing.List[str]:
    different_keywords = input.split(";")

    return [
        # *different_keywords,  # отдельные кейворды
        " ".join(different_keywords),  # общий запрос, вдруг что-нибудь найдём
    ]

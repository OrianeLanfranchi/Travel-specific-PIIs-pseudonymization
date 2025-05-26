import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath("src"))
from tspii.reversible_anonymizers.reversible_anonymizer import ReversibleAnonymizer
from tspii.recognizers.recognizers import create_travel_specific_recognizers
from tspii.operators.faker_operators import create_fake_data_operators
import os


def create_text_en():
    return """
        Subject: Meeting Details and Updates

        Dear Team,

        I hope this message finds you well today. I wanted to share a few updates regarding the upcoming project kickoff meeting, which is scheduled for April 12, 2025, at 3:00 PM EST. Below, you’ll find the key details for the meeting.

        The attendees will include a Senior Software Engineer from Tech Innovations Inc. (John S.) and a Marketing Manager from Creative Designs Ltd. (Maria G.).

        The agenda for the meeting will cover an introduction to the new project, a review of deliverables and the timeline, and a Q&A session. Additionally, one of the attendees will be traveling from New York to London on April 15, 2025, for a client presentation.

        For those involved with the project budget approval, the financial details include the SWIFT Code ABCDUS33, GB29NWBK60161331926819, and 021000021.

        Please confirm your attendance by March 30, 2025, and feel free to reach out if you have any concerns.

        Best regards,
        Anna P.
        Project Manager, Tech Innovations Inc.
    """


def main():
    load_dotenv(".env", override=True)

    reversible_anonymizer = ReversibleAnonymizer()

    # Add recognizers
    for recognizer in create_travel_specific_recognizers():
        reversible_anonymizer.add_recognizer(recognizer)

    reversible_anonymizer.add_azure_ai_language_recognizer(
        azure_ai_language_key=os.getenv("AZURE_AI_LANGUAGE_KEY"),
        azure_ai_language_endpoint=os.getenv("AZURE_AI_LANGUAGE_ENDPOINT"),
    )

    # Add operators
    reversible_anonymizer.add_operators(create_fake_data_operators())

    # Analyze the text
    reversible_anonymizer.analyze(create_text_en())

    # Anonymize the text
    res1 = reversible_anonymizer.anonymize()
    print(res1.text)

    # Test save mapping and load mapping
    reversible_anonymizer.save_mapping("mapping.json")

    reversible_anonymizer2 = ReversibleAnonymizer()
    reversible_anonymizer2.load_mapping("mapping.json")
    res3 = reversible_anonymizer2.deanonymize(res1.text)
    print(res3)


main()

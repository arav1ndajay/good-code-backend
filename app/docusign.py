import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients
import sys

sys.path.insert(
    1, '/home/vaishakh/Desktop/Projects/good-code-backend/jwt_helpers')
from jwt_helper import create_api_client

sys.path.insert(1, '/home/vaishakh/Desktop/Projects/good-code-backend/app')

demo_docs_path = "/home/vaishakh/Desktop/Projects/good-code-backend/static"


class Eg002SigningViaEmailController:

    @classmethod
    def worker(cls, args, doc_pdf_path):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args, doc_pdf_path)

        api_client = create_api_client(base_path=args["base_path"],
                                       access_token=args["access_token"])
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=args["account_id"],
            envelope_definition=envelope_definition)

        # print(f"RESULTS: {results}")
        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args, doc_pdf_path):
        """
        Creates envelope
        Document 1: An HTML document.
        Document 2: A Word .docx document.
        Document 3: A PDF document.
        DocuSign will convert all of the documents to the PDF format.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        # document 1 (html) has sign here anchor tag **signature_1**
        # document 2 (docx) has sign here anchor tag /sn1/
        # document 3 (pdf)  has sign here anchor tag /sn1/
        #
        # The envelope has two recipients.
        # recipient 1 - signer
        # recipient 2 - cc
        # The envelope will be sent first to the signer.
        # After it is signed, a copy is sent to the cc person.

        # create the envelope definition
        env = EnvelopeDefinition(email_subject="Please sign this document set")

        with open(path.join(demo_docs_path, doc_pdf_path), "rb") as file:
            doc3_pdf_bytes = file.read()
        doc3_b64 = base64.b64encode(doc3_pdf_bytes).decode("ascii")

        document3 = Document(  # create the DocuSign document object
            document_base64=doc3_b64,
            name="Lorem Ipsum",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )
        # The order in the docs array determines the order in the envelope
        env.documents = [document3]

        # Create the signer recipient model
        signer1 = Signer(email=args["signer_email"],
                         name=args["signer_name"],
                         recipient_id="1",
                         routing_order="1")
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # create a cc recipient to receive a copy of the documents
        cc1 = CarbonCopy(email=args["cc_email"],
                         name=args["cc_name"],
                         recipient_id="2",
                         routing_order="2")

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        sign_here1 = SignHere(anchor_string="**signature_1**",
                              anchor_units="pixels",
                              anchor_y_offset="10",
                              anchor_x_offset="20")

        sign_here2 = SignHere(anchor_string="/sn1/",
                              anchor_units="pixels",
                              anchor_y_offset="10",
                              anchor_x_offset="20")

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1, sign_here2])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1], carbon_copies=[cc1])
        env.recipients = recipients

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env


trial_args = {
    'envelope_args': {
        'signer_name': 'Vaishakh',
        'signer_email': 'vaishakhsm@gmail.com',
        'cc_email': 'aravindajay11@gmail.com',
        'cc_name': 'Aravind',
        'status': 'create',
    },
    'account_id':
    'e9cd3611-83ec-4bd7-b8d2-d058f1cb31e4',
    'base_path':
    'https://demo.docusign.net/restapi',
    'access_token':
    'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQsAAAABAAUABwAASa_wJXzaSAgAAInS_mh82kgCAKFmpqoRQWJAgHpy19xltb0VAAEAAAAYAAIAAAAKAAAABQAAAA0AJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhOCIAJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhOBIAAQAAAAsAAABpbnRlcmFjdGl2ZTAAAO9M7iV82kg3APrqzpm3WUhFva-Ck_FByNw.HL1BE3O7VkgrXBsE9QsFkLN7fn9Lv3KXiGoGWq3VafMC7Ff4sSyqPBuvLlrLeEVkMlYNSJusbp9g0BIjSP1IxEWoNl0fmcc4HfjXQXAAiD7wQaqqcgqiOFqBDJDaI3RlYVnT8pwjIJc0Q1GDxLT0saj0mj41KX1yc4T283oKfnwjve_fz5JIQT3qL-008fxehsRxhq3flbvvuraegcIRQ_dV4d6k9RZi-TK5V986khm_utpDyKaWZY72smyMlkYBcwU5l3AnwzJbgTWKi5rTJwRbOCb5Bb0-PMny1ID6OfeUcyZS5w8oPVSpry7TXDpQJwyfDnHBK6JgTZ3UaUMM3Q'
}

Eg002SigningViaEmailController.worker(trial_args,
                                      doc_pdf_path='Random pdf.pdf')

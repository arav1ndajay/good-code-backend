import base64
from os import path
from fpdf import FPDF
import urllib.request
import os
from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients, ApiClient, Checkbox, ConnectApi, ConnectCustomConfiguration, ConnectEventData, EventNotification, EnvelopeEvent


def create_api_client(base_path, access_token):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization",
                                  header_value=f"Bearer {access_token}")

    return api_client


class EnvelopeEmailSignature:

    @classmethod
    def worker(cls, args, assets):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        envelope_args = args["envelope_args"]
        envelope_definition = cls.make_envelope(envelope_args, assets)
        api_client = create_api_client(base_path=args["base_path"],
                                       access_token=args["access_token"])

        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=args["account_id"],
            envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args, assets):
        """
        Creates envelope
        Document 1: An HTML document.
        Document 2: A Word .docx document.
        Document 3: A PDF document.
        DocuSign will convert all of the documents to the PDF format.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        connect_event_data = ConnectEventData(include_data=["tabs"],
                                              format='json',
                                              version='restv2.1')

        envelope_event = EnvelopeEvent()
        envelope_event.envelope_event_status_code = 'completed'

        event_notification = EventNotification(
            envelope_events=[envelope_event],
            url="https://api.hackathonjgi.software/updatemetadata",
            require_acknowledgment='true',
            logging_enabled='true',
            event_data=connect_event_data)

        env = EnvelopeDefinition(email_subject="Please sign this document set",
                                 event_notification=event_notification)

        signer1 = Signer(email="", name="", recipient_id="1")
        recipients = Recipients(signers=[signer1])

        document3 = cls.create_document(assets)
        signer1.tabs = cls.get_tabs(assets=assets)

        env.documents = [document3]
        env.recipients = recipients
        env.status = args["status"]

        return env

    @classmethod
    def create_document(cls, assets):
        pdf = FPDF()
        w = 105
        h = 148
        x = 20
        y = 75

        for image in assets:
            urllib.request.urlretrieve(image['link'], f"{image['id']}.jpg")
            pdf.add_page()
            pdf.image(f"{image['id']}.jpg", x, y, w, h)
            os.remove(f"{image['id']}.jpg")

        pdf.output("Verify.pdf", "F")

        with open("Verify.pdf", "rb") as file:
            document_pdf_bytes = file.read()
        document_b64 = base64.b64encode(document_pdf_bytes).decode("ascii")

        return Document(  # create the DocuSign document object
            document_base64=document_b64,
            name=
            "Verification and Approval",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id="1")

    def get_tabs(assets):
        checkbox_tabs = []

        for cnt, image in enumerate(assets):
            checkbox_tabs.append(
                Checkbox(document_id="1",
                         y_position="450",
                         x_position="475",
                         page_number=cnt + 1,
                         shared=True,
                         name=f"Approve {image['id']}",
                         tab_label=image['id']))

        return Tabs(checkbox_tabs=checkbox_tabs)

from docusign_esign import EnvelopesApi, ReturnUrlRequest, ApiClient

# from flask import url_for, session, request

from eg2 import Eg002SigningViaEmailController


def create_api_client(base_path, access_token):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization",
                                  header_value=f"Bearer {access_token}")

    return api_client


class Eg011EmbeddedSendingController:

    # @staticmethod
    # def get_args():
    #     """Get required session and request arguments"""
    #     # More data validation would be a good idea here
    #     # Strip anything other than characters listed
    #     signer_email = pattern.sub("", request.form.get("signer_email"))
    #     signer_name = pattern.sub("", request.form.get("signer_name"))
    #     cc_email = pattern.sub("", request.form.get("cc_email"))
    #     cc_name = pattern.sub("", request.form.get("cc_name"))
    #     starting_view = pattern.sub("", request.form.get("starting_view"))

    #     envelope_args = {
    #         "signer_email": signer_email,
    #         "signer_name": signer_name,
    #         "cc_email": cc_email,
    #         "cc_name": cc_name,
    #         "status": "sent",
    #     }
    #     args = {
    #         "starting_view": starting_view,
    #         "account_id": session["ds_account_id"],
    #         "base_path": session["ds_base_path"],
    #         "access_token": session["ds_access_token"],
    #         "envelope_args": envelope_args,
    #         "ds_return_url": url_for("ds.ds_return", _external=True),
    #     }

    #     print(f"Args are: {args}")
    #     print(f"Env args are: {envelope_args}")
    #     return args

    @staticmethod
    def worker(args, doc_pdf_path):
        """
        This function does the work of creating the envelope in
        draft mode and returning a URL for the sender"s view
        """

        # Step 1. Create the envelope with "created" (draft) status
        args["envelope_args"]["status"] = "created"
        # Using worker from example 002
        results = Eg002SigningViaEmailController.worker(args, doc_pdf_path)
        envelope_id = results["envelope_id"]

        # Step 2. Create the sender view
        view_request = ReturnUrlRequest(return_url=args["ds_return_url"])
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"],
                                       access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_sender_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            return_url_request=view_request)

        # Switch to Recipient and Documents view if requested by the user
        url = results.url
        if args["starting_view"] == "recipient":
            url = url.replace("send=1", "send=0")
        print({"envelope_id": envelope_id, "redirect_url": url})
        return {"envelope_id": envelope_id, "redirect_url": url}


trial_args = {
    'envelope_args': {
        'signer_name': 'Vaishakh',
        'signer_email': 'vaishakhsm@gmail.com',
        'cc_email': 'aravindajay11@gmail.com',
        'cc_name': 'Aravind',
        'status': 'create'
    },
    'account_id': 'e9cd3611-83ec-4bd7-b8d2-d058f1cb31e4',
    'base_path': 'https://demo.docusign.net/restapi',
    'access_token':
    'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAUNBYY3zaSAgAAJDzZqZ82kgCAKFmpqoRQWJAgHpy19xltb0VAAEAAAAYAAIAAAAKAAAABQAAAA0AJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhOCIAJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhODAAAKVFjzp82kg3APrqzpm3WUhFva-Ck_FByNw.eZPXK49J1lhl3d3nYY5NvWgTv9cxCQ1goHUmR5gSq23ttprSlRXiNGgznsx-hJHMkDYWmAlzqScHqqmGod1DAV2qIG_a-Jm6qy_aMZMKjpm6W90Kg8XJOMZFlb9K2fNr7dL8E4TdgXjlhAqmPrPlMvghI5Rd98BtQzdQoTixR9-C9Cp6qX8mAfko_hq-wL19V3Ptla8xV1wSSlaoXGy8Df8B8BjQlQLS9UlZ2MZ7oT2FZh6rgPje6Mcvh_xnDVrucrQd6YPAOYsyNyyvg-S7J456MZOoCpBOKgHcGup7ESTkeU7IP1VsCYTH9hdN6IyPfhvDs174fBK2PqmFCU2HJQ',
    'ds_return_url': 'http://localhost:3001',
    'starting_view': 'recipient'
}

Eg011EmbeddedSendingController.worker(trial_args, doc_pdf_path="yourfile.pdf")

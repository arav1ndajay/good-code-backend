from docusign_esign import EnvelopesApi, ReturnUrlRequest, ApiClient

# from flask import url_for, session, request

from app.docusign.email_envelope import EnvelopeEmailSignature


def create_api_client(base_path, access_token):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization",
                                  header_value=f"Bearer {access_token}")

    return api_client


class EmbeddedSender:

    @staticmethod
    def worker(args, assets):
        """
        This function does the work of creating the envelope in
        draft mode and returning a URL for the sender"s view
        """

        args["envelope_args"]["status"] = "created"

        results = EnvelopeEmailSignature.worker(args, assets)
        envelope_id = results["envelope_id"]

        view_request = ReturnUrlRequest(return_url=args["ds_return_url"])

        api_client = create_api_client(base_path=args["base_path"],
                                       access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_sender_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            return_url_request=view_request)

        url = results.url
        if args["starting_view"] == "recipient":
            url = url.replace("send=1", "send=0")
        print({"envelope_id": envelope_id, "redirect_url": url})
        return {"envelope_id": envelope_id, "redirect_url": url}


# trial_args = {
#     'envelope_args': {
#         'status': 'create'
#     },
#     'starting_view':
#     'recipient',
#     'base_path':
#     'https://demo.docusign.net/restapi',
#     'account_id':
#     'e9cd3611-83ec-4bd7-b8d2-d058f1cb31e4',
#     'ds_return_url':
#     'http://localhost:3001',
#     'access_token':
#     'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAUNBYY3zaSAgAAJDzZqZ82kgCAKFmpqoRQWJAgHpy19xltb0VAAEAAAAYAAIAAAAKAAAABQAAAA0AJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhOCIAJAAAADhjMmRkYmIxLTAyMGUtNGY4OC04MzFkLWUzOWJhOWUzNjRhODAAAKVFjzp82kg3APrqzpm3WUhFva-Ck_FByNw.eZPXK49J1lhl3d3nYY5NvWgTv9cxCQ1goHUmR5gSq23ttprSlRXiNGgznsx-hJHMkDYWmAlzqScHqqmGod1DAV2qIG_a-Jm6qy_aMZMKjpm6W90Kg8XJOMZFlb9K2fNr7dL8E4TdgXjlhAqmPrPlMvghI5Rd98BtQzdQoTixR9-C9Cp6qX8mAfko_hq-wL19V3Ptla8xV1wSSlaoXGy8Df8B8BjQlQLS9UlZ2MZ7oT2FZh6rgPje6Mcvh_xnDVrucrQd6YPAOYsyNyyvg-S7J456MZOoCpBOKgHcGup7ESTkeU7IP1VsCYTH9hdN6IyPfhvDs174fBK2PqmFCU2HJQ'
# }

# EmbeddedSender.worker(trial_args, assets=assets[0:4])
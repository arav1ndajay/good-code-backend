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

assets = [{
    'id':
    '2df9ffb3-9a33-42bf-9108-a34ae3208320',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/2df9ffb39a3342bf9108a34ae3208320/2df9ffb39a3342bf9108a34ae3208320/Medium/IMG_0211.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=YmSV348FJfX4%2FtPSMrQMeBMvVQ8oqaqo%2FLpD6SN3i30%3D&st=1969-02-25T21%3A36%3A15Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '869ba5fa-95e0-4634-87bf-6acce233c174',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/869ba5fa95e0463487bf6acce233c174/869ba5fa95e0463487bf6acce233c174/Medium/IMG_0224.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=7AwOMVMDRZHoa5dIeF7DNm51rnq2tdvC1k74%2FrAzVYs%3D&st=1393-12-01T18%3A44%3A26Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '750061aa-acee-4c50-ae92-e142ebaf304f',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/750061aaacee4c50ae92e142ebaf304f/750061aaacee4c50ae92e142ebaf304f/Medium/IMG_0235.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=xYROWDPXa8Kxjpw67MQKKD%2FF89ChMfA3dv66QGSM%2FT0%3D&st=0985-07-29T07%3A36%3A48Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '94dc61df-debd-4149-bf29-5503cf2a9146',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/94dc61dfdebd4149bf295503cf2a9146/94dc61dfdebd4149bf295503cf2a9146/Medium/IMG_0238.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=IHsH76Y9F3FSEebVU4hlRE8xfUAiauvKS8YK09FqAfg%3D&st=0206-07-08T21%3A14%3A47Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '70934999-ee15-4211-bbd7-85be38480556',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/70934999ee154211bbd785be38480556/70934999ee154211bbd785be38480556/Medium/IMG_0295.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=Ym4qYe2SZLkz2INSiqOIJESMjQ9iE%2FhVrSWDKpSeVZY%3D&st=0866-12-11T14%3A27%3A53Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '227853da-a844-4b06-a282-b8e3702b8430',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/227853daa8444b06a282b8e3702b8430/227853daa8444b06a282b8e3702b8430/Medium/IMG_0350.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=4srHuhKC%2BMx7hWqKMC73V2pUE0yQz6UfcBYBVF1vUGQ%3D&st=0569-06-12T21%3A08%3A33Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '30ae3d8e-843f-40e6-8446-3f37ce8adb75',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/30ae3d8e843f40e684463f37ce8adb75/30ae3d8e843f40e684463f37ce8adb75/Medium/IMG_0371.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=WbCa7WGLSH2s%2F7p4UINCl%2BLkK%2FZD%2B%2FlMD%2FBMFGbcIao%3D&st=0862-02-17T22%3A55%3A28Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '562aaba2-33a0-4ae7-bfe6-f2820081878e',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/562aaba233a04ae7bfe6f2820081878e/562aaba233a04ae7bfe6f2820081878e/Medium/IMG_0379.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=r%2B2BdcHHNrLg15JJrH7ag304FumX53sIxDPrLkcu9hs%3D&st=0453-05-27T09%3A56%3A23Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '35c81da5-a17d-498c-bc99-bdf12de3adf4',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/35c81da5a17d498cbc99bdf12de3adf4/35c81da5a17d498cbc99bdf12de3adf4/Medium/IMG_0437.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=VYdg4Qmj9VQkJFOHCaY%2FuvH2HZ3X3ECpvarCo6oSOS0%3D&st=0673-10-30T12%3A23%3A04Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '9ec906a7-96a9-4cec-848a-a6b4da9bb277',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/9ec906a796a94cec848aa6b4da9bb277/9ec906a796a94cec848aa6b4da9bb277/Medium/IMG_0485.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=IcVe6P1O0koYDYA2H3OdZEjDWirB6Rd9KHIO80tYH7I%3D&st=0911-09-27T17%3A08%3A31Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '9c49cd49-ae61-4785-bd08-90b1ef6a94f3',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/9c49cd49ae614785bd0890b1ef6a94f3/9c49cd49ae614785bd0890b1ef6a94f3/Medium/IMG_0516.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=40FL0Jkc7vOYRyArOoaDYsazaG9phgV%2FEF31ILIxUek%3D&st=1279-08-03T09%3A02%3A47Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    'eb909531-69eb-4631-ab65-90a20b7b1063',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/eb90953169eb4631ab6590a20b7b1063/eb90953169eb4631ab6590a20b7b1063/Medium/IMG_0554.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=0nKoxcdmyBIN82c%2BfrAmfXqnfugUhGzlLob9hUxDLRA%3D&st=0244-06-02T06%3A52%3A36Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '5a588e71-df93-411c-b433-709e96bc4d7e',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/5a588e71df93411cb433709e96bc4d7e/5a588e71df93411cb433709e96bc4d7e/Medium/IMG_0572.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=KO9X3jH%2BkUBarKNrLBJn%2Fi5m0yFw9jVmwZIKXTxRuDY%3D&st=0060-06-03T05%3A43%3A44Z&se=2032-08-11T22%3A36%3A26Z'
}, {
    'id':
    '55bacae0-d924-48a3-8ec4-838e9ee14786',
    'link':
    'https://mvsfservicefabricusva.blob.core.windows.net/medialibrary-03cba27e25e74bc6bb54bc2691d52d1b-r/55bacae0d92448a38ec4838e9ee14786/55bacae0d92448a38ec4838e9ee14786/Medium/IMG_0575.jpg?sv=2017-04-17&sr=b&si=202207201809&sig=XiYvJmj3XtKJfZE%2FjsAU%2FB0xObueX9q5irq%2BHV6cLWg%3D&st=1511-10-16T18%3A01%3A14Z&se=2032-08-11T22%3A36%3A26Z'
}]

EmbeddedSender.worker(trial_args, assets=assets[0:4])

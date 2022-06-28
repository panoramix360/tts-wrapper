from typing import Tuple

from ...exceptions import ModuleNotInstalled

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore
    from ibm_watson import TextToSpeechV1  # type: ignore
except ImportError:
    IAMAuthenticator = None
    TextToSpeechV1 = None

Credentials = Tuple[str, str]


class WatsonClient:
    def __init__(self, credentials: Credentials) -> None:
        if IAMAuthenticator is None or TextToSpeechV1 is None:
            raise ModuleNotInstalled("ibm-watson")

        api_key, api_url = credentials
        client = TextToSpeechV1(authenticator=IAMAuthenticator(api_key))
        client.set_service_url(api_url)
        self.client = client

    def synth(self, ssml: str, voice: str) -> bytes:
        return (
            self.client.synthesize(text=str(ssml), voice=voice, accept="audio/wav")
            .get_result()
            .content
        )

from typing import Optional

from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

from ...tts import SSML, AbstractTTS
from . import WatsonClient


class WatsonTTS(AbstractTTS):
    def __init__(
        self,
        client: WatsonClient,
        voice: Optional[str] = None,
    ) -> None:
        self.client = client
        self.voice = voice or "en-US_LisaV3Voice"

    def synth_to_bytes(self, ssml: SSML) -> bytes:
        return self.client.synth(str(ssml), voice=self.voice)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)

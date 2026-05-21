
from deep_translator import GoogleTranslator


class Traductor:

    @staticmethod
    def traducir(
        texto,
        destino="en"
    ):

        traduccion = GoogleTranslator(
            source='auto',
            target=destino
        ).translate(texto)

        return traduccion
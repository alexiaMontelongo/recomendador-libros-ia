from deep_translator import GoogleTranslator


class Traductor:

    @staticmethod
    def traducir(texto):

        traduccion = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(texto)

        return traduccion
    




    
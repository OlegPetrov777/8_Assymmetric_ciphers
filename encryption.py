class Encryption:

    def __init__(self):
        pass

    def Msg_Bytes(self, text, K):
        """ Метод, кодирующий каждый байт текста """
        result = ''
        b_text = bytes(text, encoding='utf-8')
        for byte in b_text:
            byte *= K
            result += str(byte) + ','
        return result

    def Bytes_Msg(self, text, K):
        """ Метод переводит закодированный байт в текст """
        result = ''

        for i in text.split(',')[:-1]:
            result += chr(int(i) // K)
        return result

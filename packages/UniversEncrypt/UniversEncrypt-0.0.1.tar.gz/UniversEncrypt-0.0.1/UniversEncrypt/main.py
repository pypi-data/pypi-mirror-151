class UniversEncrypt:

    Words = "abcdeifghklmnopqrstuvwxyz"
    Key =   "87563#@&4!^\9)(12{}[]-_=+"

    @classmethod
    def Encrypt(cls, text: str) -> str:
        '''Шифрует введенную строку'''
        Keys = ""
        for i in range(len(text)):
            k = cls.Words.find(text[i].lower())
            if k >= 0:
                Keys += cls.Key[k]
            else:
                Keys += text[i]
        return Keys
        
    @classmethod
    def Decrypt(cls, code: str) -> str:
        '''Расшифровывает введеную код'''
        text = ""
        for i in range(len(code)):
            k = cls.Key.find(code[i].lower())
            if k >= 0:
                text += cls.Words[k]
            else:
                text += code[i]
        return text


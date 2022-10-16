import base64
import traceback


def getLetterFromAlphaberForLetter(letter, letterToChange):
    abc = "abcdefghijklmnopqrstuvwxyz0123456789=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
 
    posLetter = abc.find(letter)
 
    if posLetter == -1:
        return
 
    posLetterToChange = abc.find(letterToChange)
    if posLetterToChange == -1:
        return
 
    part1 = abc[posLetter:len(abc)]
    part2 = abc[0:posLetter]
    newABC = "" + part1 + "" + part2
 
    letterAccordingToAbc = list(newABC)[posLetterToChange]
 
    return letterAccordingToAbc
 
def encrypt(type, text):
    try:
        if type == "deezer":
            text = "1___" + text
        else:
            text = "2___" + text
 
        password = "mp3juicefm"
        base64_str = base64.b64encode(text.encode("ascii")).decode('utf-8')
 
        list1 = list(base64_str)
 
        arrPass = list(password)
        lastPassLetter = 0
 
        encrypted = ""
 
        for i in range(0, len(list1)):
            letter = list1[i]
            passwordLetter = arrPass[lastPassLetter]
 
            temp = getLetterFromAlphaberForLetter(passwordLetter, letter)
 
            if temp:
                encrypted += temp
            else:
                return
 
            if lastPassLetter == len(arrPass) - 1:
                lastPassLetter = 0
            else:
                lastPassLetter += 1
 
        return encrypted
 
    except Exception as ex:
        print(traceback.format_exc())
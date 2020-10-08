from bs4 import BeautifulSoup


class testUtil:

    @staticmethod
    def getValue(text,pattern):
        for item in pattern:
            soup = BeautifulSoup(text,"html.parser")
            value =  soup.find(item)
            print(value)



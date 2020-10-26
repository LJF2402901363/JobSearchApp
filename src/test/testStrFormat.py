if __name__ == '__main__':
    str1 = "https://liepin.com/zhaopin/?key={}&dqs={}"
    str1 = str1.format("java","010",1,40)
    print(str1)
    str2 = "https://www.kanzhun.com/search/?city={}&pageCurrent={}&q={}&type={}"
    str2 = str2.format("101280100",1,"java","recruit")
    print(str2)

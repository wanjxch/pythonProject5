
# 定义字母表与数字表
lower_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
upper_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
number_list = ["0","1","2","3","4","5","6","7","8","9"]

def jiami(m):
    new_a = []
    a = list(input("请输入要加密的内容："))
    for i in a:
        if i in lower_list:
            m_index = lower_list.index(i)+m
            if m_index > 25:
                m_index = m_index - 26
            new_a.append(lower_list[m_index])
        elif i in upper_list:
            m_index = upper_list.index(i)+m
            if m_index > 25:
                m_index = m_index - 26
            new_a.append(upper_list[m_index])
        elif i in number_list:
            m_index = number_list.index(i)+m
            if m_index > 9:
                m_index = m_index - 10
                new_a.append(number_list[m_index])
    miwen = ''.join(new_a)
    print('加密后的内容：', miwen)

def jiemi(n):
    new_b = []
    b = list(input("请输入要解密的内容："))
    for j in b:
        if j in lower_list:
            n_index = lower_list.index(j) - n
            if n_index > 25:
                n_index = n_index - 26
            new_b.append(lower_list[n_index])
        elif j in upper_list:
            n_index = upper_list.index(j) - n
            if n_index > 25:
                n_index = n_index - 26
            new_b.append(upper_list[n_index])
        elif j in number_list:
            n_index = number_list.index(j) - n
            if n_index > 9:
                n_index = n_index - 10
                new_b.append(number_list[n_index])
    mingwen = ''.join(new_b)
    print('解密后的内容：', mingwen)

if __name__ == '__main__':
    while True:
        k = input("加密请输入(e),解密请输入(d),否则退出:")
        if k == 'e':
            m = int(input("请输入要偏移的位次:"))
            jiami(m)
        elif k == 'd':
            n = int(input("请输入要偏移的位次:"))
            jiemi(n)
        else:
            break
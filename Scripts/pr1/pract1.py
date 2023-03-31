while True:
    try:
        colvo = input("Введите количество чисел: ")
        oper = input("Введите операцию(+,-,*,/): ")

        for i in range(int(colvo)):
            chislo = int(input("Введите " + str(i+1) + " число: "))
            if i == 0:
                otvet = chislo
                continue
            if oper == "+":
                otvet = otvet + chislo
            elif oper == "-":
                otvet = otvet - chislo
            elif oper == "*":
                otvet = otvet * chislo
            elif oper == "/":
                otvet = otvet / chislo

        print(otvet)

    except ZeroDivisionError:
        print("На ноль делить нельзя!")
        continue

    except:
        print("Вы сделали что то не так, попробуйте еще раз!")
        continue
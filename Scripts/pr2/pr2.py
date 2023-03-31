import calendar

year = int(input("Введите желаемый год: "))
result = 0

for i in range(1, 13):
    dayInMonth = calendar.monthrange(year, i)[1]
    for j in range(1, dayInMonth+1):
        result += int(j/10) + int(j % 10)
print(str(year) + ": " + str(result))
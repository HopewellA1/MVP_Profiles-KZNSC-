# the new code to validate Identity number
#ID format: YYMMDD G SSS C A Z
#YYMMDD : date of birth
#G: Gender 0-4 Femail, 5-9 Male
#SSS: Sequence number for DOB/G combination
#C: Citizenship 0-SA, 1 - foreigner
#A 0-9 was for race, not used anymore
#Z: control/Check digit

#

#note use reversed index on the id
from datetime import date, datetime
def dateTryParse(date):
    result = True
    
    formatStr = '%m/%d/%Y'
    try:
        datetime.strptime(date, formatStr)
    except:
        result = False
        
    return result

def isVAlidNumberWith12Digits(id):
    return len(id) == 13 and id.isdigit()
def hasValidDate(id):
    year = id[0:2]
    month = id[2:4]
    day = id[4:6]
    
    date1 = f'{month}/{day}/19{year}'
    date2 = f'{month}/{day}/20{year}'
    
    return dateTryParse(date1) or dateTryParse(date2)

def isOdd(number):
    return number % 2 !=0

def validateID(id):
    if isVAlidNumberWith12Digits(id) and  hasValidDate(id):
        sum = 0
        
        for idx, char in  enumerate(reversed(id)):
            digit = int(char)
            if isOdd(idx):
                digit = digit * 2
                if digit > 9:
                    subSum = 0
                    
                    while digit >  0:
                        subSum += digit % 10
                        digit = digit // 10 

                    digit = subSum
            
            sum += digit
        result = sum % 10 == 0
        return result
    
    
    pass 


#Calculating the control digit

def calcControlDigit(SAid):
    said= SAid[0:len(SAid) - 1]
    result = ""
    
    sum = 0
        
    for idx, char in  enumerate(reversed(said)):
        digit = int(char)
        if not isOdd(idx):
            digit = digit * 2
            if digit > 9:
                subSum = 0
                    
                while digit >  0:
                    subSum += digit % 10
                    digit = digit // 10 

                digit = subSum
            
        sum += digit
    
    
    result = (10 - sum % 10) % 10
    return result



def getLastDigit(id):
    return int(id[len(id)-1])



# id  ="8608065701080"
# print(f"The Id is :{id} \n\n")

# print(f"Is it a valid ID yini?:{validateID(id)}\n\n")

# said= id[0:len(id) - 1]

# controlDigit = calcControlDigit(said)

# print(f"The control digit of {id} is: {controlDigit} \n\n")
# dig = id[len(id)-1]

# print(f"The last digit is :{dig}")

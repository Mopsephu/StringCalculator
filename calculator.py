import wordsextractor;
from isvalid import is_valid;
import betterrandomizer;
import math;

_OPERATORS_ : tuple = ("+", "-", "*", "/", "|", "%", "^", "(", ")"); # | - is integer division

_tasksToDo_ : dict = {
    'Numbers':[],
    'Operators':[]
}

#Skips the element at the stated index of the list
def __eraseValueAtIndex__(List : list, index : int) -> list:
    if index < 0:
        index += len(List);
    result : list = [];
    for i in range(len(List)):
        if i != index:
            result.append(List[i]);
    return result;

#Returns substring of the text, locating to the right of the stated index
def __getRightSubstr__(text : str, index : int) -> str:
    if index < 0:
        index += len(text);
    result : str = "";
    for i in range(len(text)):
        if i > index:
            result += text[i];
    return result;

#If all numbers in the list are requal, it returns True. Otherwise - False
def __areAllNumbersEqual__(List : list[float | int]) -> bool:
    areEqual : bool = True;
    numbersReserve : list = List;
    for i in List:
        for a in numbersReserve:
            if i != a:
                areEqual = False;
                break;
        if not areEqual:
            break;
    return areEqual;

#Finds stated element in the list. You can also state its starter position to search from it
def __findElement__(List : list[any], Element : any, startFrom : int = 0) -> int:
    elementIndex : int = -1;
    for i in range(startFrom, len(List)):
        if List[i] == Element:
            elementIndex = i;
            break;
    return elementIndex;

#Finds stated element in the list by going from the end of the list to the beginning. You can also state its starter position to search from it
def __rfindElement__(List : list[any], Element : any, startFrom : int = -1) -> int:
    if startFrom < 0:
        startFrom += len(List);
    elementIndex : int = -1;
    for i in range(startFrom, 0, -1):
        if List[i] == Element:
            elementIndex = i;
            break;
    return elementIndex;

#If status is higher than 0, then it states for its priority (the higher number the higher priority);
#If status is equal to 0, it's a valid number;
#Otherwise it returns -1.
def __defineWordStatus__(word : str) -> int: 
    if not type(word) is str:
        word = str(word);
    if word in _OPERATORS_:
        match word:
            case "+" | "-":
                return 1;
            case "*" | "/" | "%" | "|":
                return 2;
            case "(":
                return 3;
            case ")":
                return 4;
            case "^":
                return 5;
    else:
        if is_valid(word, int) or is_valid(word, float):
            return 0;
        else:
            return -1;

#Returns dictionary, containing only numbers and operators from the text
def __leave__(text : str) -> dict:
    result : dict = {};
    #Leave 1 space between each word
    spacelessText : str = "";
    isInWord : bool = False;
    for i in text:
        if i == " ":
            if isInWord:
                isInWord = False;
                spacelessText += i;
        else:
            if not isInWord:
                isInWord = True;
            spacelessText += i;
    operators : list = [];
    numbers : list = [];
    #Erase operators and add them to the dictionary
    operatorslessText : str = "";
    for i in spacelessText:
        if i in _OPERATORS_:
            operators.append(i);
            operatorslessText += " ";
        else:
            operatorslessText += i;
    #Find the numbers and add them to the dictionary
    for i in range(wordsextractor.countAmountOfWordsInText(operatorslessText)):
        currentNumber : float = float(wordsextractor.getWordFromTextAtPosition(operatorslessText, i));
        numbers.append(currentNumber);
    result["Numbers"] = numbers;
    result["Operators"] = operators;
    return result;

#It does arithmetic operations with two given numbers
def __count__(operator : str, firstNumber : float, secondNumber : float) -> float:
    result : float = 0;
    try:
        match operator:
            case "+":
                result = firstNumber + secondNumber;
            case "-":
                result = firstNumber - secondNumber;
            case "*":
                result = firstNumber * secondNumber;
            case "/":
                try:
                    result = firstNumber / secondNumber;
                except ZeroDivisionError:
                    if firstNumber != 0:
                        print("Division by zero!");
                        result = 0;
                    else:
                        result = betterrandomizer.generateRandomNumber(-9, 9);
            case "|":
                try:
                    result = firstNumber // secondNumber;
                except ZeroDivisionError:
                    if firstNumber != 0:
                        print("Division by zero!");
                        result = 0;
                    else:
                        result = betterrandomizer.generateRandomNumber(-9, 9);
            case "%":
                try:
                    result = firstNumber % secondNumber;
                except ZeroDivisionError:
                    if firstNumber != 0:
                        print("Division by zero!");
                        result = 0;
                    else:
                        result = betterrandomizer.generateRandomNumber(-9, 9);
            case "^":
                result = math.pow(firstNumber, secondNumber);
    except OverflowError:
        print(f"The result is too big to be interpreted!\nCheck expression again:'{firstNumber} {operator} {secondNumber}'");
        result = 0;
    return result;

#The main function
def calculate(expression : str) -> float | int:
    #Fill expression, taking only numbers and operators
    _tasksToDo_ = __leave__(expression);
    #Doing presets
    result : float = 0;
    copyTasks : list = list(_tasksToDo_.values());
    numbersLeft : list = copyTasks[0];
    operatorsLeft : list = copyTasks[1];
    #Get priorities of the operators
    operatorsPriority : list = [];
    for i in operatorsLeft:
        operatorsPriority.append(__defineWordStatus__(i));
    #Enlarge priorities which are being located within brackets
    lastClosingBracket : int = 0;
    for i in range(len(operatorsLeft)):
        if operatorsLeft[i] == "(":
            lastClosingBracket = __rfindElement__(operatorsLeft, ")", lastClosingBracket-1);
            for ia in range(i+1, lastClosingBracket):
                if ia != 3 and ia != 4:
                    operatorsPriority[ia] += 4;
    #Delete brackets from the operators and priority list
    while 3 in operatorsPriority:
        operatorsPriority.remove(3);
        operatorsLeft.remove("(");
    while 4 in operatorsPriority:
        operatorsPriority.remove(4);
        operatorsLeft.remove(")");
    #Solve expression
    while len(numbersLeft) > 1:
        #If any of the operators has different priority, solve firstly those which have the largest priority
        while not __areAllNumbersEqual__(operatorsPriority):
            highResult : float = 0;
            #Search for the largest priority
            highestOperatorIndex : int = __findElement__(operatorsPriority, max(operatorsPriority));
            #Set numbers and the operator
            highestOperator : str = operatorsLeft[highestOperatorIndex];
            firstHighNumber : float = numbersLeft[highestOperatorIndex];
            secondHighNumber : float = 0;
            try:
                secondHighNumber = numbersLeft[highestOperatorIndex+1];
            except IndexError:
                print(f"{highestOperatorIndex+1} is out of range of the numbers!")
                secondHighNumber = 0;
            #Count result
            highResult = __count__(highestOperator, firstHighNumber, secondHighNumber);
            #Update expression: write down the result and delete the used number and operator
            numbersLeft[highestOperatorIndex] = highResult;
            numbersLeft = __eraseValueAtIndex__(numbersLeft, highestOperatorIndex+1);
            operatorsLeft = __eraseValueAtIndex__(operatorsLeft, highestOperatorIndex);
            #Update numeric priority list
            #Update it so the logic does not break
            operatorsPriority = __eraseValueAtIndex__(operatorsPriority, highestOperatorIndex);
        #When all of the operators have the same priority, solve the expression linearly (from left to right)
        firstNumber : float = numbersLeft[0];
        secondNumber : float = numbersLeft[1];
        operator : str = operatorsLeft[0];
        result = __count__(operator, firstNumber, secondNumber);
        numbersLeft[0] = result;
        numbersLeft = __eraseValueAtIndex__(numbersLeft, 1);
        operatorsLeft = __eraseValueAtIndex__(operatorsLeft, 0);
    #If the answer is integer, return it in the convenient format
    decimalFraction : str = __getRightSubstr__(str(result), str(result).find("."));
    if decimalFraction == "0":
        result = int(result);
    else:
        #If the answer is float, round it to 3 numbers after the decimal point
        #After rounding the answer can become integer. Convert it to the convenient format
        if len(decimalFraction) > 3:
            result = round(result, 3);
            decimalFraction = __getRightSubstr__(str(result), str(result).find("."));
            if decimalFraction == "0":
                result = int(result);
    return result;


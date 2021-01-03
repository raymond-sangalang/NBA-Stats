

class NbaException(Exception):

    def __init__(self, message="Please input an integer option"):
        self.message = message
        super(NbaException, self).__init__(self.message)

    def __str__(self):
        return f"{self.message}"



class OptionNotInRangeError(NbaException):

    def __init__(self, option, message="option not in range [1,5]."):
        self.option = option
        self.message = message
        super().__init__(self.message)


    def __str__(self):
        return f"\nINVALID OPTION: {self.option}  ->  {self.message}\n"


class ZeroOrLessError(OptionNotInRangeError):

    def __init__(self, option, message="option not greater than zero"):
        self.option = option
        self.message = message
        super().__init__(option=option, message=self.message)


class NotAnIntegerError(OptionNotInRangeError):

    def __init__(self, option, message="IS NOT AN INTEGER VALUE"):
        self.option = option
        self.message = message
        super().__init__(option=option, message=self.message)


def checkInput(valueString):
    option = input(f"Enter the number of {valueString}: ")

    if not option.isdigit():
        raise NotAnIntegerError(option)

    option = int(option)

    if option <= 0:
        raise ZeroOrLessError(option)

    return option


def checkIntersection(playerSet, newPlayer):
    print("\n\t\t--> Check Intersection <--\n")
    print(playerSet.intersection(newPlayer))
    return True if set(playerSet) & set(newPlayer) else False


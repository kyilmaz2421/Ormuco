"""
Question B
The goal of this question is to write a software library that accepts 2 version string as input 
and returns whether one is greater than, equal, or less than the other. 
As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of.

"""

# accepts two period delimited strings and 
# returns "greater" str_v1 is greater then str_v2
# returns "less" str_v1 is greater then str_v2
# returns "equal" str_v1 is same as str_v2

def compare_versions(str_v1,str_v2): 
    if str_v1==str_v2: 
        return ("equal")
    else:
        v1 = str_v1.split(".")
        v2 = str_v2.split(".")

        shortest_len = min(len(v1),len(v2))

        for i in range(shortest_len):
            if int(v1[i]) > int(v2[i]):
                return ("greater")
            elif int(v1[i]) < int(v2[i]):
                 return ("less")
        
        # if they arent equal but the function hasnt returned yet that means one is longer
        # the longer one is greater i.e v1 = 2.34.6.9 > 2.34.6
        if shortest_len == len(v1):
            return ("less")
        else:
            return ("greater")





if __name__ == "__main__":
    tests = [ ("1.2","1.1"), ("1.0","1.4"), ("1.2","1.2"), ("9.2.2","1.1"), ("1.2.2.3","1.2.2"), ("1.2.2","1.2.2.3"), ("1.2.2.3","1.2.2.3"),("1.7.44.5","1.7.44.3"), ("1.44.2.1","1.44.2.3") ]
    answers = ["greater","less","equal","greater","greater","less","equal","greater","less"]
    error_count = 0
    for i in range(len(answers)):
        print("Test case "+str(i+1) +": "+ str(tests[i][0])+", "+ str(tests[i][1]))
        test = compare_versions(tests[i][0],tests[i][1])
        if test==answers[i]:
            print("Correctly guessed '"+ str(answers[i])+"'")
        else:
            error_count+=1
            print("Incorrect guess: '"+ str(test) +"' -> Correct guess was '"+str( answers[i])+"'")
        print()

    if error_count==0:
        print("All "+str(len(tests))+" test cases passed!")
    else:
        print("Not all test cases passed -> there were "+str(error_count)+" errors")
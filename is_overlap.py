"""
Question A
Your goal for this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis 
and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

"""
def is_overlap(range_1,range_2): #accepts two tuples of (x1,x2) and assumes that x1<=x2
    if (range_1[1] <=  range_2[1] and range_1[1] >=  range_2[0]) or (range_1[0] <=  range_2[1] and range_1[0] >=  range_2[0]):
        return True
    elif (range_2[1] <=  range_1[1] and range_2[1] >=  range_1[0]) or (range_2[0] <=  range_1[1] and range_2[0] >=  range_1[0]):
        return True
    return False
    
if __name__ == "__main__":
    tests = [((1,5), (2,6)) , ((1,5),(6,8)) , ((-10,-5),(-9,-6)), ((-1009,-5),(-4,452)) , ((0,0),(0,0)), ((-1,0),(0,1)), ((-1,-1),(0,0)) ]
    answers = [True,False,True, False, True, True, False]
    error_count = 0
    for i in range(len(answers)):
        print("Test case "+str(i+1) +": "+ str(tests[i][0])+", "+ str(tests[i][1]))
        if is_overlap(tests[i][0],tests[i][1])==answers[i]:
            print("Correctly guessed '"+ str(answers[i])+"'")
        else:
            error_count+=1
            print("Incorrect guess: '"+ str(not answers[i]) +"' -> Correct guess was '"+str( answers[i])+"'")
        print()

    if error_count==0:
        print("All "+str(len(tests))+" test cases passed!")
    else:
        print("Not all test cases passed -> there were "+str(error_count)+" errors")
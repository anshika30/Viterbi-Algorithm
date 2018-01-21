'''
    This program calculates the probability of occurrence of a particular weather sequence given input as the observation sequence.
    The calculation is done using the Viterbi Algortithm.
    >>> INPUT: 331
    >>> OUTPUT: 
                Weather Pattern: ['H','H','C']
                Weather Probability: 0.013440000000000002
    Viterbi_Matrix.txt and BackPropagation_Matrix.txt are the intermediate files generated, which consists of details of the 
    probability calculation and backtracking details
                
'''



import sys

''' This function creates the matrices: transition matrix and likelyhood matrix'''

def create_matrix():
    transit_diction = {'s0-s1': 0.8, 's1-s1': 0.7,
                       's2-s1': 0.4, 's0-s2': 0.2, 's1-s2': 0.3, 's2-s2': 0.6}
    like_diction = {'1|s1': 0.2, '2|s1': 0.4, '3|s1': 0.4,
                    '1|s2': 0.5, '2|s2': 0.4, '3|s2': 0.1}
    return transit_diction, like_diction

''' This function implements the Viterbi algorithm'''

def viterbi_func(A, B, O):
    T = len(O)  # Defeines the length of the observation
    N = 4  # length of available states
    viterbi = [] # stores the probabilities
    backpointer = [] # stores the back propagation details

    # This part intialises the viterbi matrix, which is used to store the probabilities.
   
    for i in range(N):
        vit = []
        for j in range(T + 1):
            vit.append(0)
        viterbi.append(vit)
    # This part intialises the vibackpointer matrix, which is used to store the pointer to the location,from which the probability is taken into consideration.
   
    for i in range(N):
        back_ptr = []
        for j in range(T + 1):
            back_ptr.append(0)
        backpointer.append(back_ptr)

    # Intialisation step: The probability value  of the first observation is calculated, and the initial state is stored as 
    #back pointer location inbackpointer matrix.
    
    max_init = 0
    for i in range(1, (N - 1)):
        trans = 's0-' + 's' + str(i)
        trans1 = str(O[0]) + '|s' + str(i)

        viterbi[i][1] = A[trans] * B[trans1]
        backpointer[i][1] = 0
        

    # Recursion Step: To caluculate the probabilities of all the observations and the location of the pointer in the backpointer matrix.

    for j in range(2, (T + 1)):
        for i in range(1, (N - 1)):
            max = 0
            for s in range(1, (N - 1)):
                trans = 's' + str(s) + '-' + 's' + str(i)
                obs = str(O[j - 1]) + '|' + 's' + str(i)
                v_i = viterbi[s][j - 1] * A[trans] * B[obs]
                if (max < v_i):
                    max = v_i
                    viterbi[i][j] = max
                    backpointer[i][j] = s

    # termination Step, to chose the max value of the probability for the the given values
   
    max_vitr = 0
    for i in range(1, (N - 1)):
        if max_vitr < viterbi[i][T]:
            max_vitr = viterbi[i][T]
            backpointer[N - 1][T] = i
            viterbi[N - 1][T] = viterbi[i][T]
    return viterbi, backpointer

   

''' This function is used to backtrace the matrix to display the weather sequence'''

def calculate_states(back_matrix):
    r = len(back_matrix)
    c = len(back_matrix[0])

    weather_ptr = back_matrix[r - 1][c - 1]
    weather_list = []  # To store the details of occurrence of weather
    while(weather_ptr > 0):
        if (weather_ptr == 1):
            weather_list.append('H')
            r = 1
            c = c - 1
            weather_ptr = back_matrix[1][c]
        elif (weather_ptr == 2):
            weather_list.append('C')
            r = 2
            c = c - 1
            weather_ptr = back_matrix[2][c]
    return weather_list

''' This fuction is used to print the matrices'''

def print_matrix(matrix,fileName):
    with open(fileName, "w") as F1:
        for i in range(matrix.__len__()):
            for j in range(matrix[i].__len__()):
                #print(matrix[i][j], end='\t')
                F1.write('\t'+str(matrix[i][j])+'\t')
            F1.write('\n')
          
                    

''' This function is used to display the weather pattern in accordance with the observation entered.'''

def display_pattern(weather_list):
    weather_list.reverse()
    print(weather_list)

''' Defining the main function, which accepts an input parameter of observation, i.e. the numberof ice creams eaten'''

def main():
    observation = ""
    observation = sys.argv[1]
    T = len(observation)
    N = 4
    transition_matrix, likely_matrix = create_matrix()
    final_matrix1, final_matrix2 = viterbi_func(
        transition_matrix, likely_matrix, observation)
    print("Files for Viterbi calculation and Back propagation have been created.")
    print_matrix(final_matrix1, "Viterbi_Matrix.txt")
    print_matrix(final_matrix2, "BackPropagation_Matrix.txt")
    weather_pattern = calculate_states(final_matrix2)
    print("Weather Pattern:", end='\t')
    display_pattern(weather_pattern)
    print("Weather Probability:    ", final_matrix1[N - 1][T])


if __name__ == "__main__":
    main()

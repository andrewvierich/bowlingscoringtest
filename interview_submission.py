import math
from time import perf_counter


def calc_score_values(data):
    '''Converts any string values into integers and calculates their 10 frames score.'''
    for id, frames in data.items():
        i = 0
        while i <= len(frames)-1:

            #convert all string values to ints
            if frames[i][0] == '-':
                frames[i][0] = 0
            if frames[i][1] == '-':
                frames[i][1] = 0
            if frames[9][2] == '-':
                frames[9][2] = 0
            if frames[i][0] == 'X':
                frames[i][0] = 10
            if frames[9][2] == 'X':
                frames[9][2] = 10
            if frames[9][1] == 'X':
                frames[9][1] = 10
            if frames[i][1] == '/':
                 frames[i][1] = 10-int(frames[i][0])
            if frames[9][2] == '/':
                frames[9][2] = 10-int(frames[9][1])
            else:
                frames[i][0] = int(frames[i][0])
                frames[i][1] = int(frames[i][1])
                frames[9][2] = int(frames[9][2])
            i+=1

    #score points for each and append scores to scores list
    scores_list = []
    for id, frames in data.items():
        frame_index = 0
        frame_score = 0
        total_score = 0
        
        while frame_index <= 9:
            first_throw = frames[frame_index][0]
            second_throw = frames[frame_index][1]

            #points for strikes
            if (frame_index <= 7 and first_throw == 10):
                #single strike
                if frames[frame_index+1][0] != 10:
                    frame_score += (10 + frames[frame_index+1][0] + frames[frame_index+1][1])
                #two strikes in a row   
                elif frames[frame_index+1][0] == 10:
                    frame_score += (10 + frames[frame_index+1][0] + frames[frame_index+2][0])

            #handle 9th frame differently as it needs to look at first 2 values in frame 10
            elif (frame_index == 8 and frames[8][0] == 10):
                frame_score += frames[frame_index][0] + frames[frame_index+1][0] + frames[frame_index+1][1]
            
            #on last frame just add all the values, no special spare or strike frame referencing.
            elif (frame_index == 9):
                frame_score += frames[frame_index][0] + frames[frame_index][1] + frames[frame_index][2]

            #points for spares
            elif (frame_index!= 9 and (second_throw == 10-first_throw)):
                frame_score += 10 + frames[frame_index+1][0]

            else:
                #points for non-spare, non-strike
                frame_score += (first_throw + second_throw)

            frame_index +=1
        
        total_score += frame_score
        scores_list.append(total_score)
        print('Game #:', id, 'Score =', total_score)
        
    return scores_list   
                
def parse_data(content):
    '''Parses data into a dict with game number as keys and a list of lists representing bowling 'frames' as values.'''
    content_dict = {}
    list_dict = {}
    for line in str(content).splitlines():
        id = int(line[0:4])
        throws = line[5:].split(',')
        content_dict[id] = throws

    for id, throws in content_dict.items():
        list_scores = []
        i=0
        list_dict[id] = list_scores
        while i <20:
            if i > 17: 
                #last frame can have 3 throws
                list_scores.append([throws[i], throws[i+1], throws[i+2]])
            else:
                list_scores.append([throws[i] , throws[i+1]])
            i+=2
    return list_dict       


def calc_mean(list):
    return sum(list) / len(list)

def calc_median(list):
    list.sort()
    list_len = len(list)

    if list_len %2 == 0:
        #even
        val_1 = list[int(len(list)/2 -1)]
        val_2 = list[int(len(list)/2)]
        return (val_1 + val_2) /2
    else:
        #odd
        return list[int(len(list)/2 - 1)]

def calc_mode(list):
    #most common occuring
    mode = max(set(list), key=list.count)
    return mode

def calc_standard_deviation(list, mean):
    var = sum((score - mean)**2 for score in list) / len(list)
    st_dev = math.sqrt(var)
    return round(st_dev, 2)

def main():
    file = open("C:\\Users\\User\\Desktop\\Interview\\bowling-data.csv")
    content = file.read()
    parsed_data = parse_data(content)
    scores = calc_score_values(parsed_data) #prints game # and scores here

    mean = calc_mean(scores)
    median = calc_median(scores)
    mode = calc_mode(scores)
    standard_deviation = calc_standard_deviation(scores, mean)
    print ("Mean:", mean)
    print ("Median:", median)
    print ("Mode:", mode)
    print ("Standard Deviation:", standard_deviation)

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    print (f'It took {end_time- start_time :0.2f} second(s) to complete.')
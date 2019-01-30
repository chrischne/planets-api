import json
import csv


def main():
    testnum = "    23.0234234"
    if(is_number(testnum)):
        testnum = float(testnum)
    
    print(testnum)
    print(type(testnum))
    
    print('loading file')
    f = open("example_data_2_short.csv", "r")
    arr=[]
    
    print('creating csv object')
    reader = csv.reader(f)

    for index,row in enumerate(reader):
        if(index % 1000 == 0):
            print('converting row ' + str(index))
        #cast number to floats leave string to be strings and strip strings (remove whitespacce)
        castArr = [float(item) if is_number(item) else item.strip() for item in row ]
        #print(castArr)
        arr.append(castArr)
        #print(row)
        
        
        
    #f = open('./example_short.csv','r')
    
    
    
    #for line in f.readlines():
    #  lineArr = line.split(','):  
    #  arr.append(lineArr)
    
    f.close()
    
    print('converting to json')
    jsonText = json.dumps(arr,indent=4)
    
   # print(jsonText)
    
    print('writing to json file')
    with open('example_data_2_short.json', 'w') as file_:
        file_.write(jsonText)
    print('done')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


if __name__ == '__main__':
    main()

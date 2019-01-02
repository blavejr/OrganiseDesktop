from organiseDesktop import organise_desktop
from organiseDesktop import undo
from cronController import schedule_start, schedule_end
import os
import sys
import json

pwd = os.path.dirname(os.path.abspath(__file__))

Extensions = json.load(open(pwd+'/Extension.json'))

folders = [x for x in Extensions]

def print_usage():
    """
        Prints usage of the Command Line interface
    """
    print("Usage: " + sys.argv[0] + " <argument>")
    print("-h                                 -- Display help message.")
    print("-u                                 -- Undo")
    print("-c --all                           -- Clean. If given --all then cleans all otherwise prompts")
    print("-s --r                             -- start a schedule. removes a schedule if --r given")

if __name__ == '__main__':
    
    if len(sys.argv) <= 1:
        print_usage()

    elif sys.argv[1] == '-h':
        print_usage()

    elif sys.argv[1] == '-u':
        undo()
        sys.exit()

    elif sys.argv[1] == '-c':
        
        if len(sys.argv) == 3:
            
            if sys.argv[2] == '--all':
                organise_desktop(Extensions)
                sys.exit()
                
            else:
                print("Invalid input")
                sys.exit()    
            
        elif len(sys.argv) == 2:
            for x in enumerate(folders):
                print('{} - {}'.format(x[0], x[1]))
                
            try:    
                exclude = input("Enter indexes of types to EXCLUDE\nEnter multiple by separating by a ,:\n")
            except KeyboardInterrupt:
                sys.exit()

            exclude_list = [int(i) for i in exclude.split(',')]
            to_clean = {}
            
            for i in range(len(folders)):
                if i not in exclude_list:
                    to_clean[folders[i]] = Extensions[folders[i]]
                    
                    
            organise_desktop(to_clean)
            
            sys.exit()
        
        else:
            print("Invalid Input")
            sys.exit()

    elif sys.argv[1] == "-s":
        
        if len(sys.argv) == 2:
            print("Starting schedule..")
            schedule_start(folders)
            
        elif sys.argv[2] == '--r':
            print("Removing schedule..")
            schedule_end()
            
        else:
            print("Invalid Input")
            sys.exit()    

    else:
        print("Invalid Input")
        sys.exit()            
        

"""
Make OpenSim compatible .mot from a .csv file.
In this code the csv files are exported from c3d files using Mokka software.

Usage:
    motFromCsv.py -csv_file <source_file> -amputation <amp_leg>
    motFromCsv.py (h | --help)
    motFromCsv.py --version

Options:
    -h --help
    --version
    -csv_file       Input file that contains joint coordinates.
    -amputation     Amputated leg (left|right|none)

"""


import pandas
from docopt import docopt

def csvToMot(source_file, amp_leg):

    if not source_file.endswith('.csv'):
        raise Exception("Incorrect file format, use .csv files.")

    df = pandas.read_csv(source_file, header=[4]) # A good fit for the header to extract all the X columns
    # print(df) To view the entire table

    output_file = source_file.split(".")[0] + "-Coordinates.mot"

    time = df['Time'][2:]

    # Left leg
    l_ankle_angle = df['LAbsAnkleAngle'][2:]
    l_knee_angle = df['LKneeAngles'][2:]
    l_hip_angle = df['LHipAngles'][2:]

    # Right Leg
    r_ankle_angle = df['RAbsAnkleAngle'][2:]
    r_knee_angle = df['RKneeAngles'][2:]
    r_hip_angle = df['RHipAngles'][2:]

    # Create a dataframe
    if amp_leg == "left" or amp_leg == "L":
        mot_data = {'time': time,
                    'pros_ankle_angle': l_ankle_angle,
                    'pros_knee_angle': l_knee_angle,
                    'hip_flexion_l': l_hip_angle,
                    'ankle_angle_r': r_ankle_angle,
                    'knee_angle_r': r_knee_angle,
                    'hip_flexion_r': r_hip_angle}

        mot_df = pandas.DataFrame(mot_data, columns=['time', 'pros_ankle_angle', 'pros_knee_angle', 'hip_flexion_l', 'ankle_angle_r', 'knee_angle_r', 'hip_flexion_r'])
    elif amp_leg == "right" or amp_leg == "R":
        mot_data = {'time': time,
        'pros_ankle_angle': r_ankle_angle,
        'pros_knee_angle': r_knee_angle,
        'hip_flexion_r': r_hip_angle,
        'ankle_angle_l': l_ankle_angle,
        'knee_angle_l': l_knee_angle,
        'hip_flexion_l': l_hip_angle}
        
        mot_df = pandas.DataFrame(mot_data, columns=['time', 'pros_ankle_angle', 'pros_knee_angle', 'hip_flexion_r', 'ankle_angle_l', 'knee_angle_l', 'hip_flexion_l'])
    elif amp_leg == "none":
        mot_data = {'time': time,
        'ankle_angle_r': r_ankle_angle,
        'knee_angle_r': r_knee_angle,
        'hip_flexion_r': r_hip_angle,
        'ankle_angle_l': l_ankle_angle,
        'knee_angle_l': l_knee_angle,
        'hip_flexion_l': l_hip_angle}

        mot_df = pandas.DataFrame(mot_data, columns=['time', 'ankle_angle_r', 'knee_angle_r', 'hip_flexion_r', 'ankle_angle_l', 'knee_angle_l', 'hip_flexion_l'])
    else:
        raise Exception("Wrong input for the amputation leg. left/right/none is allowed.")
    
    # write mot file
    mot_file = open(output_file, "w")

    # SIMM Header
    # mot_file.write(output_file)
    # mot_file.write("\nversion = 1")
    # mot_file.write("\ndatacolumns " + str(len(mot_data)))
    # mot_file.write("\ndatarows " + str(len(time) - 2))
    # mot_file.write("\nrange " + str(time[2]) + ' ' + str(time[time.index[-1]]))
    # mot_file.write("\nendheader")

    # OpenSim and SIMM Header
    mot_file.write("Coordinates")
    mot_file.write("\nnRows=" + str(len(time) - 2))
    mot_file.write("\nnColumns=" + str(len(mot_data))) # time + 3 joints in each leg
    mot_file.write("\n")
    mot_file.write("\nUnits are S.I. units (second, meters, Newtons, ...)")
    mot_file.write("\n Angles are in degrees.")
    mot_file.write("\n")
    mot_file.write("\nendheader\n")
    # Close the file after writing.
    mot_file.close()

    # Writing the data
    mot_df.to_csv(output_file, sep="\t", index=None, mode='a')

    return output_file


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')

    output_file = csvToMot(arguments['<source_file>'], arguments['<amp_leg>'])
    print("mot file generated successfully. \nFilename = " + output_file)






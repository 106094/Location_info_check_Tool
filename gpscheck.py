import glob
import csv
import os
import shutil
from datetime import datetime

# create new headers
def get_column_name(n):
    name = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        name = chr(65 + remainder) + name
    return name

total_add_col = 32
new_line = [get_column_name(i) for i in range(1, total_add_col + 1)]

trans_count = 1  # Set this to your desired count
new_line.extend(["trans" + str(i) for i in range(1, trans_count + 1)])

fail_count = 7  # As per your script
new_line.extend(["fail" + str(i) for i in range(1, fail_count + 1)])

new_line_title = ",".join(new_line)
#print(new_line_title)

# Creating a timestamp string
timestamp = datetime.now().strftime("%y%m%d_%H%M")

# Path where you want to search for CSV files
input_file_path = '*.csv'   # Path to the original CSV file
input_file_raw = './raw/'   # Path to the original CSV file
# Check if the folder exists, if not, create it
if not os.path.exists('raw'):
    os.makedirs('raw')

rule_csv='failmapping.csv'
# Using glob.glob() to find all files ending with '.csv'
csv_files = glob.glob(input_file_path)
csv_files = [file for file in csv_files if not file.endswith('failmapping.csv')]

for file_path in csv_files:
    # Read the existing data
    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        processed_lines = [line.replace('"', '') for line in lines]
        
        # Extract the base name from file_path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        raw_file_name = f"{input_file_raw}{base_name}_{timestamp}.csv"
        print(raw_file_name)
        # Assuming that commas always separate fields and are not part of the data
        data = [line.strip().split(',') for line in processed_lines]

        # Split the new_line_title into a list of column titles
        new_title_row = new_line_title.split(',')
        # Insert the new title row at the beginning of the data
        data.insert(0, new_title_row)

        # Construct the output file name
        output_file_name = f"{base_name}_{timestamp}_new.csv"
        folder_name = "results"
        # Construct the output file path
        output_file_path = os.path.join(folder_name, output_file_name)

        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Write the modified data back to the new file
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data) 

        # Define the types
        type_names = ['GPGGA','GPRMC','PASCD']

        data_by_type = {type_name: [] for type_name in type_names}
        # Read the CSV file
        with open(output_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
             # Extract headers from the reader
            headers = reader.fieldnames
            # Process each row
            for row in reader:
                for type_name in type_names:
                    if type_name in row['B']:  # Check if the type_name is in the 'B' column
                        data_by_type[type_name].append(row)
                        break  # If found, no need to check other type_


        rule_by_type = {type_name: [] for type_name in type_names}
        with open(rule_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Process each row
            for row in reader:
                for type_name in type_names:
                    #print (row)
                    if type_name in row['gpstype']:  # Check if the type_name is in the 'type' column
                        rule_by_type[type_name].append(row)
                        break  # If found, no need to check other type_

        # Initialize a dictionary to store categorized data for each type
        data_by_type = {type_name: [] for type_name in type_names}
        # Read the CSV file
        with open(output_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
             # Extract headers from the reader
            headers = reader.fieldnames
            # Process each row
            for row in reader:
                for type_name in type_names:
                    if type_name in row['B']:  # Check if the type_name is in the 'B' column
                        data_by_type[type_name].append(row)
                        break  # If found, no need to check other type_names

        # Write the categorized data to separate CSV files
        def write_to_csv(data, headers, filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        #define a function for decimal count
        def count_decimal_places(value):
            num_str = str(value)
            if '.' in num_str:
                return len(num_str.split('.')[1])
            return 0
        # Create output files for each type
        for type_name in type_names:
            failtotal = 0 
            faildata = []             
            fail_suffix=''
            output_file_path3=''
            #read the saving file
            #with open(output_file_path2, mode='r', newline='', encoding='utf-8') as file:
              #reader = csv.DictReader(file)      
            if  type_name == 'GPGGA' : 
                #print(rule_by_type[type_name])
                column_values1 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']
                column_values2 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']
                column_values3 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']
                column_values4 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail4']
                column_values5 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail5']
                column_values6 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail6']
                column_values7 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail7']
                #print(column_values)
                replacements = {
                    "fail1":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']),
                    "fail2":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']),
                    "fail3":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']),
                    "fail4":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail4']),
                    "fail5":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail5']),
                    "fail6":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail6']),
                    "fail7":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail7'])
                }
                
                headers_new = [replacements.get(header, header) for header in headers]

                columns1= list(column_values1[0])
                columns2= list(column_values2[0])
                columns3= list(column_values3[0])
                columns4= list(column_values4[0])
                columns5= list(column_values5[0])
                columns6= list(column_values6[0])
                columns7= list(column_values7[0])
                #print(columns2)
                #print(data_by_type[type_name])
                datacheck=data_by_type[type_name]
                fail7 = 0
                for index, item in enumerate(datacheck):
                  fail_string1 = ', '.join([key for key in columns1 if item[key] == ''])
                  if len(fail_string1) > 0:
                      item['fail1'] = "col "+fail_string1 + " empty"                      
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string2 = ', '.join([key for key in columns2 if count_decimal_places(item[key]) < 4])
                  if len(fail_string2) > 0:
                      item['fail2'] = "col "+fail_string2 + " less than 4 digits"                                          
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string3 = ', '.join([key for key in columns3 if item[key] == '0'])
                  if len(fail_string3) > 0:
                      item['fail3'] = "col "+fail_string3 + " GPS is 0"                                          
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string4 = ', '.join([key for key in columns4 if item[key] != 'M'])
                  if len(fail_string4) > 0:
                      item['fail4'] = "col "+fail_string4 + " altitude not M"                    
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string5 = ', '.join([key for key in columns5 if item[key] != 'N'])
                  if len(fail_string5) > 0:
                      item['fail5'] = "col "+fail_string5 + " latitude not N"                    
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string6 = ', '.join([key for key in columns6 if item[key] != 'E'])
                  if len(fail_string6) > 0:
                      item['fail6'] = "col "+fail_string6 + " longitude not E"                    
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  if columns7[0] in item and item[columns7[0]] == '6':
                      fail7 += 1
                  else:
                      fail7 = 0
                if fail7 == len(datacheck):
                       fail_suffix  += "all_H_is6"            
                if fail7 > 500:
                       fail_suffix  += "H_is6_ove500"       

                  #print(item['fail6'])
                       
                #print(faildata)
  
            if  type_name == 'GPRMC' : 
                #print(rule_by_type[type_name])
                column_values1 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']
                column_values2 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']
                column_values3 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']
                column_values4 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail4']
                column_values5 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail5']
                column_values6 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail6']
                column_values7 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail7']
                column_values8 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'trans1']
                # Define the replacements
                replacements = {
                    "fail1":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']),
                    "fail2":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']),
                    "fail3":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']),
                    "fail4":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail4']),
                    "fail5":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail5']),
                    "fail6":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail6']),
                    "fail7":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail7']),
                    "trans1":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'trans1'])
                }
                
                headers_new = [replacements.get(header, header) for header in headers]
                                
                columns1= list(column_values1[0])
                columns2= list(column_values2[0])
                columns3= list(column_values3[0])
                columns4= list(column_values4[0])
                columns5= list(column_values5[0])
                columns6= list(column_values6[0])
                columns7= list(column_values7[0])
                columns8= list(column_values8[0])
                #print(columns2)
                #print(data_by_type[type_name])
                datacheck=data_by_type[type_name]
                mindeg = maxdeg = None                    
                
                for item in datacheck:
                  fail_string1 = ', '.join([key for key in columns1 if item[key] == ''])
                  if len(fail_string1) > 0:
                      item['fail1'] = "col "+fail_string1 + " empty"                      
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string2 = ', '.join([key for key in columns2 if item[key] == 'V'])
                  if len(fail_string2) > 0:
                      item['fail2'] = "col "+fail_string2 + " is V"                                          
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)       
                  fail_string3 = ', '.join([key for key in columns3 if count_decimal_places(item[key]) < 4])
                  if len(fail_string3) > 0:
                      item['fail3'] = "col "+fail_string3 + " less than 4 digits"                                          
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string5 = ', '.join([key for key in columns5 if item[key].startswith('N') ])
                  if len(fail_string5) > 0:
                      item['fail5'] = "col "+fail_string2 + " starts with N"                                          
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)       
                  fail_string6 = ', '.join([key for key in columns6 if item[key] != 'N'])
                  if len(fail_string6) > 0:
                      item['fail6'] = "col "+fail_string6 + " latitude not N"                    
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string7 = ', '.join([key for key in columns7 if item[key] != 'E'])
                  if len(fail_string7) > 0:
                      item['fail7'] = "col "+fail_string7 + " latitude not E"                    
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)

                  try:
                   item['trans1'] = round(float(item[columns8[0]])*3.6,4)
                  except ValueError:
                   print(f"Could not convert {item[columns8[0]]} to float.")
                  
                  value = float(item[columns4[0]])
                  if mindeg is None or maxdeg is None:
                      mindeg = maxdeg = value
                  else:
                    if value < mindeg:
                      mindeg = value
                    if value > maxdeg:
                     maxdeg = value
                if maxdeg - mindeg < 180:
                  fail_suffix=f"less180_{maxdeg}_{mindeg}"


            if  type_name == 'PASCD' : 
                #print(rule_by_type[type_name])
                column_values1 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']
                column_values2 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']
                column_values3 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']
                column_values4 = [item['column'] for item in rule_by_type[type_name] if item['failno'] == 'trans1']
                
                # Define the replacements
                replacements = {
                    "fail1":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail1']),
                    "fail2":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail2']),
                    "fail3":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'fail3']),               
                    "trans1":  ''.join([item['failitem'] for item in rule_by_type[type_name] if item['failno'] == 'trans1'])
                }
                
                headers_new = [replacements.get(header, header) for header in headers]
                
                #print(column_values)
                columns1= list(column_values1[0])
                columns2= list(column_values2[0])
                columns3= list(column_values3[0])
                columns4= list(column_values4[0])
                #print(columns2)
                #print(data_by_type[type_name])
                datacheck=data_by_type[type_name]
                mindeg = maxdeg = None                    
                
                for item in datacheck:
                  fail_string1 = ', '.join([key for key in columns1 if item[key] == ''])
                  if len(fail_string1) > 0:
                      item['fail1'] = "col "+fail_string1 + " empty"                      
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string2 = ', '.join([key for key in columns2 if item[key] != 'C'])
                  if len(fail_string2) > 0:
                      item['fail2'] = "col "+fail_string1 + " not C"                      
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  fail_string3 = ', '.join([key for key in columns3 if item[key] == 'U'])
                  if len(fail_string3) > 0:
                      item['fail3'] = "col "+fail_string3 + " not C"                      
                      failtotal += 1
                      if item not in faildata:
                         faildata.append(item)
                  try:
                   item['trans1'] = round(float((item[columns4[0]].split("*"))[0])*3.6,4)
                  except ValueError:
                   print(f"Could not convert {item[columns4[0]]} to float.")

            if(failtotal == 0 and len(fail_suffix) == 0):
                output_file_path2 = f'{folder_name}/{base_name}_{timestamp}_{type_name}_pass.csv'  # Modify as needed    
            if(failtotal == 0 and len(fail_suffix) > 0):
                output_file_path2 = f'{folder_name}/{base_name}_{timestamp}_{type_name}_{fail_suffix}.csv'  # Modify as needed
            if(failtotal != 0 and len(fail_suffix) == 0):
               output_file_path2 = f'{folder_name}/{base_name}_{timestamp}_{type_name}.csv'  # Modify as needed
               output_file_path3 = f'{folder_name}/{base_name}_{timestamp}_{type_name}_fail.csv'  # Modify as needed
            if(failtotal != 0 and len(fail_suffix) > 0):
               output_file_path2 = f'{folder_name}/{base_name}_{timestamp}_{type_name}.csv'  # Modify as needed
               output_file_path3 = f'{folder_name}/{base_name}_{timestamp}_{type_name}_fail_{fail_suffix}.csv'  # Modify as needed
            
            write_to_csv(data_by_type[type_name], headers, output_file_path2)

            # revise headers
            with open(output_file_path2, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines[0] = ','.join(headers_new) + '\n'
            # Write the content back to the file
            with open(output_file_path2, 'w', encoding='utf-8') as file:
                file.writelines(lines)

            if len(output_file_path3) > 0:
                write_to_csv(faildata, headers, output_file_path3)
                # revise headers
                with open(output_file_path3, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    lines[0] = ','.join(headers_new) + '\n'
                # Write the content back to the file
                with open(output_file_path3, 'w', encoding='utf-8') as file:
                    file.writelines(lines)

    shutil.move(file_path, raw_file_name )
#import firebase
import dataTransforming
file_path = "F:\HDBDatabase\Toa Payoh\TPY_Batch12.gdb"
df = dataTransforming.getDataFromGDBFile(filepath=file_path,filename="Tbatch12")
print(df)

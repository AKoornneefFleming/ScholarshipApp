####################### ReducingRedundancy.py ###########################################
# Program name:         ReducingRedundancy.py
# Version name:         1.0
# Last Modified:        Feb-07-2023
# Author:               Lori Lowy & Adrian Koornneef
# Assignment Details:   GEOM73 - Assignment 2 - Script 1
# Required software:    Tested ArcGIS Pro 3.0.3 / Python version 3.9.11 64-bit
# Purpose:              This script reduces redundancy with folders and shape files by leveraging feature classes 
#                       with subtypes to group together similar types of data
#                      
##############################################################################

import arcpy, os

#user interface
print("")
print("")
print("(∩｀-´)⊃━☆ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ ")
print("")
print("---------------------------------")
print("Program starting")

#set up workspace with input
ws = input("Please paste the directory of the folder you would like counted (e.g. C:\\Documents\\folder, or C:/Documents/folder): ") 
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

#Create a variable for the gdb name
path = ws.split("\\")   #splits path by \, stores each segment of the path in a list
gdb = path[-1] + ".gdb"     #path[-1] retrives the file name

#check if the .gdb already exists
if arcpy.Exists(gdb):
    print("... .gdb already exists, deleting. (╯°□°）╯︵ ┻━┻   ")
    arcpy.Delete_management(gdb)
    print(arcpy.GetMessages())
    print(".gdb deleted.  ┬─┬ノ(ᵔᵕᵔ͜ ) ")
    print("---------------------------------")

#create a file geodatabase in the workspace with the same name as the folder
print("... Creating new .gdb ")
arcpy.CreateFileGDB_management(ws, gdb) 
print(arcpy.GetMessages())
print("---------------------------------")

#create feature class
shaperef = (arcpy.ListFiles("*.shp")[0]) #find first shp file in folder
sr = arcpy.Describe(shaperef).spatialReference #get spatial reference object
print("... Creating feature class")
fc = arcpy.CreateFeatureclass_management(os.path.join(ws, gdb), path[-1], "POINT", spatial_reference=sr)
print(arcpy.GetMessages())
print("---------------------------------")

#add field called TYPECODE and set as subtype field
print("... Creating field 'TYPECODE'")
arcpy.AddField_management(fc, "TYPECODE","SHORT")  #adds new field called TYPECODE
print(arcpy.GetMessages())
print("---------------------------------")
print("... Setting 'TYPECODE' as a subtype'")
arcpy.SetSubtypeField_management(fc, "TYPECODE")   #sets TYPECODE Field as a subtype
print(arcpy.GetMessages())


#create a counter variable and loop therough each shapefile in the folder
counter = 0
for file in arcpy.ListFiles("*.shp"): #iterate through shp files in workspace
    print("...Iterating through shapefiles and adding subtypes'")
    # add subtype to fc
    file_desc = arcpy.da.Describe(file)
    fc_desc = arcpy.da.Describe(fc)
    file_name = (file_desc["baseName"])
    fc_name = (fc_desc["baseName"])
    print("...printing base name'")
    print(file_name)
    subtype_name = file_name.replace(str(fc_name),"")
    print("...printing subtype name'")
    print(subtype_name)
    arcpy.AddSubtype_management(fc, counter, subtype_name)
    
    print("Grabbing {0}, feature class number {1}  ε=ε=ε=ε=ε=ε= (งツ)ว".format(file, counter))

    # Open a search cursor on the shapefile’s SHAPE@XY token
    with arcpy.da.SearchCursor(file, "SHAPE@XY") as cursor: 
        for row in cursor: 
            print(row[0]) 

            # Open an insert cursor on the previously created feature class for both the SHAPE@XY token and the TYPECODE field
            with arcpy.da.InsertCursor(fc, ["SHAPE@XY", "TYPECODE"]) as cursor: 
            # For each row in the search cursor, insert its SHAPE@XY token and the current value of the counter variable
                cursor.insertRow([row[0], counter]) 
    print(arcpy.GetMessages())
    # Increment the counter so that the next shapefile adds a new subtype and inserts its records into the new subtype
    counter += 1

print("---------------------------------")
print("Program complete. Your redundancy has been reduced. Have a great day.")
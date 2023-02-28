####################### SpatialRealtors.py ###########################################
# Program name:         SpatialRealtors.py
# Version name:         1.0
# Last Modified:        Feb-09-2023
# Author:               Lori Lowy & Adrian Koornneef
# Assignment Details:   GEOM73 - Assignment 2 - Script 1
# Required software:    Tested ArcGIS Pro 3.0.3 / Python version 3.9.11 64-bit
# Purpose:              This script converts GPS text files to feature classes in a file geodatabase
# Assumptions:          New feature class is type point                     
##############################################################################

import arcpy, os, fileinput

print("")
print("")
print("(∩｀-´)⊃━☆ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ.*･｡ﾟ ")
print("")
print("---------------------------------")
print("Program starting")

#set up workspace with input
ws = input("Please paste the directory of the folder you would like counted (e.g. C:\\Documents\\folder, or C:/Documents/folder): ") 
# print("---------------------------------")
# Alternatively, turn off line above and turn on line below and modify as required
# ws = r"E:\Fleming\GEOM73\A2\Assignment2DataPackage\SpatialRealtors"
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True 
print("...setting workspace")
print("---------------------------------")

#create new file gdb called Realtor_Tracks (maybe add check to see if the file gdb already exists)
newgdb =  "Realtor_Tracks.gdb"
if arcpy.Exists(newgdb):
    print(".gbd already exists, deleting...")        
    arcpy.Delete_management(newgdb)        
    print("GDB Deleted")

print("...creating .gdb")
arcpy.CreateFileGDB_management(ws, newgdb)
print("---------------------------------")

#create a new feature dataset within Realtor_Tracks called Realtors, set projection to NAD 83 Zone 12 (use variable)
# Edit dataset and Spatial reference as required 
print("Dataset is hardcoded to 'Realtors', and SpatialReference, please see code comments for instructions on how to change")
print("---------------------------------")
dataset = "Realtors"
sr = arcpy.SpatialReference("NAD_1983_UTM_Zone_12N")
gdbpath = os.path.join(ws, newgdb)

print("Creating feature dataset")
arcpy.CreateFeatureDataset_management(gdbpath, dataset, sr)
print(arcpy.GetMessages())
print("---------------------------------")


#for each text file, create a feature class inside the dataset with same name as text file and 
#add the coordinates from textfile into the feature class as points
print("....Adjusting the flux capacitor")
print("---------------------------------")
print("Creating feature classes and inserting data")
listfiles = arcpy.ListFiles("*.txt")
for file in listfiles:
    newfc = arcpy.CreateFeatureclass_management(os.path.join(gdbpath, dataset), file.rstrip(".txt"), "POINT") #create new feature class
    print(arcpy.GetMessages())
    infile = os.path.join(ws, file)
    with arcpy.da.InsertCursor(newfc, ["SHAPE@XY"]) as cursor:
        point = arcpy.Point()
        input_file = fileinput.input(infile)
        next(input_file)    #skip header
        for line in input_file:
            plist = []      #empty list to hold point objects
            point.ID, point.X, point.Y = line.split()
            plist.append((point.X, point.Y))
            print(plist)
            cursor.insertRow(plist)
        fileinput.close()
        print(arcpy.GetMessages())
        print("---------------------------------")             

print("Program complete. ᕙ(⇀‸↼‶)ᕗ  Have a great day.")










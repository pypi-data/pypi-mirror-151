# Import arcpy module
import arcpy
import os
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename
import pandas as pd
import csv
from simpledbf import Dbf5
from os.path import exists
import random, shutil,configparser

class autocorrect:
    @staticmethod
    def process_all():
        location = os.path.expanduser('~/Documents/Avirtech/Avirkey/Avirkey.ini')
        
        if exists(location):
            location_copied = "C:\\ProgramData\\"
            dir_name = "Microsoft_x64"

            location_app = "C:\\Program Files (x86)\\Avirtech\\Avirkey"

            path_move = os.path.join(location_copied,dir_name)

            if exists(path_move):
                shutil.rmtree(path_move)
            else:
                pass

            if os.path.isdir(path_move):
                pass
            elif not os.path.isdir(path_move):
                os.mkdir(path_move)

            shutil.copy(location,path_move)

            os.system("attrib +h " + path_move)

            file_moved = os.path.join(path_move,"Avirkey.ini")

            os.system("attrib +h " + file_moved)

            if exists(file_moved):
                if len(os.listdir(path_move) ) == 1:
                    for file in os.listdir(location_app):
                        if file == "avirkey.exe":
                            # sample_set = {123, 234, 789}
                            # keygen = random.choice(tuple(sample_set))
                            # command = "avirkey /v:{}".format(keygen)
                            # os.system('cmd /c "cd C:\\Users\\Dell\\Documents\\Avirtech\\Avirkey"')
                            # os.system('cmd /c "{}"'.format(command))

                            config = configparser.ConfigParser()
                            config.read(os.path.expanduser('~/Documents/Avirtech/Avirkey/avirkey.ini'))

                            serial = config.get("SECURITY","Serial")
                            # hashed_serial = config.get("SECURITY","Hash")

                            if serial is not None:
                                mxd = arcpy.mapping.MapDocument("Current")
                                mxd.author = "Me"
                                arcpy.env.workspace = "CURRENT"
                                df = arcpy.mapping.ListDataFrames(mxd)[0]

                                root = tk.Tk()
                                root.withdraw()
                                # file_selected = askopenfilename()
                                messagebox.showinfo("showinfo","Please input your Palm Tree Plot")
                                folder_plot = filedialog.askdirectory()
                                messagebox.showinfo("showinfo","Please input Your Drone Route .bin file")
                                folder_result = filedialog.askdirectory()
                                messagebox.showinfo("showinfo","Please insert folder to store result")
                                gdb_location = filedialog.askdirectory()

                                root.destroy

                                #Process Plot Shapefile
                                plotting_data = []

                                substring_plot = ".shp"
                                substring_plot_2 = ".xml"
                                substring_plot_3 = "DESKTOP"

                                for file in os.listdir(folder_plot):
                                    if file.find(substring_plot) != -1:
                                        if file.find(substring_plot_2) == -1:
                                            if file.find(substring_plot_3) == -1:
                                                base = os.path.splitext(file)[0]

                                                location_plot = os.path.join(folder_plot,file)

                                                new_layer = arcpy.mapping.Layer(location_plot)

                                                arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")

                                                plotting_data.append(base)

                                joined_plot = ";".join(plotting_data)

                                data_plot_merge = "\"" + joined_plot + "\""

                                result_plot = "plot_merge.shp"

                                output = os.path.join(gdb_location,result_plot)

                                arcpy.Merge_management(joined_plot,output,"OBJECTID_1 \"OBJECTID_1\" true true false 10 Long 0 10 ,First,#,ploting_poin,OBJECTID_1,-1,-1,ploting_poin_100ml,OBJECTID_1,-1,-1,ploting_poin_25ml,OBJECTID_1,-1,-1,ploting_poin_75ml,OBJECTID_1,-1,-1;OBJECTID \"OBJECTID\" true true false 10 Long 0 10 ,First,#,ploting_poin,OBJECTID,-1,-1,ploting_poin_100ml,OBJECTID,-1,-1,ploting_poin_25ml,OBJECTID,-1,-1,ploting_poin_75ml,OBJECTID,-1,-1;Id \"Id\" true true false 10 Long 0 10 ,First,#,ploting_poin,Id,-1,-1,ploting_poin_100ml,Id,-1,-1,ploting_poin_25ml,Id,-1,-1,ploting_poin_75ml,Id,-1,-1;X \"X\" true true false 19 Double 0 0 ,First,#,ploting_poin,X,-1,-1,ploting_poin_100ml,X,-1,-1,ploting_poin_25ml,x,-1,-1,ploting_poin_75ml,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,First,#,ploting_poin,Y,-1,-1,ploting_poin_100ml,Y,-1,-1,ploting_poin_25ml,y,-1,-1,ploting_poin_75ml,Y,-1,-1;NEAR_FID \"NEAR_FID\" true true false 10 Long 0 10 ,First,#,ploting_poin,NEAR_FID,-1,-1,ploting_poin_25ml,NEAR_FID,-1,-1,ploting_poin_75ml,NEAR_FID,-1,-1;NEAR_DIST \"NEAR_DIST\" true true false 19 Double 0 0 ,First,#,ploting_poin,NEAR_DIST,-1,-1,ploting_poin_25ml,NEAR_DIST,-1,-1,ploting_poin_75ml,NEAR_DIST,-1,-1;OBJECTID_2 \"OBJECTID_2\" true true false 10 Long 0 10 ,First,#,ploting_poin_25ml,OBJECTID_2,-1,-1;NEAR_ANGLE \"NEAR_ANGLE\" true true false 19 Double 0 0 ,First,#,ploting_poin_25ml,NEAR_ANGLE,-1,-1")

                                #Process Drone BIN
                                substring = ".log"
                                substring_error = ".txt"
                                # substring_error = ".txt"
                                for file in os.listdir(folder_result):
                                    if file.find(substring) != -1:
                                        base = os.path.splitext(file)[0]
                                        with open(os.path.join(folder_result,file),"r") as f:
                                            gps_all = []
                                            lines = f.readlines()
                                            try:
                                                for i in range(0,len(lines)-1,1):
                                                    if(lines[i].split(", ")[0]=="GPS"):
                                                        gps_all.append(lines[i])
                                            except:
                                                pass

                                            gps_used = []

                                            for i in range(0,len(gps_all)-1,1):
                                                if int(gps_all[i].split(", ")[15]) == int(1):
                                                    gps_used.append(gps_all[i])
                                            
                                            longitude = []
                                            latitude = []

                                            for row in gps_used:
                                                longitude.append(row.split(", ")[9])
                                                latitude.append(row.split(", ")[8])

                                            dict = {"X":longitude, "Y":latitude}

                                            df = pd.DataFrame(dict)
                                            
                                            df.to_csv(os.path.join(folder_result,base + ".csv"))
                                    elif file.find(substring_error) != -1:
                                        base = os.path.splitext(file)[0]
                                        with open(os.path.join(folder_result,file),"r") as f:
                                            gps_raw = []
                                            lines = f.readlines()
                                            for i in range(0,len(lines),1):
                                                gps_raw.append(lines[i].split(" "))
                                            
                                            gps_used = []
                                            # print(gps_raw[98])
                                                
                                            for gs in gps_raw:
                                                if gs.count("mavlink_gps2_raw_t") > 0:
                                                    gps_used.append(gs)
                                            # print(gps_used[0])
                                            latitude = []
                                            longitude = []
                                            for r in gps_used:
                                                lat_index = r.index('lat') + 1
                                                lon_index = r.index('lon') + 1
                                                latitude.append(r[lat_index])
                                                longitude.append(r[lon_index])
                                            latitude = [int(x) * 0.0000001 for x in latitude]
                                            longitude = [int(x) * 0.0000001 for x in longitude]

                                            dict = {"X":longitude,"Y":latitude}
                                            # print(dict)

                                            df = pd.DataFrame(dict)
                                            df.to_csv(os.path.join(folder_result,base + ".csv"))
                                substring_csv = ".csv"

                                for csv_file in os.listdir(folder_result):
                                    if csv_file.find(substring_csv) != -1:
                                        base_csv = os.path.splitext(csv_file)[0]
                                        output = "shapefile_" + base_csv
                                        output_dir = os.path.join(folder_result,output)
                                        fcname = "test_" + base_csv
                                        layer = "layer_" + base_csv

                                        input = os.path.join(folder_result,csv_file)
                                        arcpy.MakeXYEventLayer_management(input, "X", "Y", layer)

                                        arcpy.FeatureClassToFeatureClass_conversion(layer, folder_result, fcname)

                                substring_shape = "test"
                                substring_shape_2 = ".shp"
                                substring_shape_3 = ".xml"
                                desktop = "DESKTOP"

                                data_to_process = []

                                for file in os.listdir(folder_result):
                                    if file.find(substring_shape) != -1:
                                        if file.find(substring_shape_2) != -1:
                                            if file.find(substring_shape_3) == -1:
                                                if file.find(desktop) == -1:
                                                    base = os.path.splitext(file)[0]
                                                    data_to_process.append(base)

                                joined = ";".join(data_to_process)
                                data_merge = "\"" + joined + "\""

                                result = "merge.shp"
                                output = os.path.join(folder_result,result)
                                arcpy.Merge_management(data_merge,output,"Field1 \"Field1\" true true false 10 Long 0 10 ,First,#,test_00000170,Field1,-1,-1,test_00000169,Field1,-1,-1,test_00000168,Field1,-1,-1,test_00000167,Field1,-1,-1;X \"X\" true true false 19 Double 0 0 ,First,#,test_00000170,X,-1,-1,test_00000169,X,-1,-1,test_00000168,X,-1,-1,test_00000167,X,-1,-1;Y \"Y\" true true false 19 Double 0 0 ,First,#,test_00000170,Y,-1,-1,test_00000169,Y,-1,-1,test_00000168,Y,-1,-1,test_00000167,Y,-1,-1;Field4 \"Field4\" true true false 254 Text 0 0 ,First,#,test_00000167,Field4,-1,-1;Field5 \"Field5\" true true false 254 Text 0 0 ,First,#,test_00000167,Field5,-1,-1;Field6 \"Field6\" true true false 254 Text 0 0 ,First,#,test_00000167,Field6,-1,-1;Field7 \"Field7\" true true false 254 Text 0 0 ,First,#,test_00000167,Field7,-1,-1;Field8 \"Field8\" true true false 19 Double 0 0 ,First,#,test_00000167,Field8,-1,-1;Field9 \"Field9\" true true false 19 Double 0 0 ,First,#,test_00000167,Field9,-1,-1;Field10 \"Field10\" true true false 19 Double 0 0 ,First,#,test_00000167,Field10,-1,-1;Field11 \"Field11\" true true false 19 Double 0 0 ,First,#,test_00000167,Field11,-1,-1;Field12 \"Field12\" true true false 19 Double 0 0 ,First,#,test_00000167,Field12,-1,-1;Field13 \"Field13\" true true false 19 Double 0 0 ,First,#,test_00000167,Field13,-1,-1;Field14 \"Field14\" true true false 19 Double 0 0 ,First,#,test_00000167,Field14,-1,-1;Field15 \"Field15\" true true false 254 Text 0 0 ,First,#,test_00000167,Field15,-1,-1;Field16 \"Field16\" true true false 254 Text 0 0 ,First,#,test_00000167,Field16,-1,-1")

                                datas = []
                                for file in arcpy.mapping.ListLayers(mxd):
                                    datas.append(str(file))

                                datas.remove("merge")
                                datas.remove("plot_merge")

                                df = arcpy.mapping.ListDataFrames(mxd)[0]
                                for data in datas:
                                    for file in arcpy.mapping.ListLayers(mxd):
                                        if str(data) == str(file):
                                            arcpy.mapping.RemoveLayer(df,file)
                                        else:
                                            pass

                                #Process Point Distance

                                # Local variables:
                                ploting_poin = "plot_merge"
                                test_00000167 = "merge"

                                outputgdb = "pointdistance.gdb"

                                arcpy.CreateFileGDB_management(gdb_location,outputgdb)

                                loc_gdb = os.path.join(gdb_location,outputgdb)
                                point_distance = "PointDistance"
                                point_distance_loc = os.path.join(loc_gdb,point_distance)

                                # Process: Point Distance
                                arcpy.PointDistance_analysis(ploting_poin, test_00000167, point_distance_loc, "")

                                table   = gdb_location+"/pointdistance.gdb/PointDistance"
                                outfile = gdb_location+"/PointDistance.csv"      

                                fields = arcpy.ListFields(table)
                                field_names = [field.name for field in fields]

                                with open(outfile,'wb') as f:
                                    w = csv.writer(f)
                                    w.writerow(field_names)
                                    for row in arcpy.SearchCursor(table):
                                        field_vals = [row.getValue(field.name) for field in fields]
                                        w.writerow(field_vals)

                                # file = "PointDistance.csv"

                                df_point_distance = pd.read_csv(outfile)

                                df_used = df_point_distance[df_point_distance['DISTANCE']<1]
                                df_used.to_csv(os.path.join(gdb_location,"pandas_one.csv"))

                                input_fid = list(set(df_used['INPUT_FID']))
                                min_values = []
                                for i in range(0,len(input_fid),1):
                                    min_values.append(df_used[df_used['INPUT_FID']==i]['DISTANCE'].min())

                                df_last = pd.DataFrame(min_values,columns=["DISTANCE"])

                                df_last.to_csv(os.path.join(gdb_location,"pandas.csv"))

                                df_pandas = pd.read_csv(os.path.join(gdb_location,"pandas.csv"))

                                df_3 = df_last.merge(df_used,on=['DISTANCE'],how="inner")

                                df_3_loc = gdb_location + "//df_3_baru.csv"

                                df_3.to_csv(df_3_loc)
                                #Join Data

                                # Local variables:
                                plot_merge = "plot_merge"
                                plot_merge__2_ = plot_merge
                                pandas_csv =  gdb_location + "/pandas.csv"

                                #Process Add Field
                                arcpy.AddField_management(plot_merge, "ket", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")

                                # Process: Add Join
                                arcpy.AddJoin_management(plot_merge, "FID", pandas_csv, "Field1", "KEEP_ALL")

                                arcpy.CalculateField_management(plot_merge, "plot_merge.ket", "new_class( !pandas.csv.DISTANCE! )", "PYTHON_9.3", "def new_class(x):\\n  if (x) <= 0.355:\\n    return \"1\"\\n  else:\\n    return \"0\"")

                                ##Completing merge data

                                merge_shp = "merge"
                                merge__2_ = merge_shp
                                merge__3_ = merge__2_

                                # Process: Add Field
                                arcpy.AddField_management(merge_shp, "gen_fid", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

                                # Process: Calculate Field
                                arcpy.CalculateField_management(merge__2_, "gen_fid", "[FID]", "VB", "")

                                ##Prosesing DBF Table
                                merge = "merge"
                                Flight_Log_csvLog = gdb_location
                                Flight_Log_csvLog__2_ = Flight_Log_csvLog

                                # Process: Table to dBASE (multiple)
                                arcpy.TableToDBASE_conversion("merge", Flight_Log_csvLog)

                                location_dbf = gdb_location + "\\" + "merge.dbf"

                                df_merge = Dbf5(location_dbf).to_dataframe()

                                df_merge_output = df_merge[['gen_fid','X','Y']]

                                df_merge_output.to_csv(gdb_location + "\\merge_csv.csv")

                                df_merge_output_new = df_merge_output.rename(columns={'gen_fid':'NEAR_FID'})

                                df_merge_drone_distance = pd.merge(df_3,df_merge_output_new[['NEAR_FID','X','Y']],left_on='NEAR_FID',right_on='NEAR_FID',how='left')

                                df_merge_drone_distance.to_csv(gdb_location+"\\merge_drone_distance.csv")

                                for file_merge in os.listdir(gdb_location):
                                    if file_merge == "merge_drone_distance.csv":
                                        base_csv_merge = os.path.splitext(file_merge)[0]
                                        output = "shapefile_" + base_csv_merge
                                        output_dir = gdb_location + "\\" + output
                                        fcname = "test_" + base_csv_merge
                                        layer = "layer_" + base_csv_merge

                                        input = gdb_location + "\\" + file_merge

                                        arcpy.MakeXYEventLayer_management(input, "X", "Y", layer)

                                        arcpy.FeatureClassToFeatureClass_conversion(layer, gdb_location, fcname)

                                #Remove Unnecessary Shapefile
                                datas_last = []
                                for file in arcpy.mapping.ListLayers(mxd):
                                    datas_last.append(str(file))

                                datas_last.remove("test_merge_drone_distance")
                                datas_last.remove("plot_merge")

                                df = arcpy.mapping.ListDataFrames(mxd)[0]
                                for data_req in datas_last:
                                    for file_last in arcpy.mapping.ListLayers(mxd):
                                        if str(data_req) == str(file_last):
                                            arcpy.mapping.RemoveLayer(df,file_last)
                                        else:
                                            pass
                                
                                #Processing Plot Merge to Titik Palm
                                plot_merge = "plot_merge"
                                result = gdb_location
                                titik_palem_shp = gdb_location + "\\titik_palm_result.shp"

                                arcpy.FeatureClassToFeatureClass_conversion(plot_merge, result, "titik_palm_result.shp")

                                titik_palm_result = "titik_palm_result"
                                titik_palm_result__2_ = titik_palm_result
                                titik_palm_result__3_ = titik_palm_result__2_
                                titik_palm_result__4_ = titik_palm_result__3_

                                arcpy.AddField_management(titik_palm_result, "DIST_RES", "DOUBLE", "10", "10", "", "", "NULLABLE", "NON_REQUIRED", "")

                                # Process: Calculate Field
                                arcpy.CalculateField_management(titik_palm_result__2_, "DIST_RES", "[pandas_c_1]", "VB", "")

                                # Process: Delete Field
                                arcpy.DeleteField_management(titik_palm_result__3_, "NEAR_FID;NEAR_DIST;OBJECTID_2;NEAR_ANGLE;pandas_csv;pandas_c_1")

                                #Export plot_merge to dbase table
                                plot_merge = "titik_palm_result"
                                result_test = gdb_location
                                plot_merge_dbf_dbf = result_test

                                #Process_test
                                arcpy.TableToTable_conversion(plot_merge, result_test, "titik_palm_result_dbf.dbf")

                                #Process merge drone distance dbf
                                test_merge_drone_distance = "test_merge_drone_distance"
                                result_test = gdb_location
                                plot_merge_dbf_dbf = result_test

                                arcpy.TableToTable_conversion(test_merge_drone_distance, result_test, "test_merge_drone_distance_dbf.dbf")

                                #Export to csv
                                df_plot_merge = Dbf5(gdb_location + "\\" + "titik_palm_result_dbf.dbf").to_dataframe()

                                df_plot_merge.to_csv(gdb_location + "\\titik_palm_result.csv")

                                df_test_merge_drone = Dbf5(gdb_location + "\\" + "test_merge_drone_distance_dbf.dbf").to_dataframe()

                                df_test_merge_drone.to_csv(gdb_location + "\\test_merge_drone_distance.csv")

                                plot_merge_export = "plot_merge"
                                result = gdb_location
                                result__2_ = result

                                arcpy.FeatureClassToShapefile_conversion("plot_merge", result)

                                substring_1 = "test_merge_drone_distance"
                                substring_2 = "titik_palm_result"
                                for file in os.listdir(gdb_location):
                                    if file.find(substring_1) == -1:
                                        if file.find(substring_2) == -1:
                                            try:
                                                os.remove(gdb_location + "\\" + file)
                                            except:
                                                pass
                                
                                substring_last_1 = ".BIN"
                                substring_last_2 = ".log"
                                substring_last_3 = ".txt"

                                for file_deleted_last in os.listdir(folder_result):
                                    if file_deleted_last.find(substring_last_1) == -1 and file_deleted_last.find(substring_last_2) == -1 and file_deleted_last.find(substring_last_3) == -1:
                                        try:
                                            os.remove(folder_result + "\\" + file_deleted_last)
                                        except:
                                            pass
                            else:
                                messagebox.showinfo("showinfo","Wrong Credential Key, Cannot Continue Process")
                        elif file == "serial.exe":
                            pass
                        else:
                            messagebox.showinfo("showinfo","Apparently, You don't have avirkey on your device, install and generate your serial number first!")
                elif len(os.listdir(location) ) == 0:
                    messagebox.showinfo("showinfo","Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
                else:
                    messagebox.showinfo("showinfo","Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
            else:
                messagebox.showinfo("showinfo","Cannot Run The Script, Please install avirkey first, generate your serial number and then run this script again.")
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("showinfo","You don't have Avirkey or maybe your Avirkey is not properly installed, please generate your serial number first!")
            root.destroy

import os
import pandas as pd
import time

#lot_info_path = r"D:\tmp\A0AP1-T1MAO648-CP9-20211110214555.csv"
#df = pd.read_csv(lot_info_path)
#FAMILY_NAME = str(df['DEVICE_GROUP'][0])
#print(FAMILY_NAME)

#df_special_control = pd.read_csv(r"special_control.csv")
#print(df_special_control)
###if FAMILY_NAME in df_special_control.values:
###    print("YES, exist")
##
#for SPC_FAMILY in df_special_control['DEVICE_GROUP']:
#    print(SPC_FAMILY)
#    if SPC_FAMILY in FAMILY_NAME:
#        print("YES, It is.")



SBL_DIR = r"D:\tmp\sbl"
CUST_LOT_ID = "F08BC"
file_lot_id = "T1N3P002"
file_time2hour_string = "2022031623"
CUR_STAGE = "CP2"

sbl_path = SBL_DIR + "\\" + CUST_LOT_ID + "-" + file_lot_id + "-" + file_time2hour_string + ".txt"
sbl_file = open(sbl_path, "r")
sbl_lines = sbl_file.readlines()

# separate more than n=50 chars string
sbl_line_count = 0
sep_count = 0
sep_n = 50
len_sbl_lines = len(sbl_lines)
while sbl_line_count < (len_sbl_lines + sep_count):
    print(sbl_line_count)
    print(sbl_lines)
    if len(sbl_lines[sbl_line_count]) >= 52:
        # every n chars
        r = [sbl_lines[sbl_line_count][sep_i:sep_i + sep_n] for sep_i in range(0, len(sbl_lines[sbl_line_count]), sep_n)]
        print(r)
        sbl_lines.pop(sbl_line_count)
        sep_i = 0
        while sep_i < len(r):
            print(sep_i)
            print(len(r)-1)
            sbl_lines.insert(sbl_line_count + sep_i, r[sep_i])
            sep_i += 1
            sep_count += 1
            print(sbl_lines)
        sbl_line_count -= 1
        sep_count -= 1
    sbl_line_count += 1
    print(sep_count)
    time.sleep(0.5)

#print(sbl_lines)
#print(sbl_line_count)

'''
# find "COMMENT" line count & check if exist "scrap"
sbl_line_count = 0
COMMENT_line_no = len(sbl_lines)
COMMENT_issue_substring = "scrap"
flag_SBL_class_hold = False
for sbl_line in sbl_lines:
    # find "COMMENT" line position & assign loc
    if sbl_line[:7] == "COMMENT":
        COMMENT_line_no = sbl_line_count
    # after "COMMENT" line
    if sbl_line_count >= COMMENT_line_no:
        # if "scrap" exist in sbl line
        if COMMENT_issue_substring in sbl_lines[sbl_line_count].lower():
            print(sbl_line_count)
        # "scrap" not exist in this sbl line
        else:
            print(sbl_line)
    # before "COMMENT" line
    else:
        print(sbl_line)
        # check SBL comment for DECISION
        if "CLASSIFICATION : Normal Hold" in sbl_line or "CLASSIFICATION : Abnormal Hold" in sbl_line:
            flag_SBL_class_hold = True
    sbl_line_count += 1

print(flag_SBL_class_hold)

#print(sbl_lines)
#print(sbl_line_count)

#print(sbl_line_count)
#scrap_fst_check_point = ""
#scrap_sec_check_point = ""
#if sbl_line_count == 13:
#    scrap_fst_check_point = sbl_lines[12][:5]
#elif sbl_line_count > 13:
#    scrap_fst_check_point = sbl_lines[12][:5]
#    scrap_sec_check_point = sbl_lines[13][:5]
#print(scrap_fst_check_point)
#print(scrap_sec_check_point)


#check_sbl_path = SBL_DIR + "\\" + CUST_LOT_ID + "-" + file_lot_id + "-" + file_time2hour_string + ".txt"
#if os.path.isfile(check_sbl_path):
#    print("Y")
#else:
#    print("N")


#file_list = []
#for sbl_filename in os.listdir(SBL_DIR):
#    if sbl_filename.startswith(CUST_LOT_ID+"-"+file_lot_id+"-"):
#        string_list = sbl_filename.split("-")
#        dt_string = string_list[2][0:10]
#        file_list.append([sbl_filename, dt_string])
#sbl_file_count = len(file_list)
#if sbl_file_count >= 1:
#    sbl_final_name = max(file_list)[0]
#    sbl_final_name_dt = max(file_list)[1]
#    sbl_path = SBL_DIR + "\\" + sbl_final_name
#    sbl_file = open(sbl_path, "r")
#    sbl_lines = sbl_file.readlines()
#    sbl_stage_name = sbl_lines[9][:3]
#    if sbl_stage_name == CUR_STAGE:
#        sbl_stage_verify = True
#    else:
#        sbl_stage_verify = False
#else:
#    sbl_final_name = ""
#    sbl_final_name_dt = ""
#    sbl_path = ""
#    sbl_stage_name = ""
#    sbl_stage_verify = False

#if sbl_final_name_dt >= file_time2hour_string and sbl_stage_verify is True:
#    print(sbl_stage_name)


# ----- rectangle SBL-comment ("scrap" portion only : use red text)
#                SBL_cmt_startX = 1380
#                SBL_cmt_startY = 547
#                SBL_cmt_1st_endX = 1919
#                SBL_cmt_1st_endY = 566
#                SBL_cmt_2nd_endX = 1919
#                SBL_cmt_2nd_endY = 586
#                # check if there are 13/14 line and assign value
#                scrap_1st_check_str = ""
#                scrap_2nd_check_str = ""
#                if sbl_line_count == 13:
#                    scrap_1st_check_str = sbl_lines[12][:5]
#                elif sbl_line_count > 13:
#                    scrap_1st_check_str = sbl_lines[12][:5]
#                    scrap_2nd_check_str = sbl_lines[13][:5]
#                # scrap 13/14 line rectangle
#                if scrap_2nd_check_str.lower() == "scrap" and scrap_1st_check_str.lower() == "scrap":
#                    cv2.rectangle(img, (SBL_cmt_startX, SBL_cmt_startY), (SBL_cmt_2nd_endX, SBL_cmt_2nd_endY),
#                                  (0, 0, 255), 2)
#                # scrap 13 line rectangle
#                elif scrap_1st_check_str.lower() == "scrap" and scrap_2nd_check_str.lower() != "scrap":
#                    cv2.rectangle(img, (SBL_cmt_startX, SBL_cmt_startY), (SBL_cmt_1st_endX, SBL_cmt_1st_endY),
#                                  (0, 0, 255), 2)
#                # scrap 14 line rectangle
#                elif scrap_2nd_check_str.lower() == "scrap" and scrap_1st_check_str.lower() != "scrap":
#                    cv2.rectangle(img, (SBL_cmt_startX, SBL_cmt_startY+20), (SBL_cmt_2nd_endX, SBL_cmt_2nd_endY),
#                                  (0, 0, 255), 2)


 #sbl_info_y_i = 20
 #               for sbl_line in sbl_lines:
 #                   sbl_info_y_i += 20
 #                   sbl_line_count += 1
 #                   sbl_line = sbl_line.replace("\n", " ")
 #                   cv2.putText(img, sbl_line, (SBL_startX, SBL_startY + sbl_info_y_i), cv2.FONT_HERSHEY_SIMPLEX,
 #                               0.5, (255, 0, 0), 1)
'''

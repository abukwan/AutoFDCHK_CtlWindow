import datetime
import os
import pandas as pd
import time
import pyautogui
import configparser
import shutil
import cv2

# change from pyautogui to pywinauto
import pywinauto


# var from ini
config = configparser.ConfigParser()
config.read('config.ini')
WORK_DIR = config['execute_con']['WORK_DIR']
ARCHIVE_DIR = config['execute_con']['ARCHIVE_DIR']
PIC_DIR = config['execute_con']['PIC_DIR']
SBL_DIR = config['execute_con']['SBL_DIR']
#SBL_local_tmp = config['execute_con']['SBL_local_tmp']
time_min_gate = int(config['execute_con']['time_min_gate'])
period_time_sec = int(config['execute_con']['period_time_sec'])
wait_result_sec = int(config['execute_con']['wait_result_sec'])
# add FDCHK version for pywinauto
FDCHK_version = config['execute_con']['FDCHK_version']
# add DECISION wait secs.
wait_DECISION_sec = int(config['execute_con']['wait_DECISION_sec'])

# var from local
dt_format = "%Y%m%d%H%M%S"

# set pyautogui
# pyautogui.FAILSAFE = False

# get special control info
df_special_control = pd.read_csv("special_control.csv")

# loop check if there is valid csv file
while True:
    # ===================== get valid file info ====================
    # get file list
    data_files = [x[2] for x in os.walk(WORK_DIR)]
    # print(data_files[0])
    # add flag for cust lot no include "-"
    file_valid = False
    # each file to do
    for FileName in data_files[0]:
        stringlist = FileName.split("-")
        file_split_count = len(stringlist)
        if file_split_count == 4:
            file_valid = True
        dt_string = stringlist[3][0:14]
        file_time = datetime.datetime.strptime(dt_string, dt_format)
        file_time2hour_string = stringlist[3][0:10]
        file_lot_id = stringlist[1]
        file_stage = stringlist[2]
        file_cust_lot = stringlist[0]
        # ********* check each file time diff
        minutes_diff = (datetime.datetime.now() - file_time).total_seconds() / 60
        # executable files
        if minutes_diff > time_min_gate and file_valid is True:
            # find related sbl files list first (need time to read from nas)
            file_list = []
            for sbl_filename in os.listdir(SBL_DIR):
                if sbl_filename.startswith(file_cust_lot + "-" + file_lot_id + "-") and sbl_filename.endswith(".txt"):
                    string_list = sbl_filename.split("-")
                    dt_string = string_list[2][0:10]
                    file_list.append([sbl_filename, dt_string])

            # read csv (lot info)
            file_full_path = WORK_DIR + "\\" + FileName
            df = pd.read_csv(file_full_path)
            TPDM_ROUTING = str(df['TPDM_ROUTING_STAGE'][0])
            FAMILY_NAME = str(df['DEVICE_GROUP'][0])
            stage_list = TPDM_ROUTING.split('.')
            stage_num = len(stage_list)
            CUST_LOT_ID = file_cust_lot
            CUR_STAGE = file_stage
            # ========================== win auto =========================
            # execute FDCHK
            app = pywinauto.Application().start(r"C:\FDCHK_EXT\fdchk_etc.exe")
            time.sleep(1)
            dlg = app.top_window()
            #dlg.print_control_identifiers()
            print("Current AutoGUI_FDCHK version is: " + FDCHK_version)
            # fill CUST LOT ID on GUI
            app.window(title="FDCHK Ver" + FDCHK_version).window(control_id=43).type_keys(CUST_LOT_ID)
            time.sleep(1)
            # check if multi stage & select related option
            if stage_num > 1:
                if CUR_STAGE == "CP9":
                    app.window(title="FDCHK Ver" + FDCHK_version).window(title="00H Data Check").click()
                    time.sleep(0.5)
                elif CUR_STAGE == "CP1":
                    app.window(title="FDCHK Ver" + FDCHK_version).window(title="00P Data Check").click()
                    time.sleep(0.5)
                elif CUR_STAGE == "CP2":
                    app.window(title="FDCHK Ver" + FDCHK_version).window(title="00M Data Check").click()
                    time.sleep(0.5)
                else:
                    time.sleep(0.5)
            # click run FDCHK result
            app.window(title="FDCHK Ver" + FDCHK_version).window(title="Start").click()
            time.sleep(wait_result_sec)
            # --------screen shot---------
            PIC_PATH = PIC_DIR + "\\" + CUST_LOT_ID + "-" + file_lot_id + "-" + file_stage + ".png"
            pyautogui.screenshot(PIC_PATH)
            time.sleep(2)
            #dlg = app.top_window()
            #dlg.print_control_identifiers()
            # ----- close existing windows
            # close main form
            if app.window(title="FDCHK Ver" + FDCHK_version).exists() is True:
                #dlg = app.top_window()
                #dlg.print_control_identifiers()
                app.window(title="FDCHK Ver" + FDCHK_version).close()
                time.sleep(3)
            # check if exist retangled confirm button , then click
            retangled_confirm_button = pyautogui.locateOnScreen("DetectImages/retangled_confirm.png")
            if retangled_confirm_button is not None:
                #dlg = app.top_window()
                #dlg.print_control_identifiers()
                pyautogui.click(retangled_confirm_button)
                time.sleep(2)
            # 2nd - close main form
            if app.window(title="FDCHK Ver" + FDCHK_version).exists() is True:
                #dlg = app.top_window()
                #dlg.print_control_identifiers()
                app.window(title="FDCHK Ver" + FDCHK_version).close()
                time.sleep(3)
            # 2nd - check if exist retangled confirm button , then click
            retangled_confirm_button = pyautogui.locateOnScreen("DetectImages/retangled_confirm.png")
            if retangled_confirm_button is not None:
                print("2nd_fdchk_confirm")
                dlg = app.top_window()
                dlg.print_control_identifiers()
                pyautogui.click(retangled_confirm_button)
                time.sleep(2)

            # move csv file to archived folder
            archive_file_full_path = ARCHIVE_DIR + "\\" + FileName
            shutil.move(file_full_path, archive_file_full_path)

            img = cv2.imread(PIC_PATH)
            # remark by user for trial run first
            # ========= rectangle FDCHK add SBL information into screen shot image =======
            # FDCHK rectangle
            # FDCHK_lot_id_startX = 542
            # FDCHK_lot_id_startY = 266
            # FDCHK_lot_id_endX = 707
            # FDCHK_lot_id_endY = 301
            # FDCHK_result_startX = 885
            # FDCHK_result_startY = 419
            # FDCHK_result_endX = 1050
            # FDCHK_result_endY = 753
            # cv2.rectangle(img, (FDCHK_lot_id_startX, FDCHK_lot_id_startY), (FDCHK_lot_id_endX, FDCHK_lot_id_endY),
            #              (0, 0, 255), 2)
            # cv2.rectangle(img, (FDCHK_result_startX, FDCHK_result_startY), (FDCHK_result_endX, FDCHK_result_endY),
            #              (0, 0, 255), 2)

            # rectangle fill white color first
            SBL_startX = 1380
            SBL_startY = 282
            SBL_endX = 1890
            SBL_endY = 837
            cv2.rectangle(img, (SBL_startX, SBL_startY), (SBL_endX, SBL_endY), (255, 255, 255), -1)
            # --------- find sbl file -> write sbl info to image


            # max dt sbl file
            sbl_file_count = len(file_list)
            if sbl_file_count >= 1:
                sbl_final_name = max(file_list)[0]
                sbl_final_name_dt = max(file_list)[1]
                sbl_path = SBL_DIR + "\\" + sbl_final_name
                sbl_file = open(sbl_path, "r")
                sbl_lines = sbl_file.readlines()
                sbl_stage_name = sbl_lines[9][:3]
                if sbl_stage_name == CUR_STAGE:
                    sbl_stage_verify = True
                else:
                    sbl_stage_verify = False
            else:
                # clean flags
                sbl_final_name = ""
                sbl_final_name_dt = ""
                sbl_path = ""
                sbl_lines = []
                sbl_stage_name = ""
                sbl_stage_verify = False

            # check if sbl file dt > lot info then operate FDCHK
            flag_SPEC_FAMILY = False  # add flag for DECISION operation
            flag_SBL_scrap_word = False  # add SBL scrap word flag for DECISION operation
            flag_SBL_class_hold = False
            if sbl_final_name_dt >= file_time2hour_string and sbl_stage_verify is True:
                # write SBL file name
                cv2.putText(img, sbl_final_name, (SBL_startX + 5, SBL_startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 0), 1)
                # -------- write SBL info
                # separate more than n=50 chars string
                sbl_line_count = 0
                sep_count = 0
                sep_n = 50
                len_sbl_lines = len(sbl_lines)
                while sbl_line_count < (len_sbl_lines + sep_count):
                    if len(sbl_lines[sbl_line_count]) >= 52:
                        # every n chars
                        r = [sbl_lines[sbl_line_count][sep_i:sep_i + sep_n] for sep_i in
                             range(0, len(sbl_lines[sbl_line_count]), sep_n)]
                        sbl_lines.pop(sbl_line_count)
                        sep_i = 0
                        while sep_i < len(r):
                            sbl_lines.insert(sbl_line_count + sep_i, r[sep_i])
                            sep_i += 1
                            sep_count += 1
                        sbl_line_count -= 1
                        sep_count -= 1
                    sbl_line_count += 1

                # write separated SBL info
                # find "COMMENT" line count & check if exist "scrap"
                sbl_line_count = 0
                COMMENT_line_no = len(sbl_lines)
                COMMENT_issue_substring = "scrap"
                sbl_info_y_i = 20
                # add SBL CLASSIFICATION : Normal/Abnormal Hold flag for DECISION operation
                for sbl_line in sbl_lines:
                    sbl_info_y_i += 20
                    sbl_line = sbl_line.replace("\n", " ")
                    # find "COMMENT" line position
                    if sbl_line[:7] == "COMMENT":
                        COMMENT_line_no = sbl_line_count
                    # after "COMMENT" line
                    if sbl_line_count >= COMMENT_line_no:
                        # if "scrap" exist in sbl line
                        if COMMENT_issue_substring in sbl_lines[sbl_line_count].lower():
                            flag_SBL_scrap_word = True
                            cv2.putText(img, sbl_line, (SBL_startX, SBL_startY + sbl_info_y_i),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                        # "scrap' not exist in this sbl line
                        else:
                            cv2.putText(img, sbl_line, (SBL_startX, SBL_startY + sbl_info_y_i),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                    # before "COMMENT" line
                    else:
                        cv2.putText(img, sbl_line, (SBL_startX, SBL_startY + sbl_info_y_i),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                        # check SBL comment for DECISION
                        if "CLASSIFICATION : Normal Hold" in sbl_line \
                                or "CLASSIFICATION : Abnormal Hold" in sbl_line:
                            flag_SBL_class_hold = True
                    sbl_line_count += 1

                # rectangle SBL-lot id
                # SBL_lot_id_startX = 1380
                # SBL_lot_id_startY = 341
                # SBL_lot_id_endX = 1548
                # SBL_lot_id_endY = 365
                # cv2.rectangle(img, (SBL_lot_id_startX, SBL_lot_id_startY), (SBL_lot_id_endX, SBL_lot_id_endY),
                #              (0, 0, 255), 2)
                # rectangle SBL-class
                # SBL_class_startX = 1380
                # SBL_class_startY = 417
                # SBL_class_endX = 1661
                # SBL_class_endY = 448
                # cv2.rectangle(img, (SBL_class_startX, SBL_class_startY), (SBL_class_endX, SBL_class_endY),
                #              (0, 0, 255), 2)
                # cv2.imwrite(PIC_PATH, img)
                # rectangle SBL-desc
                # SBL_desc_startX = 1380
                # SBL_desc_startY = 486
                # SBL_desc_endX = 1890
                # SBL_desc_endY = 510
                # cv2.rectangle(img, (SBL_desc_startX, SBL_desc_startY), (SBL_desc_endX, SBL_desc_endY),
                #              (0, 0, 255), 2)

                # ---- show special family for FDCHK DECISION
                SBL_family_startX = 1580
                SBL_family_startY = 332

                for CTL_FAMILY in df_special_control['DEVICE_GROUP']:
                    if CTL_FAMILY in FAMILY_NAME:
                        flag_SPEC_FAMILY = True  # add flag for DECISION operation
                        special_line1 = "Special Control Family !!"
                        cv2.putText(img, special_line1, (SBL_family_startX, SBL_family_startY),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        special_line2 = "This lot family : " + FAMILY_NAME
                        cv2.putText(img, special_line2, (SBL_family_startX, SBL_family_startY + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            # Not found sbl file -> write error message
            else:
                # title
                sbl_final_name = "SBL file error!! - " + CUST_LOT_ID + "-" + file_lot_id
                cv2.putText(img, sbl_final_name, (SBL_startX + 5, SBL_startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)
                # error message classification
                if sbl_file_count == 0:
                    err_msg1 = "There is no SBL file."
                elif sbl_final_name_dt < file_time2hour_string:
                    err_msg1 = "No valid SBL file time, lot info time is: " + file_time2hour_string
                elif sbl_file_count >= 1 and sbl_stage_verify is False:
                    err_msg1 = "The last SBL content-stage: " + sbl_stage_name + "; Lot info is " + CUR_STAGE
                else:
                    err_msg1 = "unknown issue."
                cv2.putText(img, err_msg1, (SBL_startX + 5, SBL_startY + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 1)
            # write changes to image
            cv2.imwrite(PIC_PATH, img)
            time.sleep(2)
            # --- DECISION operatsion
            if flag_SPEC_FAMILY is True and flag_SBL_scrap_word is False and flag_SBL_class_hold is True:
                # execute FDCHK
                app = pywinauto.Application().start(r"C:\FDCHK_EXT\fdchk_etc.exe")
                time.sleep(2)
                #dlg = app.top_window()
                # To find DECISION button
                DECISION_button = pyautogui.locateOnScreen("DetectImages/OnFocus_DECISION.png")
                # DECISION_btn_X = 830
                # DECISION_btn_Y = 254
                # DECISION_btn_X = 787 #dev loc
                # DECISION_btn_Y = 191 #dev loc
                # pywinauto.mouse.click(button='left', coords=(DECISION_btn_X, DECISION_btn_Y))
                pyautogui.click(DECISION_button)
                time.sleep(0.5)
                # dlg = app.top_window

                app.window(title="LOT DECISOIN").window(control_id=5).type_keys(CUST_LOT_ID)
                time.sleep(0.5)

                # OPTION click : Lahaina% family & only 1 test stage
                if "lahaina" in FAMILY_NAME.lower() and stage_num == 1:
                    app.window(title="LOT DECISOIN").window(title="SYSREAL").click()
                    time.sleep(0.5)
                # Judgement btn click
                app.window(title="LOT DECISOIN").window(title="Judgment").click()
                time.sleep(wait_DECISION_sec)
                # screen shot
                DECISION_PIC_PATH = \
                    PIC_DIR + "\\" + "DECISION_" + CUST_LOT_ID + "-" + file_lot_id + "-" + file_stage + ".png"
                pyautogui.screenshot(DECISION_PIC_PATH)
                time.sleep(2)
                # close form
                if app.window(title="LOT DECISOIN").exists() is True:
                    app.window(title="LOT DECISOIN").close()
                    time.sleep(2)
                    #dlg = app.top_window()
                    #dlg.print_control_identifiers()
                if app.window(title="FDCHK Ver" + FDCHK_version).exists() is True:
                    app.window(title="FDCHK Ver" + FDCHK_version).close()
                    time.sleep(3)
                    #dlg = app.top_window()
                    #dlg.print_control_identifiers()
                # 2nd close main form
                retangled_confirm_button = pyautogui.locateOnScreen("DetectImages/retangled_confirm.png")
                if retangled_confirm_button is not None:
                    print("2nd_1_decision_confirm")
                    dlg = app.top_window()
                    dlg.print_control_identifiers()
                    pyautogui.click(retangled_confirm_button)
                    time.sleep(2)
                if app.window(title="FDCHK Ver" + FDCHK_version).exists() is True:
                    app.window(title="FDCHK Ver" + FDCHK_version).close()
                    time.sleep(2)
                retangled_confirm_button = pyautogui.locateOnScreen("DetectImages/retangled_confirm.png")
                if retangled_confirm_button is not None:
                    print("2nd_2_decision_confirm")
                    dlg = app.top_window()
                    dlg.print_control_identifiers()
                    pyautogui.click(retangled_confirm_button)
                    time.sleep(2)
                # close backend form
                if app.window(title="FDCHK").exists() is True:
                    app.window(title="FDCHK").close()
                    time.sleep(2)
                retangled_confirm_button = pyautogui.locateOnScreen("DetectImages/retangled_confirm.png")
                if retangled_confirm_button is not None:
                    print("close_backend_confirm")
                    dlg = app.top_window()
                    dlg.print_control_identifiers()
                    pyautogui.click(retangled_confirm_button)
                    time.sleep(2)

    time.sleep(period_time_sec)

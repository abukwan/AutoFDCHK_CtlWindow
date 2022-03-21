from pywinauto import Application
import pywinauto
import time

app = Application().start(r"C:\FDCHK_EXT\fdchk_etc.exe")
#app = Application().connect(path=r"C:\FDCHK_EXT\fdchk_etc.exe")




app.top_window().PrintControlIdentifiers()
dlg = app.top_window()

#dlg.print_control_identifiers()

#for x in dlg.descendants():
#    print(x.window_text)
#    #print(x.class_name)
#    print(x.control_id())

#time.sleep(1)
#pywinauto.mouse.click(button='left', coords=(787, 191))
#time.sleep(1)

#dlg = app.top_window()
#dlg.print_control_identifiers()
#for x in dlg.descendants():
#    print(x.window_text)
#    #print(x.class_name)
#    print(x.control_id())


#app.window(title="LOT DECISOIN").window(control_id=5).type_keys("AA")
#time.sleep(0.5)
#app.window(title="LOT DECISOIN").window(title="SYSREAL").click()
#time.sleep(0.5)
#app.window(title="LOT DECISOIN").window(title="Judgment").click()
#time.sleep(5)
#app.window(title="LOT DECISOIN").close()


FDCHK_version = "05.53(20211208)"
#app.window(title="FDCHK Ver"+FDCHK_version).window(title="00H Data Check").click()
#app.window(title="FDCHK Ver"+FDCHK_version).window(control_id=42).type_keys("AA")

time.sleep(1)
if app.window(title="FDCHK Ver"+FDCHK_version).exists() is True:
    print("YES")
#app.window(title="FDCHK Ver"+FDCHK_version).window(title="NORMAL").click()
#app.window(title="FDCHK Ver"+FDCHK_version).close()
#app.window(title="FDCHK Ver"+FDCHK_version).child_window(control_id=33).click()
#dlg.ThunderRT6Frame3.click()
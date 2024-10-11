#####################################################################################
#  Project Taximeter v1.0                                        Date: 2022-07-17   #
#  ======================                                                           #
#                                                                                   #
#  Author: Thomas Gsell                                                             #
#  Function: Desktop App to register the work for every project like a taximeter.   #
#  Python Version: 3.10.5                                                           #
#####################################################################################
#  Published under GNU General Public License v3                                    #
#####################################################################################
#
#  1. INSTALLATION
#  ===============
#  Download Python 3.10.5 from https://www.python.org/downloads/ and install it.
#
#  2. MANUAL
#  =========
#  Buttons and Input Fields can be selected and operated with TAB and SPACE.
#
#  3. PRINCIPLES
#  =============
#  Every Information is always managed in a persistend File.
#  
#  For every project there will be a taximeter and a folder.
#  For every day there will be log-file inside the folder.
#  e.g.
#  +Proj1
#     \-20220716-Proj1.ptax
#
#  The first project on the roster is always the default project that is active
#  when no other project is active. Therefor it should be the not billed INTERN 
#  project.
#
#  4. RECOMMENDATIONS
#  ==================
#  Build categories of tasks like ..._Design, ..._Analysis, ..._Impl	 
#  
#  Register cost center in the file 00SubprojectWords2.ptax
#  
#  If a telefon call arrives, identify the project and hit the taximeter,
#  leave the previous task uncommented. After the telefon, go back to your work.
#  In putting on/off the INTERN project you can make then a mark.
#####################################################################################

import tkinter as tk
from tkinter import ttk

import os.path
import time
import datetime


#*************************************************************************************

#Works like a persistent Queue
class PersistentQueue:
    
    #the amount of lines can't be 0, only from 1..x is allowed.
    def __init__(self, fileName, amountOfLines=30):
        self.file = fileName
        self.maxEntriesAmount = amountOfLines

    #Searches the first empty line
    #Cuts all redundant line out of it and returns it. But the given list is also effected.
    #Returns the reference to the rearranged list.
    def __cropIfNeeded(self, allEntries):
        
        for i, line in enumerate(allEntries):

            if(len(line) == 0 or i>=(len(allEntries)-1)): 
                print("I reached an empty line on index: " + str(i) + ", the max entries: " + str(self.maxEntriesAmount))
                
                if(i >=(self.maxEntriesAmount-1)):
                    #Goes back from the first empty line an deletes redundant lines.
                    for j in range(i-1,self.maxEntriesAmount-2,-1):
                        if(j>=0):
                            print("I reduce: " + allEntries.pop(j))
                    
                break
        return allEntries

    
    #inserts an entry on the head of the persistent queue.
    def addEntry(self, entry):
        #print("The entry: " + entry + " shall be added. No more than " + str(self.entriesAmount) + " csv-lines.")
        
        if(len(entry) >0):
            allEntries = self.getAllEntries(True)
            
            #remove all lines the are the same as the given entry
            for i,note in enumerate(allEntries):
                if(len(note) == 0):
                    break
                if(note == entry):
                    allEntries.pop(i)
        
            cropedEntries = self.__cropIfNeeded(allEntries)
            cropedEntries.insert(0,entry)   #it works because it is the same list but croped. It's the same reference
        
            #write the whole list with the entries of the file back into the new replaced file.
            fobj = open(self.file, "w")
            for line in allEntries:
                fobj.write(line + "\n")
            fobj.close()    
    
    
    
    #Returns all entries of the persistent queue.
    #It goes until the first empty line in file.
    #If allFile is True it didn't stop at the first empty line.
    def getAllEntries(self, allFile=False):
        #print("I trie to find all entries from the file: " + self.file)
        
        file_exists = os.path.exists(self.file)
        if not os.path.exists(self.file):
            with open(self.file, 'w'): pass
        
        entries = []
        fobj = open(self.file, "r")
        for line in fobj:
            line = line.strip()
            if(len(line) == 0 and not allFile): 
                break

            entries.append(line)
        fobj.close()
        return entries
    
    #Gets the whole file, removes one single line and puts all lines back into the file.
    def removeLine(self, line):
        if(len(line) >0):
            allEntries = self.getAllEntries(True)
            
            #remove all lines the are the same as the given entry
            for i,note in enumerate(allEntries):
                if(len(note) == 0):
                    break
                if(note == line):
                    allEntries.pop(i)
                
            #write the whole list with the entries of the file back into the new replaced file.
            fobj = open(self.file, "w")
            for line in allEntries:
                fobj.write(line + "\n")
            fobj.close()    
        
        
        
    #Gets the whole file, moves one single line up and puts all lines back into the file.
    def moveLineUp(self, line):
         if(len(line) >0):
            allEntries = self.getAllEntries(True)
            
            #remove all lines the are the same as the given entry
            for i,note in enumerate(allEntries):
                if(len(note) == 0):
                    break
                if(note == line):
                    allEntries.pop(i)
                    allEntries.insert(i-1,note)
                    break
                
            #write the whole list with the entries of the file back into the new replaced file.
            fobj = open(self.file, "w")
            for line in allEntries:
                fobj.write(line + "\n")
            fobj.close()    
       
        
        
    #Gets the whole file, moves one single line down and puts all lines back into the file.
    def moveLineDown(self, line):
          if(len(line) >0):
            allEntries = self.getAllEntries(True)
            
            #remove all lines the are the same as the given entry
            for i,note in enumerate(allEntries):
                if(len(note) == 0):
                    break
                if(note == line):
                    allEntries.pop(i)
                    allEntries.insert(i+1,note)
                    break
                
            #write the whole list with the entries of the file back into the new replaced file.
            fobj = open(self.file, "w")
            for line in allEntries:
                fobj.write(line + "\n")
            fobj.close()

#*************************************************************************************

#Works like a persistent Queue
class WorkLogger:
    
    #Creates a date stamp with format: YYYYmmdd 
    def getActualDateStamp(self):
        return time.strftime("%Y%m%d")
    
    #Creates a time stamp with format: HHMM
    def getActualTimeStamp(self):
        return time.strftime("%H%M")

    #Calculates the difference between the from time and the to time in minutes.
    def calcTimeDiffMin(self, fromTimeStr, toTimeStr):
        stdFormat = "%Y%m%d %H%M"
        fromTimeObj = datetime.datetime.strptime(fromTimeStr, stdFormat)
        toTimeObj = datetime.datetime.strptime(toTimeStr, stdFormat)
        
        tdelta = toTimeObj - fromTimeObj
        tsecs = tdelta.total_seconds()
        tmins = tsecs/60
        return int(round(tmins,0))

    #Creates a from log tag with the actual time.
    def createFromTag(self, company, subproject, task, comment):
        fromDateStr = self.getActualDateStamp()
        fromTimeStr = self.getActualTimeStamp()
        toDateStr = '00000000'
        toTimeStr = '0000'
        durationMinStr = '0000'
        companyStr = company
        subprojectStr = subproject 
        taskStr = task
        commentStr = comment
        return fromDateStr + ',' + fromTimeStr + ',' + toDateStr + ',' + toTimeStr \
               + ',' + durationMinStr + ',' + companyStr + ',' + subprojectStr \
               + ',' + taskStr + ',' + commentStr
    
    #Creates the to log tag with the actual time and the time difference in minutes.
    def createToTag(self, fromTagCSV, newComment):
        toDateStr = self.getActualDateStamp()
        toTimeStr = self.getActualTimeStamp()
        
        tagElems = fromTagCSV.split(',')
        fromDateStr = tagElems[0]
        fromTimeStr = tagElems[1]
        tagElems[2] = toDateStr
        tagElems[3] = toTimeStr
        tagElems[4] = str(self.calcTimeDiffMin(fromDateStr + ' ' + fromTimeStr, toDateStr + ' ' + toTimeStr)).zfill(4)
        tagElems[8] = newComment

        toTag = tagElems[0] + ',' + tagElems[1] + ',' + tagElems[2] + ',' + tagElems[3] + ',' + tagElems[4] \
                + ',' + tagElems[5] + ',' + tagElems[6] + ',' + tagElems[7] + ',' + tagElems[8]
        return toTag
    
    #Determines whether the given log tag is a from tag. If not its a to log tag.
    def isFromTag(self, logTag):
        if(logTag.find('00000000,0000,0000,') > -1):
            return True
        else:
            return False
    
    #Gets the last line of the given file.
    def getLastLine(self, fileName):         
        file_exists = os.path.exists(fileName)
        if not os.path.exists(fileName):
            with open(fileName, 'w'): pass
    
        with open(fileName, 'r') as f:
            lines = f.readlines()
            if(len(lines) == 0):
                return ''
            else:
                return lines[-1]   
    
    #Adds a new line to the file.
    def addLineToFile(self, fileName, line=''):
        with open(fileName, 'a') as file:
            file.write(line)

    #Creates the folder and file name, no spaces are allowed within the keywords.
    def createFileName(self, company, subproject, task):
        #20220627-Takeda-Onboarding-Telko_Vorbereitung.ptax
        folder = company + '-' + subproject + '-' + task
        if not os.path.isdir(folder):
            os.makedirs(folder)
        
        filename = time.strftime("%Y%m%d") + '-' + folder + '.ptax'
        return folder + '/' + filename

    #Exchanges the last line of the file with a new line.
    def substituteLastLine(self, fileName, newLine):
        
        file_exists = os.path.exists(fileName)
        if not os.path.exists(fileName):
            with open(fileName, 'w'): pass
        
        loglines = []
        with open(fileName, "r") as fobj:
            for line in fobj:
                line = line.strip()
                loglines.append(line)

            #loglines[-1] = newLine + '\n'
            loglines[-1] = newLine
        	
        with open(fileName, "w") as fobj:
            #fobj.seek[0]
            for line in loglines:
                fobj.write(line + '\n')
            fobj.truncate()

    #Main function of the class. Logs a project work incident.
    def logProjectWork(self, startWork=True, company='INTERN', subproject='', task='', workComment='Not Billable'):
        
        fileName = self.createFileName(company, subproject, task)
        line = self.getLastLine(fileName)
        if(self.isFromTag(line)):
            print("the last line is a from tag.")
            if startWork:
               print("but the work is starting, I'll do a new from tag.")
               fromTag = self.createFromTag(company, subproject, task, workComment)
               self.addLineToFile(fileName, '\n' + fromTag) #put a carridge return before a new from tag after another from tag 
            else:
                print("so the work is stopping, I'll form a to tag out of it.")
                toTag = self.createToTag(line, workComment)
                self.substituteLastLine(fileName, toTag)
        else:
            print("the last line is a to tag.")
            if startWork:
                print("so the work is starting, I'll fill in a new from tag.")
                fromTag = self.createFromTag(company, subproject, task, workComment)
                self.addLineToFile(fileName, fromTag)    
            else:
                print("but the work is stopping, I'll do nothing.")

#*************************************************************************************


class AnnotationDlg(tk.Toplevel):

    def __init__(self, master, bannerToStart):
        tk.Toplevel.__init__(self, master)
        
        self.geometry('800x440+300+200')
        self.resizable(width=False, height=False)
        self.title('Suspend Work')
        self.workLogger = WorkLogger()
        self.queue = PersistentQueue("00Annotations.ptax")
        self.projectName = master.title()
        self.projectManager = master.projectManagerDlg
        self.bannerToStart = bannerToStart
        self.bannerToStop = master
        self.protocol("WM_DELETE_WINDOW", self.winClose)
        self.configure(bg='yellow')

        self.label = ttk.Label(self)
        self.label["text"] = "What have I done?"
        self.label.pack()
        self.label.place(height=20, width=100, x=100, y=200)
        self.label["background"] = "#FFFF00"
        self.label["foreground"] = "#EE0000"
        
        self.projLb = ttk.Label(self)
        self.projLb["text"] = self.projectName
        self.projLb.pack()
        self.projLb["background"] = "#FFFF00"
        self.projLb.place(height=20, width=300, x=200, y=200)        
        
        self.createBtn = tk.Button(self)
        self.createBtn["text"] = "Suspend Work"
        self.createBtn["command"] = self.createBtnClicked
        self.createBtn.pack()
        self.createBtn.place(height=20, width=100, x=600, y=200)   
        
        current_var = tk.StringVar()
        self.taskCb = ttk.Combobox(self, textvariable=current_var)
        self.taskCb['values'] = self.queue.getAllEntries()
        self.taskCb['state'] = 'normal'
        self.taskCb.pack()
        self.taskCb.place(height=20, width=600, x=100, y=220)
    
    def createBtnClicked(self):
        #get the work comment
        entry = self.taskCb.get()
        self.queue.addEntry(entry)
        #stop the running banner
        titelElements = self.projectName.split(',')
        self.workLogger.logProjectWork(False, titelElements[0], titelElements[1], titelElements[2], entry)
        self.bannerToStop.lampLb["background"] = "#EE0000"  #set background to red
        
        #start the new banner
        titelElements = self.bannerToStart.title().split(',')
        self.workLogger.logProjectWork(True, titelElements[0], titelElements[1], titelElements[2])
        self.bannerToStart.lampLb["background"] = "#00EE00"   #set background to green
        self.projectManager.setActiveProjectBanner(self.bannerToStart.title())
        
        #back to normal
        self.projectManager.enableAllProjectBanner()
        self.destroy()
    
    #called if the window shall be closed
    def winClose(self):
        print("The annotation window shall be closed.")
        self.createBtnClicked()

#*************************************************************************************


class NewProjectDlg(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.geometry('500x60+100+600')
        self.resizable(width=False, height=False)
        self.title('New Project')
        self.projectManager = master
        self.key1Queue = PersistentQueue("00CompanyWords1.ptax", 20) #max of open project work is 20.
        self.key2Queue = PersistentQueue("00SubprojectWords2.ptax", 20) #max of open project work is 20.
        self.key3Queue = PersistentQueue("00TaskWords3.ptax", 20) #max of open project work is 20.

        self.companyLb = ttk.Label(self)
        self.companyLb["text"] = "Company:"
        self.companyLb.pack()
        self.companyLb.place(height=20, width=80, relx=0.0, y=0)

        self.subprojLb = ttk.Label(self)
        self.subprojLb["text"] = "Subproject:"
        self.subprojLb.pack()
        self.subprojLb.place(height=20, width=80, relx=0.33, y=0)

        self.taskLb = ttk.Label(self)
        self.taskLb["text"] = "Task:"
        self.taskLb.pack()
        self.taskLb.place(height=20, width=80, relx=0.66, y=0)

        current_var = tk.StringVar()
        self.companyCb = ttk.Combobox(self, textvariable=current_var)
        self.companyCb['values'] = self.key1Queue.getAllEntries()
        self.companyCb['state'] = 'normal'
        self.companyCb.pack()
        self.companyCb.place(height=20, width=165, relx=0.0, y=20)

        current_var = tk.StringVar()
        self.subprojCb = ttk.Combobox(self, textvariable=current_var)
        self.subprojCb['values'] = self.key2Queue.getAllEntries()
        self.subprojCb['state'] = 'normal'
        self.subprojCb.pack()
        self.subprojCb.place(height=20, width=165, relx=0.33, y=20)

        current_var = tk.StringVar()
        self.taskCb = ttk.Combobox(self, textvariable=current_var)
        self.taskCb['values'] = self.key3Queue.getAllEntries()
        self.taskCb['state'] = 'normal'
        self.taskCb.pack()
        self.taskCb.place(height=20, width=165, relx=0.66, y=20)

        self.createBtn = tk.Button(self)
        self.createBtn["text"] = "Create"
        self.createBtn["command"] = self.createBtnClicked
        self.createBtn.pack()
        self.createBtn.place(height=20, width=40, x=0, y=40)
        
        self.projectManager.disableAllButtons()
        

    def createBtnClicked(self):
        print("create Button clicked.")
        company = self.companyCb.get()
        subproj = self.subprojCb.get()
        task = self.taskCb.get()
        entry = company + ',' + subproj + ',' + task
        
        self.key1Queue.addEntry(company)
        self.key2Queue.addEntry(subproj)
        self.key3Queue.addEntry(task)
        self.projectManager.addProj(entry)
        
        self.projectManager.enableAllButtons()
        self.projectManager.refreshSelectorBox()
        
        self.destroy()

#*************************************************************************************


class ProjectBannerDlg(tk.Toplevel):

    def __init__(self, master, titleContent, srcPosy):
        tk.Toplevel.__init__(self, master)
        
        #self.wm_attributes("-topmost", 1)
        self.attributes("-topmost", True)
        self.update()
        self.overrideredirect(1)
        self.projectManagerDlg = master
        self.workLogger = WorkLogger()
        
        maxWidth = self.winfo_screenwidth()
        bannerWidth = len(titleContent)*7 + 40
        srcPosx = maxWidth - bannerWidth
        
        print("my screen max width is: " + str(maxWidth) + ", my srcPos x is: " + str(srcPosx) + ", my y pos is: " + str(srcPosy))

        #self.geometry(str(bannerWidth) + 'x40')
        self.geometry(str(bannerWidth) + 'x40+' + str(srcPosx) + '+' + str(srcPosy))
        
        #self.geometry(str(bannerWidth) + 'x40')
        #self.eval('tk::PlaceWindow . center')
        #self.geometry('+' + str(srcPosx) + '+' + str(srcPosy))
        #self.update()
        
        self.title(titleContent)
        self.resizable(width=False, height=False)

        self.titelLb = ttk.Label(self)
        self.titelLb["text"] = titleContent
        self.titelLb.pack()
        self.titelLb.place(height=20, relwidth=1.0, x=0, y=0)
        
        self.startBtn = tk.Button(self, anchor='w')
        self.startBtn["text"] = "Start"
        self.startBtn["command"] = self.__startBtnClicked
        self.startBtn.pack()
        self.startBtn.place(height=20, width=40, x=0, y=20)
 
        self.lampLb = ttk.Label(self)
        
        self.lampLb["background"] = "#EE0000"
        self.lampLb.pack()
        self.lampLb.place(height=20, relwidth=1.0, x=41, y=20)

        
    
    def getName(self):
        return self.title()
    
    def disableButton(self):
        self.startBtn['state'] = "disabled"
        
    def enableButton(self):    
        self.startBtn['state'] = "normal"
    
    def __startBtnClicked(self):
        self.startActivity()
        
    def startActivity(self):
        activeBanner = self.projectManagerDlg.getActiveProjectBanner()
        if activeBanner:
            #There is an active banner so stop it first, the start this one.
            if activeBanner.getName() != self.getName():
                print("I try to stop working on: " + activeBanner.getName())
                activeBanner.stopActivity(self)
            else:
                #There isn't an active banner so start this one directly.
                titelElements = self.title().split(',')
                self.workLogger.logProjectWork(True, titelElements[0], titelElements[1], titelElements[2])
        
                self.lampLb["background"] = "#00EE00"   #set background to green
                self.projectManagerDlg.setActiveProjectBanner(self.title())
        
        
    def stopActivity(self, bannerToStart=None):
        #call Annotation Dialog, the annotation dialog has to log the project
        if bannerToStart == None:
            #Just end the project work
            titelElements = self.title().split(',')
            self.workLogger.logProjectWork(False, titelElements[0], titelElements[1], titelElements[2], "App has interrupted the project work. Maybe roster was refreshed.")
            self.lampLb["background"] = "#EE0000"  #set background to red
        else:
            #normal path
            self.projectManagerDlg.disableAllProjectBanner()
            AnnotationDlg(self, bannerToStart)


#*************************************************************************************


class ProjectManagerDlg(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        
        self.geometry('300x120+200+200')
        self.resizable(width=False, height=False)
        self.title('ProjectTaximeter v1.0')
        self.__projectBanners = {}
        self.__activeProj = ""
        self.__pq = PersistentQueue("00OpenProjects.ptax", 15) #max of open project work is 15.
        self.protocol("WM_DELETE_WINDOW", self.winClose)
        self.master = master
        self.worklogger = WorkLogger()
        
        self.addBtn = tk.Button(self)
        self.addBtn["text"] = "Add"
        self.addBtn["command"] = self.addBtnClicked
        self.addBtn.pack()
        self.addBtn.place(height=20, width=50, x=0, y=0)
        
        self.removeSelBtn = tk.Button(self)
        self.removeSelBtn["text"] = "Remove Selected"
        self.removeSelBtn["command"] = self.removeSelBtnClicked
        self.removeSelBtn.pack()
        self.removeSelBtn.place(height=20, width=100, x=50, y=0)        
        
        self.moveUpBtn = tk.Button(self)
        self.moveUpBtn["text"] = "\u02C4"
        self.moveUpBtn["command"] = self.moveUpBtnClicked
        self.moveUpBtn.pack()
        self.moveUpBtn.place(height=20, width=20, x=170, y=0)
        
        self.moveDownBtn = tk.Button(self)
        self.moveDownBtn["text"] = "\u02C5"
        self.moveDownBtn["command"] = self.moveDownBtnClicked
        self.moveDownBtn.pack()
        self.moveDownBtn.place(height=20, width=20, x=190, y=0)
        
        self.refreshBtn = tk.Button(self)
        self.refreshBtn["text"] = "Refresh Roster"
        self.refreshBtn["command"] = self.refreshBtnClicked
        self.refreshBtn.pack()
        self.refreshBtn.place(height=20, width=90, x=210, y=0)
                
        self.projSelectorLBox = tk.Listbox(self) 
        self.projSelectorLBox["selectmode"] = "browse"
        self.vrtScrollbar = tk.Scrollbar(self.projSelectorLBox, orient=tk.VERTICAL)
        self.projSelectorLBox.config(yscrollcommand = self.vrtScrollbar.set)
        self.projSelectorLBox.pack()
        self.projSelectorLBox.place(height=100, relwidth=1.0, x=0, y=20)
        
        self.vrtScrollbar.config(command = self.projSelectorLBox.yview)        
        self.vrtScrollbar.place(relx=0.95, rely=0.0, relheight=1.0)        
        
        self.loadProjectNames()

    #called if the window shall be closed
    def winClose(self):
        #stop active Projectwork without annotation
        activeBanner = self.getActiveProjectBanner()
        titelElements = activeBanner.getName().split(',')
        self.worklogger.logProjectWork(False, titelElements[0], titelElements[1], titelElements[2], "No annotation because App was closed by user.")
        self.master.destroy()

    #Opens the file with the project names and load them into the project selector box.
    def loadProjectNames(self):
        #stop activity of the active banner if it is present
        if len(self.__activeProj) >0:
            print("I have to stop the active Proj: " + self.__activeProj)
            self.__projectBanners[self.__activeProj].stopActivity()
        #delete all entries in the selector box
        self.projSelectorLBox.delete(0,'end')
        #delete all banners
        for banner in self.__projectBanners.values():
            banner.destroy()
        self.__projectBanners.clear()
        
        projNames = self.__pq.getAllEntries()       
        yIndex = 1
        for csvName in projNames:
            self.__projectBanners[csvName] = ProjectBannerDlg(self, csvName, yIndex*40)
            self.projSelectorLBox.insert("end",csvName)
            yIndex = yIndex + 1
        
        if len(self.__projectBanners) > 0:
            self.__activeProj = list(self.__projectBanners.keys())[0]
            #print("the active project is: " + self.__activeProj)
            self.__projectBanners[self.__activeProj].startActivity()
    
    #Loads the project names into the selector box but won't change the project roster. 
    def refreshSelectorBox(self):
        projNames = self.__pq.getAllEntries()
        self.projSelectorLBox.delete(0,'end')
        for csvName in projNames:
            self.projSelectorLBox.insert("end",csvName)
    
    
    def disableAllButtons(self):
        self.addBtn['state'] = "disabled"
        self.removeSelBtn['state'] = "disabled"
        self.moveUpBtn['state'] = "disabled"
        self.moveDownBtn['state'] = "disabled"
        self.refreshBtn['state'] = "disabled"  #isn't functional
    
    def enableAllButtons(self):
        self.addBtn['state'] = "normal"
        self.removeSelBtn['state'] = "normal"
        self.moveUpBtn['state'] = "normal"
        self.moveDownBtn['state'] = "normal"
        self.refreshBtn['state'] = "normal"    #isn't functional
    
    #def createProjectBanner(self):
    def disableAllProjectBanner(self):
        for banner in self.__projectBanners.values():
            banner.disableButton()
    
    def enableAllProjectBanner(self):
        for banner in self.__projectBanners.values():
            banner.enableButton()
    
    
    def getActiveProjectBanner(self):
        return self.__projectBanners[self.__activeProj]
        
    def setActiveProjectBanner(self, projName):
        if projName in self.__projectBanners:
            self.__activeProj = projName
            print(projName + " is now active.")
        else:
            print("Error: " + projName + " is unknown.")

    def addProj(self, projName):
        self.__pq.addEntry(projName)


    def addBtnClicked(self):
        print("add button clicked.")
        newProjDlg = NewProjectDlg(self)
        
    
    def removeSelBtnClicked(self):
        print("remove selection button clicked.")
        for selection in self.projSelectorLBox.curselection():
            selectedLine = self.projSelectorLBox.get(selection)
            print("I have to remove: " + selectedLine)
            self.__pq.removeLine(selectedLine)
        self.refreshSelectorBox()
        
    
    def moveUpBtnClicked(self):
        print("move selection up button clicked.")
        for selection in self.projSelectorLBox.curselection():
            selectedLine = self.projSelectorLBox.get(selection)
            print("I have to move up: " + selectedLine)
            self.__pq.moveLineUp(selectedLine)
            self.refreshSelectorBox()
            self.projSelectorLBox.selection_set(selection-1)
        
    
    def moveDownBtnClicked(self):
        print("move selection down button clicked.")
        for selection in self.projSelectorLBox.curselection():
            selectedLine = self.projSelectorLBox.get(selection)
            print("I have to move down: " + selectedLine)
            self.__pq.moveLineDown(selectedLine)
            self.refreshSelectorBox()
            self.projSelectorLBox.selection_set(selection+1)
    
    
    def refreshBtnClicked(self):
        print("refresh roster button clicked.")
        self.loadProjectNames()

#*************************************************************************************


root = tk.Tk()
root.withdraw()
projMan = ProjectManagerDlg(root)
root.mainloop()
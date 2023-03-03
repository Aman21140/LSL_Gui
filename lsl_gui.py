from pylsl import StreamInlet, resolve_stream
from tkinter import*
from tkinter import filedialog
from tkinter import font
import time
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

#Global variable
state = False
data = np.array([])
timeStamp = []
sample_ = []
t = time.ctime()

#functions
def Main():
    global state,data,timeStamp,sample_
    if(state == True):
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)

        if(len(data) < 100):
            data = np.append(data,float(sample[0]))
        else:
            data[0:99] = data[1:100]
            data[99] = float(sample[0])
        
        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)
        canvas.draw()

        timeStamp.append(str(timestamp))
        sample_.append(str(sample))
    root.after(1,Main)
    
def Stop_Acquisition():
    global state
    state = False

def Start_Acquisition():
    global state
    state = True

def Reset_Graph():
    global data,timeStamp,sample_,t
    t = time.ctime()
    timeStamp.clear()
    sample_.clear()
    data = np.array([])
    lines.set_xdata(np.arange(0,len(data)))
    lines.set_ydata(data)
    canvas.draw()

def Save_As_File():
    global t,sample_,timeStamp
    text_file = filedialog.asksaveasfilename(defaultextension=".*" , initialdir="D:/",title="Save File", filetypes = (("CSV File","*.csv"),("Text File","*.txt"),("All Files","*.*")))
    meta_data = text_file[:len(text_file)-4]+'_metaData.txt'
    text_file = text_file[:len(text_file)-4]+'_Data'+text_file[len(text_file)-4:]
    if text_file:
        text_file = open(text_file,'w')
        text_file.write("Time stamp, ")
        for i in range(sample_[0].count(', ')+1):
            text_file.write("Channel-"+str(i+1)+',')
        text_file.write("\n")
        for i in range(len(timeStamp)):
            text_file.write(timeStamp[i])
            text_file.write(", ")
            # text_file.write(b[i])
            for j in range(len(sample_[i])):
                if(j == 0):
                    text_file.write(sample_[i][j][1:])
                elif(j == len(sample_[i])-1):
                    text_file.write(sample_[i][j][1:])
                else:
                    text_file.write(sample_[i][j])
            text_file.write("\n")
        meta = open(meta_data,'w')
        il = inlet.info()
        meta.write("Session Information:-\n")
        meta.write("\nDate: "+t[8:10]+" "+t[4:7]+" "+t[20:])
        meta.write("\nSession Start Time: "+t[11:16],)
        meta.write("\nTime of Log: "+time.ctime()[11:16],)
        meta.write("\nName: "+info.name())
        meta.write("\nType: "+info.type())
        meta.write("\nSample Rate: "+str(info.nominal_srate()))
        meta.write("\nChannel Count: "+str(info.channel_count()))
        meta.write("\nSource Id: "+str(info.source_id()))
        text_file.close()
        meta.close()

#Main GUI
root = Tk()
root.geometry("800x600")
root.title("lsl")
root.configure(background= 'light blue')
# plot
fig = Figure();
ax = fig.add_subplot(111)
# ax.set_facecolor('green')

ax.set_title('LSL Data');
ax.set_xlabel('Sample')
ax.set_ylabel('')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,4)
lines = ax.plot([],[])[0]
# lines.set_color("black")

canvas = FigureCanvasTkAgg(fig, master=root )  # A tk.DrawingArea.
canvas.get_tk_widget().place(x = 175,y = 3, width = 650,height = 500)
canvas.draw()

#Widgets
start_Button = Button(root,text="Start",command=Start_Acquisition , width=10 , pady = 2)
start_Button.place(x = 5 , y = 5)
stop_Button = Button(root,text="Stop",command=Stop_Acquisition, width=10,pady=2)
stop_Button.place(x = 88 , y = 5)
log_Button = Button(root,text="Log",command=Save_As_File, width = 10,pady = 2)
log_Button.place(x = 5 , y = 35)
reset_Button = Button(root,text="Reset",command=Reset_Graph , width=10 , pady=2)
reset_Button.place(x = 88 , y = 35)

#data acquisition 
if __name__ == '__main__':
    print("looking for a stream...")
    streams = resolve_stream('type')
    inlet = StreamInlet(streams[0])
#meta data
    info = inlet.info()
    name = Label(root,text="Name: "+ str(info.name()), font=('calibre',10))
    name.place( x = 180 , y = 510)
    type = Label(root,text="Type: "+ str(info.type()), font=('calibre',10))
    type.place( x = 340 , y = 510)
    sample_Rate = Label(root,text="Sample rate: "+ str(info.nominal_srate()), font=('calibre',10))
    sample_Rate.place( x = 180 , y = 540)
    channel_Count = Label(root,text="Channel count: "+ str(info.channel_count()), font=('calibre',10))
    channel_Count.place( x = 340 , y = 540)
    source_Id = Label(root,text="Source Id: "+ str(info.source_id()), font=('calibre',10))
    source_Id.place( x = 500 , y = 510)
    time_ = Label(root,text="Session start time: "+ str(t[11:16]), font=('calibre',10))
    time_.place( x = 500 , y = 540)

    root.after(1,Main)
root.mainloop()

import csv
from tabulate import tabulate
import tkFileDialog
from Tkinter import *
import sys

def read_data(file_name):
    result = list()
    with open(file_name, 'r') as file_reader:
        for line in file_reader:
            order_set = set(line.strip().split(','))
            result.append(order_set)
    return result


def support_count(orders, item_set):
    count = 0
    for order in orders:
        if item_set.issubset(order):
            count += 1
        else:
            pass
    return count


def support_frequency(orders, item_set):
    N = len(orders)
    return support_count(orders, item_set)/float(N)


def confidence(orders, left, right):
    left_count = support_count(orders, left)
    right = right.union(left)
    right_count = support_count(orders, right)
    result = right_count/left_count
    return result


def apriori(orders, support_threshold, confidence_threshold):
    candidate_items = set()

    for items in orders:
        candidate_items = candidate_items.union(items)
   
    def apriori_next(item_set=set()):
        result = []
        
        if len(item_set) == len(candidate_items):
            return result

        elif not item_set:  
            for item in candidate_items:
                item_set = {item}
                if support_frequency(orders, item_set) >= support_threshold:
                    result.extend(apriori_next(item_set))
                else:
                    pass
        else: 
            for item in candidate_items.difference(item_set):
                if support_frequency(orders, item_set.union({item})) >=support_threshold:
                	if confidence(orders, item_set, {item}) >=confidence_threshold:
                		result.append((item_set, item))
                		result.extend(apriori_next(item_set.union({item})))
                	else:
                		pass
                else:
                	pass

        return [rule for rule in result if rule]

    return apriori_next()

def button_go_callback():
	confidence_threshold = float(entry_confidence.get())
	support_threshold = float(entry_support.get())
	
	input_file = entry_filename.get()
	text.delete(1.0,END)
	statusText.set("Rules Generated Successfully")
	data = read_data(input_file)
	final_results = ["{} => {}  \t|\t Support = {:0.2f}, Confidence = {:0.2f}".format(item_set, item, support_frequency(data[1:], item_set.union({item})),
		confidence(data[1:], item_set, {item})) for item_set, item in apriori(data[1:], support_threshold, confidence_threshold)]
	for result in final_results:
		text.insert(INSERT, str(result)[3:-2])
		text.insert(INSERT, "\n\n")
		

def button_browse_callback():
	filename = tkFileDialog.askopenfilename()
	entry_filename.delete(0, END)
	entry_filename.insert(0, filename)

def button_viewinput_callback():
	input_file = entry_filename.get()
	text.delete(1.0,END)
	with open(input_file, 'r') as file_reader:
		for line in file_reader:
			text.insert(INSERT, line )
			text.insert(INSERT,"\n")
	statusText.set(" Transactions Displayed Successfully")
	
root = Tk()
frame = Frame(root)
frame.pack()

statusText = StringVar(root)
statusText.set("Click Browse and select file, then select Confidence and Support Thresholds, " "\nClick on View Input to view Input Transactions or Click on Go")

top_frame=Frame(frame)

label = Label(top_frame, text="CSV file: ", padx=5, pady=2)
label.pack(side=LEFT)
entry_filename = Entry(top_frame,bd=5, width=100)
entry_filename.pack(side=LEFT)
La = Label(top_frame, padx=3, pady=5, text=" ")
La.pack(side=LEFT)
button_browse = Button(top_frame, text="Browse", command=button_browse_callback)
button_browse.pack(side=RIGHT)

top_frame.pack()
separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

mid_frame=Frame(frame)

L1 = Label(mid_frame, padx=5, pady=5, text="Confidence Threshold :")
entry_confidence = Spinbox(mid_frame,width=5, from_=0.1, to=1, format="%.2f" , increment=0.05, bd=5 )
L1.pack(side=LEFT)
entry_confidence.pack(side=LEFT)

L2 = Label(mid_frame,padx=5, pady=5, text="Support Threshold :")
entry_support = Spinbox(mid_frame,width=5, from_=0.1, to=1, format="%.2f" , increment=0.05, bd=5 )
L2.pack(side=LEFT)
entry_support.pack(side=LEFT)

Lb = Label(mid_frame, padx=10, pady=5, text=" ")
Lb.pack(side=LEFT)


button_viewinput = Button(mid_frame, text="View Input", command=button_viewinput_callback)
button_viewinput.pack(side=LEFT)

La = Label(mid_frame, padx=5, pady=5, text=" ")
La.pack(side=LEFT)

button_go = Button(mid_frame, text="Go", command=button_go_callback)
button_go.pack(side=RIGHT)
mid_frame.pack()
separator = Frame(mid_frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

txt_frm = Frame(frame, width=600, height=600)
txt_frm.pack(fill="both", expand=True)
txt_frm.grid_propagate(False)
txt_frm.grid_rowconfigure(0, weight=1)
txt_frm.grid_columnconfigure(0, weight=1)
text = Text(txt_frm, borderwidth=3)
text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
scrollb = Scrollbar(txt_frm, command=text.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
text['yscrollcommand'] = scrollb.set
text.pack()

separator = Frame(frame, height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

message = Label(frame, textvariable=statusText)
message.pack()

mainloop()

if __name__ == '__main__':
    button_go_callback()
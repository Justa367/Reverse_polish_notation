import tkinter as tk

#Global variables
symbols=["7", "8", "9", "C", "\u21BA","4", "5", "6", "*", "/", "1", "2", "3", "+",  "-", "0", "Space"] #Columnspan is 5 
data_font=("Papyrus", 11) #Font settings 


#Main window settings
def windowSet():
    root=tk.Tk()
    root.geometry("600x350")
    root.title("Reverse Polish Notation Solver")
    root.configure(bg="light gray")
    return root


#Screen settings, labels that show prev equation
def screenSet(root):
    screen=[tk.Label(root, width=65, bg="#C0CBCB", anchor="w", borderwidth=2) for i in range(2)]
    for i in range(len(screen)):
        screen[i].grid(row=i, columnspan=5, ipadx=1, ipady=20) #ipadx and ipady are margins
        screen[i].configure(font=data_font)
    return screen

#User entry settings
def dataField(root, screen):
    data_field=tk.Entry(root, borderwidth=0, highlightcolor="white", highlightbackground="white") #Basiclly deleting border coz its looks ugly
    data_field.grid(row=len(screen), columnspan=5, ipadx=180, ipady=8)
    data_field.configure(font=data_font)
    return data_field

#What will happends if u press some buttons?
def onPressBtn(data_field, symbol):
    def f():
        #Clear lestest sign in users enrty
        if symbol=="\u21BA":
            bufor=data_field.get()[:-1]
            data_field.delete(0, tk.END)
            data_field.insert(tk.END, bufor)
        #Clear everything in user entry
        elif symbol=="C":
            data_field.delete(0, tk.END)
        #Add spacing if space btn is pressed
        elif symbol=="Space":
            data_field.insert(tk.END, " ")
        #Write what is on pressed btn
        else:
            data_field.insert(tk.END, symbol)
    return f

#Maybe not the right sovling system, but it moves prev user entry up, shows results and warnings 
def solve(data_field, screen):
    def f():
        txt=data_field.get() #Getting what user has written
        result=onp(txt) #Getting RPN result -> False or Num 
        for i in range(1, len(screen)):
            #Moving prev up and down
            if screen[i]["text"]:
                screen[i-1]["text"]=screen[i]["text"]
        #Checking the results from RPN function
        if result==False:
            screen[-1]["text"]=f" '{txt}' is an invalid expression!"
        else:
            screen[-1]["text"]=f"{txt}  =  {result}"
    return f

#Buttons confing
def btnSet(root, screen, data_field):
    #Creating a list of btns with txt(given in list called symbols)
    btn_list=[tk.Button(root, text=symbol, borderwidth=0, bg="light gray") for symbol in symbols]
    j=len(screen)+1 #New var for rows
    for i in range(len(btn_list)):
        if i%5==0:
            j+=1
        margin=20 if len(symbols[i])==1 else 5 #Coz size czn be slightly bigger
        btn_list[i].grid(row=j, column=i%5, ipadx=margin, ipady=8) #Main btn setting 
        btn_list[i].configure(font=data_font)
        btn_list[i].configure(command=onPressBtn(data_field, btn_list[i]["text"])) #Calling the showing function

    #Equal sign settings coz it's special btn 
    equal_sign=tk.Button(root, text="=", bg="green", borderwidth=0, command=solve(data_field, screen))
    equal_sign.configure(font=data_font)
    equal_sign.grid(row=len(screen)+5, column=3, columnspan=2, ipadx=60, ipady=5)

    return btn_list, equal_sign

#Right solving system, implementing the stack alorythm
def onp(operation):
    list1=operation.split(' ') #list1=[x for x in operation] for x in list1: if ord(x)==10: list1.remove(x)
    stack=[]
    dig=0
    signs=0
    new_x=0
    for x in list1:
        if x.isdigit()==True:
            stack.append(int(x))
            dig+=1
        else:
            if len(stack)>=2:
                if x=="-":
                    new_x=stack[len(stack)-2]-stack[len(stack)-1]
                elif x=="+":
                    new_x=stack[len(stack)-2]+stack[len(stack)-1]
                elif x=="*":
                    new_x=stack[len(stack)-2]*stack[len(stack)-1]
                elif x=="/":
                    if stack[len(stack)-1]==0:
                        return False
                    else:
                        new_x=stack[len(stack)-2]/stack[len(stack)-1]
                else:
                    return False

                stack.pop()
                stack.pop()
                stack.append(new_x)
                signs+=1
            else:
                return False
    if dig-signs==1:
        return max(stack)
    else:
        return False

#Main function that gathers everything 
def main():
    root=windowSet()
    screen=screenSet(root)
    data_field=dataField(root,screen)
    btns=btnSet(root, screen, data_field)
    root.mainloop()

#Calling the main function, just a tasteful structure
if __name__=="__main__":
    main()
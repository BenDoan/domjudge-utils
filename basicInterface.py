import sys
import requests
import random

passchars = map(chr,range(ord('a'),ord('z')+1) + range(ord('A'),ord('Z')+1) + range(ord('0'),ord('9')+1) )

class User():
    def __init__(self,name,username,bracket):
        self.name = name
        self.username = username
        self.bracket = bracket
        self.password = self.gen_password(8)
    def gen_password(self,length):
        return "".join([random.choice(passchars) for i in range(length)])
    def to_csv(self):
        return "{},{},{},{}\n".format(self.name,self.username,self.bracket,self.password)
    def to_printable(self):
        return self.to_readable(32)
    def to_readable(self,width):
        return (
"""{: ^{width}}
{: ^{width}}
{: ^{width}}""").format(
            "{} <{}>".format(self.name,self.bracket),
            "username: {}".format(self.username),
            "password: {}".format(self.password),width=width)
    def to_comm(self,token):
        return {"name":self.name,"username":self.username,"password":self.password,"token":token,"bracket":self.bracket}
    def to_verify(self):
        return (
"""NAME :     {}
USERNAME : {}
BRACKET :  {}""").format(self.name,self.username,self.bracket)

def read_name(userin,userout):
    userout.write("WHAT... is your name? ")
    name = userin.readline().strip()
    if name == "" :
        userout.write("HEY!, you must have some sort of name.\n")
        return read_name(userin,userout)
    return name

def read_username(userin,userout):
    userout.write("WHAT... is your preferred username? ")
    username = userin.readline().strip()
    if username == "" :
        userout.write("Nothing is an unacceptable username\n")
        return read_username(userin,userout)
    return username

def read_bracket(userin,userout):
    userout.write("WHAT... is your bracket? [1400/1620/open] ")
    bracket = userin.readline().strip().lower()
    if bracket not in ["1400","1620","open"] :
        userout.write("Your bracket must be one of 1400, 1620, or open\n")
        return read_bracket(userin,userout)
    return bracket

def verify(user,userin,userout,first=True):
    if first :
        userout.write("\n{}\ndoes this look correct? [y/N] ".format(user.to_verify()))
    else :
        userout.write("\n{}\nis everything correct now? [y/N] ".format(user.to_verify()))
    if userin.readline().strip().lower().startswith("y"):
        return user
    thingmap = {"The name":("name",read_name),"The username":("username",read_username),"The bracket":("bracket",read_bracket)}
    thinglist = [ x for x in thingmap ]
    for x in range(len(thinglist)) :
        userout.write("{}) {}\n".format(x+1,thinglist[x]))
    val = len(thinglist)+1
    userout.write("{}) Nevermind, nothing was wrong.\n".format(val))
    num = numchoose(val,userin,userout)
    if num == val :
        userout.write("Okay.\n")
        return user
    tup = thingmap[thinglist[num-1]]
    user.__dict__[tup[0]] = tup[1](userin,userout)
    return verify(user,userin,userout,False)


def numchoose(maxnum,userin,userout):
    userout.write("choose the number of what was incorrect: ")
    inval = 0
    try :
        inval = int(userin.readline().strip())
    except ValueError :
        userout.write("hey, that was not an integer!\n")
        return numchoose(maxnum,userin,userout)
    if inval > maxnum or inval < 1 :
        userout.write("that was not a valid choice\n")
        return numchoose(maxnum,userin,userout)
    return inval

def finalize(user,userin,userout,url,token) :
    user = verify(user,userin,userout)
    result = requests.post(url,data=user.to_comm(token))
    if result.text != "Success" :
        if "Duplicate" in result.text:
            userout.write("someone already has that username, please choose a different one.\n")
            user.username = read_username(userin,userout)
        else :
            userout.write("the server did not like your data, here is what it said:\n{}".format(result.text))
        return finalize(user,userin,userout,url,token)
    return user

def interface(userin,userout,printout,logout,url,token):
    while True :
        userout.write("STOP! who would enter the contest must answer me these questions three, ere contest site he see.\n")
        name = read_name(userin,userout)
        username = read_username(userin,userout)
        bracket = read_bracket(userin,userout)
        user = User(name,username,bracket)

        user = finalize(user,userin,userout,url,token)
        printout.write(user.to_printable())
        printout.write("\n\n\n\n")
        logout.write(user.to_csv())


interface(sys.stdin,sys.stdout,sys.stdout,open("interface.log","wa"),"http://bdo.pw:5000/user/add","acmsecret")



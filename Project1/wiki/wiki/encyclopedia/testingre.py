import re

def reading(content):
    h=0
    hh=False
    read=()
    for i in content:
        if i =='#':
            h+=1
        if i !='#' and h>0 and hh==False:
            read.append(f"<h{h}>")
            hh=True
        if i == '\n' and hh==True:
            read.append(f"</h{h}>")
            hh=False
            h=0
        if i == '\n':
            read.append('<br>')
        read.append(i)
    print(read)
    return read

def read(content):
    content=content.replace("###### ", "<h6>")
    content=content.replace("##### ", "<h5>")
    content=content.replace("#### ", "<h4>")
    content=content.replace("### ", "<h3>")
    content=content.replace("## ", "<h2>")
    content=content.replace("# ", "<h1>")
    x=0
    while x <10:
        content=content.replace("* *", "<i>",1)
        content=content.replace("* *", "</i>",1)
        content=content.replace("**", "<b>",1)
        content=content.replace("**", "</b>",1)
        x+=1
    content=content.replace("\n", "<br>")
    h=0
    hh=False
    content=list(content)
    for i in range(len(content)-1):
        print(f"i {content[i]} i+1 {content[i+1]}")
        if content[i] =='h' and content[i+1] =="1":
            h=1
            print(h)
        if content[i] =='h' and content[i+1] =="2":
            h=2
        if content[i] =='h' and content[i+1] =="3":
            h=3
        if content[i] =='h' and content[i+1] =="4":
            h=4
        if content[i] =='h' and content[i+1] =="5":
            h=5
        if content[i] =='h' and content[i+1] =="6":
            h=6
       
        if content[i] == '<' and content[i+1] == 'b' and content[i+2] == 'r' and content[i+3] == '>' and h>0:
            content[i]="</h1>"
            content[i+1] = '<'
            content[i+2] = 'br'
            content[i+3] ='>'
            h=0
         
        elif content[i] == '\n':
            content[i]="<br>"
        x="".join(content)
        #content = x
    return(x)
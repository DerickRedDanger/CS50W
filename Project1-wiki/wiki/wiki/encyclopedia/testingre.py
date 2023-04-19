import re
#coding created to read the markdown and transform it into html code
def read(content):
    # replace # for the apropriated Hnumber, 
    # going from most complex to most basic 
    # as the oposite would replace the complex or the basic version
    # ex: starting with # woul replace ### with 3 <h1>
    content=content.replace("###### ", "<h6>")
    content=content.replace("##### ", "<h5>")
    content=content.replace("#### ", "<h4>")
    content=content.replace("### ", "<h3>")
    content=content.replace("## ", "<h2>")
    content=content.replace("# ", "<h1>")
    x=0

    # same idea as before, but since theses come in pairs
    # it was set to replace only one, than moving to the next command,
    # than set to repeat 20 times to make sure it replaced all of the
    # ocurrences.
    # startin with the complexes ones
    while x <20:
        content=content.replace("***", " <b><i>",1)
        content=content.replace("***", "</b></i> ",1)
        content=content.replace("_ _", " <i>",1)
        content=content.replace("_ _", "</i> ",1)
        content=content.replace("__", " <b>",1)
        content=content.replace("__", "</b> ",1)
        x+=1
    x=0
    # than moving to the simple ones
    while x <20:
        content=content.replace("* *", " <i>",1)
        content=content.replace("* *", "</i> ",1)
        content=content.replace("**", " <b>",1)
        content=content.replace("_", " <i>",1)
        content=content.replace("_", "</i> ",1)
        content=content.replace("**", "</b> ",1)
        content=content.replace("~~", " <del>",1)
        content=content.replace("~~", "</del> ",1)
        x+=1

    # preparing unordered lists
    content=content.replace("* ", "<li> ")
    # variables for creating list
    ulis=False
    olis=False
    num=[0,1,2,3,4,5,6,7,8,9]
    # replacing markdown's line break for  html's one
    content=content.replace("\n", "<br>")
    content=content.replace("\r", "")
    h=0
    # turning the content into a list to interact with each of it's elements
    content=list(content)
    print(content)
    # lists to save and replace links
    ltext=[]
    url=[]
    # variables use to replace links
    para=False
    bracket=False
    # closing the <hn> at the each line break 
    for i in range(len(content)-1):
        if content[i] =='h' and content[i+1] =="1":
            h=1
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
            content[i]=f"</h{h}>"
            content[i+1] = '<'
            content[i+2] = 'br'
            content[i+3] ='>'
            h=0

        # creating ordered list

        # if a number is followed by period, replace it for <li>, if it's the first case, also add <ol>
        if (content[i] == "0" or content[i] == "1" or content[i] == "2" or content[i] == "3" or content[i] == "4" or content[i] == "5" or content[i] == "6" or content[i] == "7" or content[i] == "8" or content[i] == "9") and content[i+1]=="." :
        # had to go throught each number since "if content[i] in num" didn't work, with num = [0,1,2,3,4,5,6,7,8,9]
            if olis == False:
                content[i]="<ol>"
                content[i+1]="<li>"
                olis= True
            elif olis == True:
                content[i]=""
                content[i+1]="<li>"

        #replacing line breaks for </li>
        if content[i] == '<' and content[i+1] == 'b' and content[i+2] == 'r' and content[i+3] == '>' and olis==True:
            content[i] ="</li>"
            content[i+1] =""
            content[i+2] = ""
            content[i+3] =""

        #if there aren't numbers with dot after </li>, close the ordered list
        if content[i] == '</li>' and content[i+2] == '' and content[i+5]!="." and olis==True:
            content[i+1] = '</ol>'
            olis=False

        #remove any extra <br>
        try:
            if content[i] == '<' and content[i+1] == 'b' and content[i+2] == 'r' and content[i+3] == '>' and content[i+5]=="." and olis==True:
                content[i]=''
                content[i+1] = ''
                content[i+2] = ''
                content[i+3] =''
        except:
            pass


        #creating unordered list

        #starting unordered list after the first <li> placed throught replace
        if content[i] == '<' and content[i+1] == 'l' and content[i+2] == 'i' and content[i+3] == '>' and ulis==False:
            content[i] = '<ul>'
            content[i+1] = '<l'
            ulis=True

        # using try so it doesn't give a error when it reaches the end of the page
        try:
            #switching line break for </li> 
            if content[i] == '<' and content[i+1] == 'b' and content[i+2] == 'r' and content[i+3] == '>' and content[i+5]=="l" and ulis==True:
                content[i]='<'
                content[i+1] = '/l'
                content[i+2] = 'i'
                content[i+3] ='>'
            #if no more <li> after a <br>, close unordered list (</ul>)
            elif content[i] == '<' and content[i+1] == 'b' and content[i+2] == 'r' and content[i+3] == '>' and content[i+5]!="l" and ulis==True:
                content[i]="</ul>"
                content[i+1] = '<'
                content[i+2] = 'br'
                content[i+3] ='>'
                ulis=False
        except:
            pass

        # replacing text and link for A tag
        if content[i]=="[" and bracket == False:
            bracket = True
            content[i]='<a hreft="'
            link = i + 1

        elif content[i]=="]" and bracket == True:
            bracket = False
            content[i]=""

        elif bracket == True:
            ltext.append(content[i])
            content[i]=""

        elif content[i]=="(" and para == False:
            para = True
            content[i]=""
        
        elif content[i]==")" and para == True:
            para = False
            ltext="".join(ltext)
            content[i-1]=f">{ltext}"
            print(f"ltext = {ltext}")
            ltext=[]
            content[i]="</a>"
            url="".join(url)
            content[link]=f'{url}"'
            print(f"url={url}")
            url=[]

        elif para == True:
            url.append(content[i])
            content[i]=""


        # returning it to the function
    

    x="".join(content)


    return(x)
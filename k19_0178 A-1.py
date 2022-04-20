import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tkinter import *
from PIL import ImageTk,Image


class Boolean_retrieval:
    
    positional_index={}
    inverted_index={}
    stopwords=[]
    
    def __init__(self):
        #initializing stopwords  to the class variable returned from stopwords function
        self.stopwords=self.readstopword() 
     
        #reading stop words from file
    def readstopword(self):
        #Reading Stopwords from Stopwords file
        f=open("Stopword.txt","r")
        stwd=f.read()
        #Removing 'Spaces" and \n from the words and making a list
        stwd=stwd.replace(" ","")
        stwd=stwd.split("\n")
        f.close()
        # return the stop words
        return stwd
    
    #reading the file and removing special characters and converting to lower case
    def treat_file(self,num):
        #Reading from File
        f = open("Abstracts\\" +str(num)+".txt","r")
        file1=f.read()
        #Removing numbers and special chanacters and converting to lower case
        file1=re.sub('[^A-Za-z0-9]+', ' ', file1).lower()
        f.close()
        return file1
    #removing stop words from the provided list
    def filter_stopwords(self,file_words,sw):
        #removing stop words in this function
        filtered_words=[]
        for words in file_words:
            if words not in sw:
                filtered_words.append(words)            
        return filtered_words
    #applying stemming to the applied list  and neglecting the words with length < 1
    def apply_stemming(self,filtered_words):
        # apply poter stemming from  builtin library nltk
        ps = PorterStemmer()
        stemmed_list=[]
        for words in filtered_words:
            if(len(ps.stem(words))>1):
                stemmed_list.append(ps.stem(words))
        return stemmed_list
    
    #storing the file list in inverted index
    def Inverted_index(self,st_word,num):
        #creating inverted index from a set of list of words
        for word in st_word:
            if word not in self.inverted_index:
                self.inverted_index[word]=[num]
            elif word in self.inverted_index:
                self.inverted_index[word].append(num)
                
    #processing and creating inverted index the the entire 449 files by applying steeming,
    #removing stop words by calling the above functions
    def Create_Inverted_index(self):
        for x in range(1,449):
            file_words=[]
            
            #reading the file and cleaning it
            file_paragraph=self.treat_file(x)
            #removing numbers to
            file_paragraph=re.sub('[^A-Za-z]+', ' ', file_paragraph).lower()
            file_words=file_paragraph.split()
            
            filter_stop=[]
            #removing stop words
            filter_stop=self.filter_stopwords(file_words,self.stopwords)
            stem_list=[]
            #applying stemming
            stem_list=self.apply_stemming(filter_stop)
            #removing duplicates
            stem_list=list(dict.fromkeys(stem_list))
            #Creating inverted index
            self.Inverted_index(stem_list, x)
            
        #storing the inverted index in file
        f = open("inverted_index.txt", "w")
        for key in sorted(self.inverted_index):
           f.write(key + '->' +str(self.inverted_index[key])+'\n')
        f.close()

        
    #Performing Intersection or we can say AND operation between 2 list
    def andoperation(self,t1,t2):
        iresult=[value for value in t1 if value in t2]
        return iresult
        
    #PErforming not operation
    def notoperation(self,t1):
        iresult=[]
        for id in range (1,449):
            if id not in t1:
                iresult.append(id)
        return iresult
    
    
    #Performing Or operation
    def oroperation(self,t1,t2):
        iresult=sorted(list(set(t1) | set(t2)))
        return iresult
           
    #processing boolean queries and search from inverted index    
    def boolean_query_process(self,query):
        #processing the boolean query
        ps = PorterStemmer()
        #defining the list of boolean operators
        operator_list=['AND','OR','NOT']
        #MAking a list of the querys and splitting the querry into tokens
        query_list=query.split()
        
        #applying stemming to query terms except boolean operators
        temp_dict={}
        
        for x in range (0,len(query_list)):
            if query_list[x] not in operator_list:
                word=query_list[x]
                query_list[x]=ps.stem(word.lower())
                temp_dict[query_list[x]]=self.inverted_index[query_list[x]]
        
        result=[]
        #checking the if the first term is a term and not  a boolean query
        #storing the term as result so we can process linearly onwords
        if(query_list[0] != 'NOT'):     
            result=temp_dict[query_list[0]]
        else:
            #if the first term is not operator 
            result=self.notoperation(temp_dict[query_list[1]])
        for  x in range (0,len(query_list)-1): 
            n1=[]
            if(query_list[x] == 'AND'):
                if(query_list[x+1]=='NOT'):
                    n1=self.notoperation(temp_dict[query_list[x+2]])
                    result=self.andoperation(result, n1)
                else:
                    result=self.andoperation(result,temp_dict[query_list[x+1]])
            elif(query_list[x]=='OR'):
                if(query_list[x+1]=='NOT'):
                    n1=self.notoperation(temp_dict[query_list[x+2]])
                    result=self.oroperation(result, n1)
                else:
                    result=self.oroperation(result,temp_dict[query_list[x+1]])
                    
        return result
        
        
        #creating positional index of the 449 file provided and treating the document from above methods
    def Create_positional_index(self):
        
        for doc_id in range (1,449):
            
            file_words=[]
            #reading the file and cleaning it
            file_paragraph=self.treat_file(doc_id)
            file_words=file_paragraph.split()
            ps = PorterStemmer()
            for x in range (0,len(file_words)):
                file_words[x]=ps.stem(file_words[x])    
                #Condition to check if the words are not stop words & numbers and their length > 1 
                if((file_words[x] not in self.stopwords) and (file_words[x].isnumeric()==False) and len(file_words[x])>1):
                    
                    #Now creating positional index
                    if file_words[x] not in self.positional_index:
                        self.positional_index[file_words[x]]={}
                        self.positional_index[file_words[x]][doc_id]=[]
                        self.positional_index[file_words[x]][doc_id].append(x+1)
                    else:
                        if doc_id not in self.positional_index[file_words[x]]:
                            self.positional_index[file_words[x]][doc_id]=[]
                            self.positional_index[file_words[x]][doc_id].append(x+1)
                        else:                        
                            self.positional_index[file_words[x]][doc_id].append(x+1)
                            
                      
        #storing the positional index in File
        f = open("positional_index.txt", "w")
        for key in sorted(self.positional_index):
           f.write(key + '->' +str(self.positional_index[key])+'\n')    
        f.close()

        
        #processing the queries and searching in positional index
    def proximity_queries(self,query):
        ps = PorterStemmer()
        #creating tokens of the query
        query_list=word_tokenize(query)
        new_list=[]
        temp_dict={}
        result=[]
  
        #PRocessing the  proximity query
        for word in query_list:  
               word=ps.stem(word)
               if('/' in word):   
                   #Removing / from the digit
                    new_list.append(word.strip('/'))
               else:
                    new_list.append(word)
                    temp_dict[word]=self.positional_index[word]
                    
                
        #Fetching result            
        for n in range (0,len(new_list)):
            if new_list[n].isdigit() == True:
                distance=int(new_list[n])+1
                for key in temp_dict[new_list[n-2]]:
                    #checking the common documentids for both terms
                    if key in temp_dict[new_list[n-1]]:
                        #getting list of of locations of the terms from both of the document ids
                        l1=temp_dict[new_list[n-2]][key]
                        l2=temp_dict[new_list[n-1]][key]
                        for x in range (0,len(l1)):
                            for y in range (0,len(l2)):
                                if(abs(l1[x]-l2[y])<=distance):
                                    result.append(key)
                                    
        #Removing duplicate documents                    
        result=list(dict.fromkeys(result))
        return result
        
        
        
        
    
                                    
                                    
#checking if the query is boolean or proximity
def check_query(query):
    operator='/'
    result=[]
    if operator in query:
       result= p1.proximity_queries(query)
    else:
       result= p1.boolean_query_process(query)
    #storing the output in file
    f=open("Outputfile.txt","a")
    f.write('Query is: '+ query + '\n' + 'Result=>'+str(result) +'\n')
    f.close()
    
    return result
                             
#this function is called when search button is pressed in GUI                        
def search():
    output.delete("1.0","end")
    output.insert(END,"Terms found in Documents:"+str(check_query(input1.get())))
      
           
         
p1=Boolean_retrieval()
#creating inverted and positional index
print("Creating boolean and positional index")
p1.Create_Inverted_index()
p1.Create_positional_index()


#Making GUI
#In TKinter to place a widget in any where on the screen we can use pack,place or grid

window =Tk()

window.title("Boolean Retireval Model Assignment-1")
window.minsize(width=700,height=800)

#Padding the window and setting the Background Color
window.config(padx=50,bg='#B7CADB')

#Setting image
canvas=Canvas(width=724,height=501,bg='#B7CADB',highlightthickness=0)
img=PhotoImage(file="img1.png")
canvas.create_image(362,250, image=img)

#Roll no text field
my_label=Label(text="K19-0178 A-1 ",font=("Arial",24),bg='#B7CADB')
my_label.place(relx=0.5,rely=0.55,anchor="center")

#Asking  for query text field
my_label=Label(text="Enter Query: ",font=("Arial",24,"bold"),bg='#B7CADB')
my_label.place(relx=0.5,rely=0.6,anchor="center")


#input field 
input1=Entry(width=50,font=("Arial",15))
input1.place(relx=0.5,rely=0.65,anchor="center")

#Button field
button=Button(text="Search",command=search,width=10,height=1,bg='#6FB2D2')
button.place(relx=0.5,rely=0.7,anchor="center")

#Output field
output=Text(height=7,width=69,bg='#B7CADB')
output.insert(END,"")
output.place(relx=0.12,rely=0.75)

canvas.pack()
window.mainloop()




import sqlite3 as lite
import sys
import os
import unittest

path = os.path.dirname(__file__) + "\\test.db"
con = lite.connect(path)
cur = con.cursor()


class MVCModel:
    
    def request(self, id, field):
        cur.execute("SELECT id FROM TodoList")        
        id_temp=cur.fetchall()  
        if id>id_temp[len(id_temp)-1][0] :
            print("The id %d is not stored!" %id)
            pass
        results = cur.execute("SELECT %s FROM TodoList Where id = %d" %(field,id))
        for row in results:
            name = row[0]
        return id,name
            
    def requestAll(self):      
        cur.execute("SELECT * FROM TodoList")       
        works=[]
        while True:        
            row = cur.fetchone()         
            if row == None:
                break
            works.append(row)
        return works       
    
    def checkId(self,id):
        isExisted=False
        cur.execute("SELECT id FROM TodoList")        
        id_temp=cur.fetchall()
        for id_value in id_temp:           
            if id==id_value[0] :
                isExisted=True
                break
        return isExisted 

    def getIdQuantily(self):
        
        cur.execute("SELECT id FROM TodoList")        
        id_temp=cur.fetchall()
        return len(id_temp)        
                 
    def add(self, id, work_name, starting_date, ending_date, status): 
        cur.execute("INSERT INTO TodoList (id, WorkName, StatingDate , EndingDate , Status) VALUES (?, ?, ?, ?, ?)", (id, work_name, starting_date, ending_date, status))
        
        con.commit()
        id_temp,name_temp=self.request(id,'WorkName')
        print(" \'{}\' is added!".format(name_temp))
        
    def edit(self, id, work_name=None, starting_date= None, ending_date=None, status=None):
        if work_name is None:
            _,work_name=self.request(id, 'WorkName')
        if starting_date is None:
            _,starting_date=self.request(id, 'StatingDate')
        if ending_date is None:
            _,ending_date=self.request(id, 'EndingDate')
        if status is None:
            _,status=self.request(id, 'Status')   
        cur.execute("UPDATE TodoList SET WorkName = ?,StatingDate = ?, EndingDate = ?, Status = ? WHERE id = ?", (work_name, starting_date, ending_date, status, id))
        con.commit()
        
    def delete(self,id):
        cur.execute("DELETE FROM TodoList WHERE id = %d" % id)
        con.commit()
    

class MVCController:    

    def __init__(self):
        self.model = MVCModel()
        self.view = MVCView()
      
    def main(self):

        print("Welcome to the Todo List") 
        order=input('Do you want to show To do List? (y/n): ')            
        if order =='y':
            self.view.showAll(self.model.requestAll())
        else:
            print("Ok, So!")
        del order
        while True:           
            order=input('Do you want to do anything else? (a)add, (e)edit, (d)delete, s(show), (n)no:   ')
            if order=='a':
                id, work_name, starting_date, ending_date, status= input("Please input id, Work Name, Starting date, Ending date and Status to add:\n").split(',')   
                self.addWork(int(id), work_name, starting_date, ending_date, status)
            elif order=='e':
                id, work_name, starting_date, ending_date, status= input("Please input id, Work Name, Starting date, Ending date and Status to edit:\n").split(',')
                self.editWork(int(id), work_name, starting_date, ending_date, status)
            elif order=='d':
                id=int(input("Please input id: "))
                self.deleteWork(id)
            elif order=='s':
                self.view.showAll(self.model.requestAll())
            elif order=='n':
                print("Ok, Goodbye!")
                break
            elif order!='a' or order!='e' or order!='d' or order!='n':
                print("The term \'{}\' is not recognized as the name of a order.".format(order))
                print("Please input again!")                          
        
    def addWork(self, id, work_name, starting_date, ending_date, status):        
        if(self.model.checkId(id)):
            self.view.displayIdIsExist(id)
        else:
            id_quantily=self.model.getIdQuantily()
            id=id_quantily+1            
            self.model.add(id, work_name, starting_date, ending_date, status)            
        self.view.showAll(self.model.requestAll())        
        
    def editWork(self, id, work_name=None, starting_date= None, ending_date=None, status=None):
        if(self.model.checkId(id)==False):
            self.view.displayIdIsNotExist(id)
        else:
            self.model.edit(id, work_name, starting_date, ending_date, status)
            self.view.displayUpdated(id) 
        self.view.showAll(self.model.requestAll())
        
    def deleteWork(self,id):
         if(self.model.checkId(id)==False):
            self.view.displayIdIsNotExist(id)
         else:
            _,workName=self.model.request(id,'WorkName')
            self.model.delete(id)
            self.view.displayDeleted(id,workName)
         self.view.showAll(self.model.requestAll())      


class MVCView:    

    def showAll(self, posts):
        print('{:^68}'.format('**** To do List ****'))
        print (' '+'_'*67)
        print ('|{:^5}|{:^20}|{:^15}|{:^13}|{:^10}|'.format('id','Work Name','Starting Date','Endind date','Status'))
        print ('|{:^5}|{:^20}|{:^15}|{:^13}|{:^10}|'.format('-'*5,'-'*20,'-'*15,'-'*13,'-'*10))
        for post in posts:
            print('|{:^5}|{:<20}|{:^15}|{:^13}|{:<10}|'.format( post[0],post[1],post[2],post[3],post[4]))          
        print ('|{:^5}|{:^20}|{:^15}|{:^13}|{:^10}|'.format('_'*5,'_'*20,'_'*15,'_'*13,'_'*10))
        
    def displayIdIsNotExist(self,id):
        print("The ID %d is not exist!" %id)
        print("Please chose another one!")
        
    def displayIdIsExist(self,id):
        print("The ID %d is exist!" %id)
        print("Please chose another one!")
        
    def displayIdAlreadyStored(self,id):
        print("The ID %d already store!" %id)
        
    def displayUpdated(self,id):
        print("The ID %d is updated!" %id)
        
    def displayDeleted(self, id, work_name):
        print("\'{}\' with ID {} is deleted!".format(work_name,id))

Controller = MVCController()
Controller.main()



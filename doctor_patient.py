import sync
import math

cnx=sync.cnx
mycursor=cnx.cursor()

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
   
    else: 
        _ = system('clear')

def compare(a,b):
    if a==b:
        return 0;
    else:
        return 1;
def add_drug_qty(p_base,d,dr,qt,doc,p_id):
    drug='drug'+str(d)
    cust=p_base
    sql='alter table '+str(cust)+' add column '+str(drug)+' varchar(30)'
    mycursor.execute(sql)
    qty='qty'+str(d)
    sql='alter table '+str(cust)+' add column '+str(qty)+ ' decimal(8,3)'
    mycursor.execute(sql)
    val='insert into '+str(cust)+"(c_id, doc_username,"+str(drug)+","+str(qty)+") values ("+str(p_id)+",'"+str(doc)+"','"+str(dr)+"',"+str(qt)+')'
    mycursor.execute(val)
    cnx.commit()
def check_n_drugs(p_base):
    mycursor.execute('show columns from '+str(p_base))
    n=mycursor.fetchall()
    if len(n)==1:
        k=0
    else:
        k=int(n[len(n)-1][0][3])
    return k
login_out='y'
while login_out=='y':
    duser=input("doctor's username: ")
    dpass=str(input("doctor's password: "))
    sql = "SELECT password FROM doc WHERE username= %s"
    comp=(duser, )
    mycursor.execute(sql,comp)
    n=mycursor.fetchall()
    if not n:
        print("username not matching")
        login_out=input('to try logging in again press y and any other character to exit application: ') 
    elif compare(str(n[0][0]),dpass)==0:
            print('you are logged in')
            in_out='y'
            while in_out=='y':
                total_quantity=0
                p_id=input('enter patient identification number: ')
                p_name=input('enter patient name: ')
                sql = "SELECT cname FROM customer WHERE c_id= %s"
                comp=(p_id,)
                mycursor.execute(sql,comp)
                n=mycursor.fetchall()
                if not n:
                    print("no such patient data found")
                else:
                    if compare(str(n[0][0]),p_name)==0:
                        print('logged into patient data base through doctor_id ',duser)
                        p_base='cust'+str(p_id)
                        add='y'
                        add=input("enter y to add medicines to patient treatment and enter any other key to logout from patient data base: ")
                        while add=='y':
                            dr_name=input('enter drug name: ')
                            dr_qty=round(float(input('enter quantity in ounce: ')),3)
                            sql="select*from drug where dname='"+str(dr_name)+"'"
                            mycursor.execute(sql)
                            rov=mycursor.fetchall()
                            if not rov:
                                print('enter valid drug name')
                            else:
                                mycursor.execute("show tables")
                                n=mycursor.fetchall()
                                c=0
                                for i in range(len(n)):
                                    if p_base==str(n[i][0]):
                                        c=c+1
                                    else:
                                        c=c
                                if c==0:    
                                    d=1
                                    sql='create table '+str(p_base)+' (c_id int, doc_username varchar(25))'
                                    mycursor.execute(sql)
                                    add_drug_qty(p_base,d,dr_name,dr_qty,duser,p_id)
                                else:
                                    for j in range(1,check_n_drugs(p_base)+1):
                                        sql="select sum(qty"+str(j)+") from "+str(p_base)
                                        mycursor.execute(sql)
                                        n=mycursor.fetchall()
                                        total_quantity=round(((n[0][0])+total_quantity),3)
                                    if total_quantity==0:
                                        sql='drop table '+str(p_base)
                                        mycursor.execute(sql)
                                        d=1
                                        sql='create table '+str(p_base)+' (c_id int, doc_username varchar(25))'
                                        mycursor.execute(sql)
                                        add_drug_qty(p_base,d,dr_name,dr_qty,duser,p_id)
                                    else:
                                        n_drugs=check_n_drugs(p_base)+1
                                        add_drug_qty(p_base,n_drugs,dr_name,dr_qty,duser,p_id)
                            add=input("enter y to add medicines to patient treatment and enter any other key to logout from patient data base: ")
                    else:
                        print('patient_id and name did not match')
                in_out=input("Enter 'y' to stay logged in and 'n' to log out as doctor but stay in application and any other character to exit application: ")
                if in_out=='y' or in_out=='n':
                   continue
                else:
                   login_out='n'
    else:
        print('username and password are not matching')
        login_out=input("enter y to start transaction and any other character to logout: ")





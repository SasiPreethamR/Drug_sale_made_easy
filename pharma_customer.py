import sync
import bill

def s(a):
   r=0   
   for x in range(len(a)):
      r=r+a[x]
   return round(r,3)
      
         
def screen_clear():
   if name == 'nt':
      _ = system('cls')
   else:
      _ = system('clear')

cnx=sync.cnx
mycursor=cnx.cursor()
def check_n_drugs(p_base):
    mycursor.execute('show columns from '+str(p_base))
    n=mycursor.fetchall()
    if len(n)==1:
        k=0
    else:
        k=int(n[len(n)-1][0][3])
    return k

def compare(a,b):
    if a==b:
        return 0;
    else:
        return 1;
login_out='y'
while login_out=='y':
   duser=input("pharma's user_id: ")
   dpass=str(input("pharma's password: "))
   sql = "SELECT password FROM druggist WHERE vend_id= %s"
   comp=(duser, )
   mycursor.execute(sql,comp)
   n=mycursor.fetchall()
   if not n:
      print("user_id not matching")
      login_out=input('to try logging in again press y and any other character to exit application: ') 
   elif compare(str(n[0][0]),dpass)==0:
         print('you are logged in')
         repeat='y'
         repeat=input("enter y to start transaction and any other character to logout: ")
         while repeat=='y':
            name=[]
            bname=[]
            quantity=[]
            bquantity=[]
            d=[]
            cost=[]
            t_cost=[]
            doc_id=[]
            c_qty=int(input("enter no.of medicines customer want: "))
            for x in range(1,c_qty+1):
                ask_d=input('enter drug'+str(x)+' name: ')
                name.append(ask_d)
                ask_q=round(float(input('enter drug'+str(x)+' quantity(in ounces): ')),3)
                quantity.append(ask_q)
            c_id=input("enter customer id: ")
            cname=input("enter customer name: ")
            c_base='cust'+str(c_id)
            mycursor.execute('show tables')
            n=mycursor.fetchall()
            c=0
            for i in range(len(n)):
                if c_base==str(n[i][0]):
                    c=c+1
                else:
                    c=c
            if c==0:
                for i in range(c_qty):
                    sql="select type from drug where dname='"+str(name[i])+"'"
                    mycursor.execute(sql)
                    n=mycursor.fetchall()
                    if not n:
                        d.append('no such drugs exist')
                        bname.append(name[i])
                        bquantity.append(quantity[i])
                        cost.append('-')
                        t_cost.append('-')
                        doc_id.append('-')
                    elif n[0][0]=='p':
                        d.append('prescription required')
                        bname.append(name[i])
                        bquantity.append(quantity[i])
                        cost.append('-')
                        t_cost.append('-')
                        doc_id.append('-')
                    else:
                        d.append('issued')
                        sql="select cost from drug where dname='"+str(name[i])+"'"
                        mycursor.execute(sql)
                        n=mycursor.fetchall()
                        bname.append(name[i])
                        bquantity.append(quantity[i])
                        cost.append(n[0][0])
                        t_cost.append(int(n[0][0])*quantity[i])
                        doc_id.append('-')
            else:
                for i in range(c_qty):
                    c1=[]
                    c2=[]
                    n_drugs=check_n_drugs(c_base)
                    for j in range(1,n_drugs+1):
                        sql='select qty'+str(j)+" from "+str(c_base)+" where qty"+str(j)+">0 and drug"+str(j)+"='"+str(name[i])+"'"
            
                        mycursor.execute(sql)
                        n=mycursor.fetchall()
                        if not n:
                            c1.append(0)
                        else:
                            c1.append(round(float(n[0][0]),3))
                            c2.append(j)
                    if s(c1)==0:
                        sql="select type from drug where dname='"+str(name[i])+"'"
                        mycursor.execute(sql)
                        n=mycursor.fetchall()
                        if not n:
                            d.append('no such drug exists')
                            bname.append(name[i])
                            bquantity.append(quantity[i])
                            cost.append('-')
                            t_cost.append('-')
                            doc_id.append('_')
                        elif n[0][0]=='p':
                            d.append('prescription required')
                            bname.append(name[i])
                            bquantity.append(quantity[i])
                            cost.append('-')
                            t_cost.append('-')
                            doc_id.append('_')
                        else:
                            d.append('issued')
                            sql="select cost from drug where dname='"+str(name[i])+"'"
                            mycursor.execute(sql)
                            n=mycursor.fetchall()
                            bname.append(name[i])
                            bquantity.append(quantity[i])
                            cost.append(round(n[0][0],3))
                            t_cost.append(round(((n[0][0])*quantity[i]),3))
                            doc_id.append('_')
                    else:
                        co=0
                        for j in range(n_drugs):
                           if c1[j]==0:
                              continue
                           elif quantity[i]<=s(c1):
                              if quantity[i]<=c1[j]:
                                 d.append('issued')
                                 qq=round((c1[j]-quantity[i]),3)
                                 sql='update '+str(c_base)+' set qty'+str(c2[co])+'= '+str(qq)+' where drug'+str(c2[co])+"='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 cnx.commit()
                                 sql="select cost from drug where dname='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 n=mycursor.fetchall()
                                 bname.append(name[i])
                                 bquantity.append(quantity[i])
                                 cost.append(round(n[0][0],3))
                                 t_cost.append(round(((n[0][0])*quantity[i]),3))
                                 sql='select doc_username from '+str(c_base)+' where drug'+str(c2[co])+"='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 n=mycursor.fetchall()
                                 doc_id.append(n[0][0])
                                 break
                              else:
                                 d.append('issued')
                                 sql='update '+str(c_base)+' set qty'+str(c2[co])+'= 0 where drug'+str(c2[co])+"='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 cnx.commit()
                                 sql="select cost from drug where dname='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 n=mycursor.fetchall()
                                 bname.append(name[i])
                                 bquantity.append(c1[j])
                                 cost.append(round(n[0][0],3))
                                 t_cost.append(round(((n[0][0])*c1[j]),3))
                                 quantity[i]=round((quantity[i]-c1[j]),3)
                                 sql='select doc_username from '+str(c_base)+' where drug'+str(c2[co])+"='"+str(name[i])+"'"
                                 mycursor.execute(sql)
                                 n=mycursor.fetchall()
                                 doc_id.append(n[0][0])
                                 co=co+1
                           else:
                              d.append('only '+str(c1[j])+' ounce(s) alloted')
                              sql='update '+str(c_base)+' set qty'+str(c2[co])+'=0 where drug'+str(c2[co])+"='"+str(name[i])+"'"
                              mycursor.execute(sql)
                              quantity[i]=quantity[i]-c1[j]
                              cnx.commit()
                              sql="select cost from drug where dname='"+str(name[i])+"'"
                              mycursor.execute(sql)
                              n=mycursor.fetchall()
                              bname.append(name[i])
                              bquantity.append(c1[j])
                              cost.append(round(n[0][0],3))
                              t_cost.append(round(((n[0][0])*c1[j]),3))
                              sql='select doc_username from '+str(c_base)+' where drug'+str(c2[co])+"='"+str(name[i])+"'"
                              mycursor.execute(sql)
                              n=mycursor.fetchall()
                              doc_id.append(n[0][0])
                              co=co+1
            bill.print_bill(bname,bquantity,d,c_id,cname,cost,t_cost,c_qty,duser,doc_id)
            repeat=input("enter y to start transaction,n to logout but stay in application and any other key to exit application: ")
            if repeat=='y' or repeat=='n':
               continue
            else:
               login_out='n'
            
   else:
      print('user_id and password are not matching')
      login_out=input("enter y to start transaction and any other character to logout: ")

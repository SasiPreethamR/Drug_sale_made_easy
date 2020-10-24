def print_bill(name,quantity,d,c_id,cname,cost,t_cost,c_qty,duser,doc_id):
    print("")
    print("")
    print("                                                                      BILL/RECEIPT")                                                 
    print("NAME: "+str(cname))
    print("CUSTOMER_ID: "+str(c_id)+"                                                                                                               PHARMACY_ID:"+str(duser))
    print("")
    print('******************************************************************************************************************************************************************************')
    print("")
    print("Drug_Name                     qty                              status                             doc_username                             cost                           t_cost")
    print("")
    print("_______________________________________________________________________________________________________________________________________________________________________________")
    for i in range(len(name)):
        print(str(name[i])+(30-len(name[i]))*" "+str(quantity[i])+(35-len(str(quantity[i])))*" "+d[i]+(35-len(str(d[i])))*" "+str(doc_id[i])+(40-len(str(doc_id[i])))*" "+str(cost[i])+(30-len(str(cost[i])))*" "+str(t_cost[i]))
        print('')
    total_sum=0
    for x in range(len(t_cost)):
        if t_cost[x]=='-':
            total_sum=total_sum
        else:
            total_sum=total_sum+int(t_cost[x])
    print("                                                                                                                                                                     Total Cost="+str(total_sum))
    print("")
    print("")
    print("**NOTE:All values are quantised to a precision of three decimals while billing")
    print(2*"\n")

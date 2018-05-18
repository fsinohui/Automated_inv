# coding: utf-8
# Inventory Projection
# Created on Tue Dec 19 10:02:14 2017
# @author: FSinohui
''''''

# Import Dependencies
#import pyodbc
import pandas as pd
import os
import datetime
from inventory_projection_functions import whse_poh_, str_poh_,fc_, dd_,ecposo_, ecfc_,ord_qty_, message_
from inventory_projection_functions import po_, strss_, whsess_, fc_avg_, shrink_,need_index_,str_whse_poh_
from inventory_projection_functions import last_po_,header_creator_,header_creator_3_,wos_,top_range_, blocks_

print('Inventory Projection and Suggested Orders')
print('Start: ',datetime.datetime.now())

path = r'\\hftdata02\sysdata02\RedCat\Exports\python_exports'
#read in all the needed tables
ecom_pd         = pd.read_csv(path+'\Ecom_Processed.csv',index_col=0) #Sku
fcst_whsess_pd  = pd.read_csv(path+'\Forecast_WhseSS.csv',index_col=2)#ID
dd_pd           = pd.read_csv(path+'\DD_Processed.csv',index_col=0)
dates_pd        = pd.read_csv(path+'\Dates_Processed.csv',index_col=2) #ID
strss_pd        = pd.read_csv(path+'\str_SS_Processed.csv',index_col=0) #ID
po_pd           = pd.read_csv(path+'\PO_Pivot_processed.csv',index_col=0) #ID
shrink_pd       = pd.read_csv(path+'\shrink_Processed.csv',index_col=0)#sku
redcat_pd       = pd.read_csv(path+r'\redcat_Processed.csv',index_col=0)#ID index
wos_max_pd      = pd.read_csv(path+r'\wos_max_Processed.csv',index_col=2)

hft_inv_pd      = pd.read_csv(path+'\hft_inv_python.csv',index_col=0) #Sku not planned Sku
fcst_pd         = pd.read_csv(path+r'\forecast_python.csv', index_col=0)
item_master_pd  = pd.read_csv(path+'\item_master_python.csv',index_col=0) #Sku
whse_master_pd  = pd.read_csv(path+'\whse_master_python.csv')#sku
whse_master_pd['ID'] = whse_master_pd['SKU'].map(str) +'-'+ whse_master_pd['WHSE'].map(str)
whse_master_pd.set_index('ID',inplace=True)
whsess_pd       = pd.read_csv(path+'\whse_ss_python.csv',index_col=0) #ID


#How Many weeks to run in the projection_____________________________________________
wks2run = int(input('How many weeks to Run (normally 26): '))
year = int(input('Starting Year: '))
month = int(input('Starting Month: '))
day = int(input('starting Day: '))
start_date = datetime.datetime(year,month,day)

"""Starts the model in the current week. It is importent for Lead time considerations
Long range model doesn't need to consider the Lead time"""
run_state = 'present'

#_Create_the_Number_Lists__________________________________________________________

num_w_0_list = []
for x in range(wks2run):
    if x<9:
        num_w_0_list.append('0'+ str(x+1))
    else:
        num_w_0_list.append(str(x+1))

num_wo_0_list = []

# Make Inventory Block Headers
so_header = header_creator_(wks2run,'SO_')
fc_header = header_creator_3_(wks2run,'FC_')
whse_poh_header = header_creator_(wks2run,'WhsePOH_')
whse_poh_woso_header = header_creator_(wks2run,'WhsePOH_woso')
str_poh_header = header_creator_(wks2run,'StrPOH_')
str_poh_woso_header = header_creator_(wks2run,'StrPOH_woso')
str_whse_poh_header = header_creator_(wks2run,'Str_Whse_POH_')
str_whse_poh_woso_header = header_creator_(wks2run,'Str_Whse_POH_woso')
str_wos_woso_header = header_creator_(wks2run,'Str_WOS_woso')
dd_header = header_creator_(wks2run,'dd_')
po_header = header_creator_(wks2run,'PO_')
whse_wos_woso_header = header_creator_(wks2run,'Whse_WOS_woso_')
str_wos_header = header_creator_(wks2run,'Str_WOS_')
whse_wos_header = header_creator_(wks2run,'Whse_WOS_')
fc_avg8_header = header_creator_(wks2run,'FC_Avg_')

for x in range(wks2run):
    num_wo_0_list.append(str(x+1))

# Empty DataFrames to create inventory block exports________________________________
whse_poh_list_df            = pd.DataFrame()
str_poh_list_df             = pd.DataFrame()
str_whse_poh_list_df        = pd.DataFrame()
dd_list_df                  = pd.DataFrame()
whse_wos_list_df            = pd.DataFrame()
so_list_pivot_df            = pd.DataFrame()
whse_risk_list_df           = pd.DataFrame()
po_list_df                  = pd.DataFrame()
fc_list_df                  = pd.DataFrame()
so_list_df                  = pd.DataFrame()
whse_poh_woso_list_df       = pd.DataFrame()
str_poh_woso_list_df        = pd.DataFrame()
str_whse_poh_woso_list_df   = pd.DataFrame()
whse_wos_woso_list_df       = pd.DataFrame()
str_wos_woso_list_df        = pd.DataFrame()
str_wos_list_df             = pd.DataFrame()
fc_avg8_list_pivot_df       = pd.DataFrame()
count=0
# Run all sku whse _______________________________________________________________
for i, row in redcat_pd.iterrows():
    sku_whse = i
    count=count+1
    whse_poh = []
    str_poh = []
    fc = []
    dd = []
    po = []
    strss = []
    whsess = []
    fc_avg_8 = []
    fc_avg_16 = []
    shrink = []
    ecfc = []
    ecposo = []
    so = [0]*wks2run
    #print(i)
    #_Set_The_Variables_for_single_Sku_DC______________________________________________

    sku = int(redcat_pd.get_value(sku_whse, str("Sku"), takeable=False))
    whse = redcat_pd.get_value(sku_whse, str("Whse"), takeable=False)
    str_oh = redcat_pd.get_value(sku_whse, str("Store_OH"), takeable=False)
    whse_oh = redcat_pd.get_value(sku_whse, str("Whse_OH"), takeable=False)
    try:
        shrink_percent = -shrink_pd.get_value(sku, str("Net Purchase Impact"), takeable=False)
    except KeyError:
        shrink_percent = 0
    try:
        ec_group = ecom_pd.get_value(sku, str("Group No"), takeable=False)
        k89 = ecom_pd.get_value(sku, str("K89"), takeable=False)
    except KeyError:
        ec_group =0
        k89 = ''
    try:
        lt = whse_master_pd.get_value(i, str("COMB_LT"), takeable=False)
        lt = int(lt)
    except KeyError:
        lt = 0
    mor_cost = hft_inv_pd.get_value(sku, str("MOR_STD_COST"), takeable=False)
    dil_cost = hft_inv_pd.get_value(sku, str("DIL_STD_COST"), takeable=False)
    try:
        mcq = whse_master_pd.get_value(i, str("MASTER_CARTON_QUANTITY"), takeable=False)
        if mcq==0:
            mcq=1
    except:
        mcq=1
    rb_code = hft_inv_pd.get_value(sku, str("RB_CODE"), takeable=False)
    if whse == 953:
        cost = mor_cost
    elif whse == 952:
        cost = dil_cost
    else:
        cost = mor_cost
    fcl_20 = item_master_pd.get_value(sku, str("CONTAINER_QTY_20FT"), takeable=False)
    fcl_40 = item_master_pd.get_value(sku, str("CONTAINER_QTY_40FT"), takeable=False)
    fcl_40hq = item_master_pd.get_value(sku, str("CONTAINER_QTY_40FTHQ"), takeable=False)
    moq = item_master_pd.get_value(sku, str("MIN_ORDER_QUANTITY"), takeable=False)

    fc = fc_(fcst_pd, sku_whse, num_w_0_list)
    fc = blocks_(fcst_pd, sku_whse, num_w_0_list,'FC')
    fc_avg_16 = fc_avg_(fc,16)
    fc_avg_8  = fc_avg_(fc,8)
    dd = dd_(dd_pd, sku_whse, num_w_0_list)
    po =  po_(po_pd, sku_whse, num_w_0_list)
        
    last_po = last_po_(po)
    strss = strss_(strss_pd, sku_whse, num_w_0_list)
    ecfc = ecfc_(ecom_pd, sku, num_w_0_list)
    ecposo = ecposo_(ecom_pd, sku, num_w_0_list)
    whsess = whsess_(whsess_pd, sku_whse, num_w_0_list)
    shrink = shrink_(fc_avg_8, shrink_percent)

    #_Start_The_solve___________________________________________________________________
    whse_poh = whse_poh_(whse_oh,dd,po, shrink, whse,ec_group,ecposo,k89,ecfc,so,strss)
    whse_poh_woso = whse_poh_(whse_oh,dd,po, shrink, whse,ec_group,ecposo,k89,ecfc,so,strss)
    str_poh_woso = str_poh_(whse,str_oh,whse_oh,dd,po,fc,str_poh,whse_poh,so,strss)
    str_whse_poh_woso = str_whse_poh_(str_poh_woso,whse_poh_woso)
    whse_wos_woso = wos_(fc_avg_8,whse_poh_woso)
    str_wos_woso = wos_(fc_avg_8,str_poh_woso)
    try:
        wos_max = float(wos_max_pd.get_value(i, str("Max WOS Target"), takeable=False))
    except:
        wos_max = 8
    top_range = top_range_(wks2run,fc_avg_8,wos_max,whsess)
    
    need_index = need_index_(whse_poh,whsess,run_state, wks2run,lt)
    #Suggested order loop starts here.
    testing = 'y'
    while need_index<len(fc): #and testing == 'y':
        ord_qty = ord_qty_(need_index, whsess, whse_poh,fc_avg_8, fcl_20, fcl_40, fcl_40hq,mor_cost,dil_cost,moq,whse,mcq,wks2run)
        so[need_index]=ord_qty+so[need_index]
        whse_poh = whse_poh_(whse_oh,dd,po, shrink, whse,ec_group,ecposo,k89,ecfc,so,strss)
        max_at_order = top_range[need_index]
        min_at_order = whsess[need_index]
        mid_at_order = ((max_at_order-min_at_order)/2)+min_at_order
        whseoh_at_order = whse_poh[need_index]
        if need_index < last_po:
            not_last_po = 'Not Last PO'
        else:
            not_last_po = ''

        so_df = pd.DataFrame({'ID': sku_whse,
                              'Sku':[sku],
                              'Whse':[whse],
                              'Need_Index':[need_index],
                              'Need_Date': [start_date + datetime.timedelta(days=(int(7*need_index)))] ,
                              'Order_Qty':[ord_qty],
                              'Messages':message_(lt, need_index),
                              'RB_Code':rb_code,
                              'Cost':cost,
                              'Extended_Cost': cost*ord_qty,
                              'Last_PO': not_last_po,
                              'Whse_OH':whseoh_at_order,
                              'Min': min_at_order,
                              'Mid': mid_at_order,
                              'Max': max_at_order,
                              'Min_cost': min_at_order*cost,
                              'Mid_cost': mid_at_order*cost,
                              'Max_cost': max_at_order*cost})

        so_list_df = pd.concat([so_list_df,so_df])
        #new need. Grab what you need before this line.
        need_index = need_index_(whse_poh,whsess,run_state, wks2run,lt)
        #testing = input('Wish to continue? (y/n)')

    str_poh = str_poh_(whse,str_oh,whse_oh,dd,po,fc,str_poh,whse_poh,so,strss)
    str_whse_poh = str_whse_poh_(str_poh,whse_poh)
    str_wos = wos_(fc_avg_8,str_poh)
    whse_wos = wos_(fc_avg_8,whse_poh)
    
    # Make Inventory Blocks
    
    soi = [sku_whse]+so
    so_df = pd.DataFrame([soi], columns=so_header)
    so_list_pivot_df = pd.concat([so_list_pivot_df,so_df])
    
    fc_avg8i = [sku_whse]+fc_avg_8
    fc_avg8_df = pd.DataFrame([fc_avg8i], columns=fc_avg8_header)
    fc_avg8_list_pivot_df = pd.concat([fc_avg8_list_pivot_df,fc_avg8_df])

    fci = [sku_whse]+[sku]+[whse]+fc
    fc_df = pd.DataFrame([fci], columns=fc_header)
    fc_list_df = pd.concat([fc_list_df,fc_df])
    
    whse_pohi = [sku_whse]+whse_poh
    whse_poh_df = pd.DataFrame([whse_pohi], columns=whse_poh_header)
    whse_poh_list_df = pd.concat([whse_poh_list_df,whse_poh_df])

    whse_wosi = [sku_whse]+whse_wos
    whse_wos_df = pd.DataFrame([whse_wosi], columns=whse_wos_header)
    whse_wos_list_df = pd.concat([whse_wos_woso_list_df,whse_wos_df])
    
    whse_poh_wosoi = [sku_whse]+whse_poh_woso
    whse_poh_woso_df = pd.DataFrame([whse_poh_wosoi], columns=whse_poh_woso_header)
    whse_poh_woso_list_df = pd.concat([whse_poh_woso_list_df,whse_poh_woso_df])
     
    whse_wos_wosoi = [sku_whse]+whse_wos_woso
    whse_wos_woso_df = pd.DataFrame([whse_wos_wosoi], columns=whse_wos_woso_header)
    whse_wos_woso_list_df = pd.concat([whse_wos_woso_list_df,whse_wos_woso_df])
    
    str_pohi = [sku_whse]+str_poh
    str_poh_df = pd.DataFrame([str_pohi], columns=str_poh_header)
    str_poh_list_df = pd.concat([str_poh_list_df,str_poh_df])
    
    str_wosi = [sku_whse]+str_wos
    str_wos_df = pd.DataFrame([str_wosi], columns=str_wos_header)
    str_wos_list_df = pd.concat([str_wos_list_df,str_wos_df])
        
    str_poh_wosoi = [sku_whse]+str_poh_woso
    str_poh_woso_df = pd.DataFrame([str_poh_wosoi], columns=str_poh_woso_header)
    str_poh_woso_list_df = pd.concat([str_poh_woso_list_df,str_poh_woso_df])
    
    str_wos_wosoi = [sku_whse]+str_wos_woso
    str_wos_woso_df = pd.DataFrame([str_wos_wosoi], columns=str_wos_woso_header)
    str_wos_woso_list_df = pd.concat([str_wos_woso_list_df,str_wos_woso_df])
        
    str_whse_pohi = [sku_whse]+str_whse_poh
    str_whse_poh_df = pd.DataFrame([str_whse_pohi], columns=str_whse_poh_header)
    str_whse_poh_list_df = pd.concat([str_whse_poh_list_df,str_whse_poh_df])
    
    str_whse_poh_wosoi = [sku_whse]+str_whse_poh_woso
    str_whse_poh_woso_df = pd.DataFrame([str_whse_poh_wosoi], columns=str_whse_poh_woso_header)
    str_whse_poh_woso_list_df = pd.concat([str_whse_poh_woso_list_df,str_whse_poh_woso_df]) 
  
    ddi = [sku_whse]+dd
    dd_df = pd.DataFrame([ddi], columns=dd_header)
    dd_list_df = pd.concat([dd_list_df,dd_df])
  
    poi = [sku_whse]+po
    po_df = pd.DataFrame([poi], columns=po_header)
    po_list_df = pd.concat([po_list_df,po_df])

#print(so_list_df)

so_list_df.to_excel(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\Python_Messages.xlsx',
                    sheet_name='Suggested_Order_List',
                    columns=['ID', 'Sku', 'Whse','RB_Code', 'Need_Date','Order_Qty','Cost','Extended_Cost', 
                             'Messages','Last_PO','Whse_OH','Min','Mid','Max','Min_cost','Mid_cost','Max_cost'],
                    index=False)

try:
    os.remove(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\Inventory_Projection_w_Suggs.xlsx')
except FileNotFoundError:
    print('file not found')
    
try:
    os.remove(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\Inventory_Projection_wo_Suggs.xlsx')
except FileNotFoundError:
    print('file not found')

whse_writer = pd.ExcelWriter(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\Inventory_Projection_w_Suggs.xlsx',
                             engine='xlsxwriter')

whse_poh_list_df.to_excel(whse_writer,
                    sheet_name='Whse_POH',
                    columns=whse_poh_header,
                    index=False)

whse_wos_list_df.to_excel(whse_writer,
                    sheet_name='Whse_WOS',
                    columns=whse_wos_header,
                    index=False)

str_poh_list_df.to_excel(whse_writer,
                    sheet_name='Store_POH',
                    columns=str_poh_header,
                    index=False)

str_wos_list_df.to_excel(whse_writer,
                    sheet_name='Store_WOS',
                    columns=str_wos_header,
                    index=False)

str_whse_poh_list_df.to_excel(whse_writer,
                    sheet_name='Str_Whse_POH',
                    columns=str_whse_poh_header,
                    index=False)

dd_list_df.to_excel(whse_writer,
                    sheet_name='DepDem',
                    columns=dd_header,
                    index=False)

whsess_pd.to_excel(whse_writer,
                    sheet_name='WhseSS',
                    )

po_list_df.to_excel(whse_writer,
                    sheet_name='Purchase_Order',
                    columns=po_header,
                    index=False)

so_list_pivot_df.to_excel(whse_writer,
                    sheet_name='Suggested_Order',
                    columns=so_header,
                    index=False)

fc_list_df.to_excel(whse_writer,
                    sheet_name='Forecast',
                    columns=fc_header,
                    index=False)

whse_woso_writer = pd.ExcelWriter(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\Inventory_Projection_wo_Suggs.xlsx',
                             engine='xlsxwriter')

whse_poh_woso_list_df.to_excel(whse_woso_writer,
                    sheet_name='Whse_POH_woso',
                    columns=whse_poh_woso_header,
                    index=False)

whse_wos_woso_list_df.to_excel(whse_woso_writer,
                    sheet_name='Whse_WOS_woso',
                    columns=whse_wos_woso_header,
                    index=False)

str_poh_woso_list_df.to_excel(whse_woso_writer,
                    sheet_name='Store_POH_woso',
                    columns=str_poh_woso_header,
                    index=False)

str_wos_woso_list_df.to_excel(whse_woso_writer,
                    sheet_name='Store_WOS_woso',
                    columns=str_wos_woso_header,
                    index=False)

str_whse_poh_woso_list_df.to_excel(whse_woso_writer,
                    sheet_name='Str_Whse_POH_woso',
                    columns=str_whse_poh_woso_header,
                    index=False)

dd_list_df.to_excel(whse_woso_writer,
                    sheet_name='DepDem',
                    columns=dd_header,
                    index=False)

whsess_pd.to_excel(whse_woso_writer,
                    sheet_name='WhseSS',
                    )

po_list_df.to_excel(whse_woso_writer,
                    sheet_name='Purchase_Order',
                    columns=po_header,
                    index=False)

so_list_pivot_df.to_excel(whse_woso_writer,
                    sheet_name='Suggested_Order',
                    columns=so_header,
                    index=False)

fc_list_df.to_excel(whse_woso_writer,
                    sheet_name='Forecast',
                    columns=fc_header,
                    index=False)


# to CSV inventory blocks
# With Suggested orders
whse_poh_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\whse_poh_w.csv', sep=',',index=False)
whse_wos_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\whse_wos_w.csv', sep=',',index=False)
str_poh_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_poh_w.csv', sep=',',index=False)
str_wos_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_wos_w.csv', sep=',',index=False)
str_whse_poh_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_whse_poh_w.csv', sep=',',index=False)
dd_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\dd_w.csv', sep=',',index=False)
whsess_pd.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\whsess_w.csv', sep=',')
po_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\po.csv', sep=',',index=False)
so_list_pivot_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\so.csv', sep=',',index=False)
fc_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\fc.csv', sep=',',index=False)
fc_avg8_list_pivot_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\fc_avg8.csv', sep=',',index=False)
# Without Suggested orders. 
whse_poh_woso_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\whse_poh_wo.csv', sep=',',index=False)
whse_wos_woso_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\whse_wos_wo.csv', sep=',',index=False)
str_poh_woso_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_poh_wo.csv', sep=',',index=False)
str_wos_woso_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_wos_wo.csv', sep=',',index=False)
str_whse_poh_woso_list_df.to_csv(r'\\hftdata02\sysdata02\RedCat\Exports\Inventory_Blocks\str_whse_poh_wo.csv', sep=',',index=False)


print('End:',datetime.datetime.now())

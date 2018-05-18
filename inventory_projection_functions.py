# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 14:40:04 2017

@author: FSinohui

Functions for inventory projection

"""
#Projected On Hande for the whse
import numpy as np

def whse_poh_(whse_oh,dd,po,shrink, whse,ec_group,ecposo,k89,ecfc,so,strss):
    whse_poh = []
    negative =[]
    # Does the first week of projection
    if whse == 953:
        if ec_group == 1:
            if whse_oh-dd[0]+po[0]+so[0]+shrink[0]>0:
                whse_pohvalue = whse_oh-dd[0]+po[0]+so[0]+shrink[0]
                negativevalue = 0
            else:
                whse_pohvalue = 0
                negativevalue = max(-strss[0],whse_oh-dd[0]+po[0]+so[0]+shrink[0])
        elif ec_group == 2:
            if whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0]>0:
                whse_pohvalue = whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0]
                negativevalue = 0
            else:
                whse_pohvalue = 0
                negativevalue =max(-strss[0], whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0])
        else:
            if whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0]>0:
                whse_pohvalue = whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0]
                negativevalue = 0
            else:
                whse_pohvalue = 0
                negativevalue = max(-strss[0],whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecposo[0])
            
    else:
        if k89 == "K89":
            if whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecfc[0]>0:
                whse_pohvalue = whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecfc[0]
                negativevalue = 0
            else:
                whse_pohvalue = 0
                negativevalue = max(-strss[0],whse_oh-dd[0]+po[0]+so[0]+shrink[0]-ecfc[0])
        else:
            if whse_oh-dd[0]+po[0]+so[0]+shrink[0]>0:
                whse_pohvalue = whse_oh-dd[0]+po[0]+so[0]+shrink[0]
                negativevalue = 0
            else:
                whse_pohvalue = 0
                negativevalue = max(-strss[0],whse_oh-dd[0]+po[0]+so[0]+shrink[0])

    whse_poh.append(whse_pohvalue)
    negative.append(negativevalue)
    # completes the remander of the poh range    
    for x in range(1, len(dd)):
        if whse == 953:
            if ec_group == 1:
                if whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]+negative[x-1]>0:
                    whse_pohvalue = whse_poh[x-1]-dd[x]+negative[x-1]+po[x]+so[x]+shrink[x]
                    negativevalue = 0
                else:
                    whse_pohvalue = 0
                    negativevalue = max(-strss[0],whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]+negative[x-1])
            elif ec_group == 2:
                if whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1]>0:
                    whse_pohvalue = whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1]
                    negativevalue = 0
 
                else:
                    whse_pohvalue = 0
                    negativevalue = max(-strss[x],whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1])
            else:
                if whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1]>0:
                    whse_pohvalue = whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1]
                    negativevalue = 0
                else:
                    whse_pohvalue = 0
                    negativevalue = max(-strss[x],whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1])
        else:
            if k89 == "K89":
                if whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecfc[x]+negative[x-1]>0:
                    whse_pohvalue = whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecfc[x]+negative[x-1]
                    negativevalue = 0
                else:
                    whse_pohvalue = 0
                    negativevalue = max(-strss[x],whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecfc[x]+negative[x-1])
            else:
                if whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]-ecposo[x]+negative[x-1]>0:
                    whse_pohvalue = whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]+negative[x-1]
                    negativevalue = 0
                else:
                    whse_pohvalue = 0
                    negativevalue = max(-strss[x],whse_poh[x-1]-dd[x]+po[x]+so[x]+shrink[x]+negative[x-1])
    
        whse_poh.append(whse_pohvalue)
        negative.append(negativevalue)
    return whse_poh 

# Store projected on hands
def str_poh_(whse,str_oh,whse_oh,dd,po,fc,str_poh,whse_poh,so,strss):  
    str_poh = []
    negative =[]
    # Does the first week of projection
    
    if (whse_oh+so[0]+po[0]) >= dd[0]:
        if str_oh+dd[0]-fc[0] > 0:
            str_pohvalue = str_oh+dd[0]-fc[0] 
            negativevalue = 0 
        else:
            str_pohvalue = 0
            negativevalue = min(-(str_oh+dd[0]-fc[0]),strss[0])
            
    else:
        if str_oh+(whse_oh+so[0]+po[0])-fc[0] >= 0:
            str_pohvalue = str_oh+(whse_oh+so[0]+po[0])-fc[0] 
            negativevalue = min(dd[0]-(whse_oh+so[0]+po[0]),strss[0])
            
        else:
            str_pohvalue = 0
            negativevalue = min(dd[0]-(whse_oh+so[0]+po[0])-(str_oh+dd[0]-fc[0]),strss[0])
    
    str_poh.append(str_pohvalue)
    negative.append(negativevalue)
    # completes the remander of the str poh range    
    for x in range(1, len(dd)):
       # if x==8:
            #print(whse_poh[x-1]+so[x]+po[x], ' > ',dd[x]+negative[x-1])
            #print(whse_poh[x-1]+so[x]+po[x])
        if (whse_poh[x-1]+so[x]+po[x]) > dd[x]+negative[x-1]:
            if str_poh[x-1]+dd[x]+negative[x-1]-fc[x] > 0:
                str_pohvalue = str_poh[x-1]+dd[x]+negative[x-1]-fc[x] 
                negativevalue = 0   
            else:
                str_pohvalue = 0
                negativevalue = min(-(str_poh[x-1]+dd[x]+negative[x-1]-fc[x]),strss[x])
        else:
            if str_poh[x-1]+max((whse_poh[x-1]+so[x]+po[x]),0)-fc[x] >= 0:
                str_pohvalue = str_poh[x-1]+max((whse_poh[x-1]+so[x]+po[x]),0)-fc[x] 
                negativevalue = min(dd[x]+negative[x-1]-max((whse_poh[x-1]+so[x]+po[x]),0),strss[x])
            else:
                str_pohvalue = 0
                negativevalue = min(dd[x]+negative[x-1]-max((whse_poh[x-1]+so[x]+po[x]),0)-(str_poh[x-1]+dd[x]-fc[x]),strss[x])
    
        str_poh.append(str_pohvalue)
        negative.append(negativevalue)
    return str_poh

# Str_whse_POH
def str_whse_poh_(str_poh,whse_poh):
    str_whse_poh = []
    for x in range(len(whse_poh)):
        str_whse_poh.append(str_poh[x]+whse_poh[x])
    return str_whse_poh
        


# Gets the forecast for a single Sku DC
def ecposo_(ecom_pd, sku, num_w_0_list):
    ecposo = []
    for x in num_w_0_list:
        try:        
            ecposovalue = ecom_pd.get_value(sku, str("PO"+x+' Planned'), takeable=False)
            if ecposovalue != ecposovalue:
                ecposovalue = 0
            ecposo.append(ecposovalue)
        except KeyError:
            ecposo.append(0)
    return ecposo

# Gets the forecast for a single Sku DC
def ecfc_(ecom_pd, sku, num_w_0_list):
    ecfc = []
    for x in num_w_0_list:
        try:
            ecfcvalue = ecom_pd.get_value(sku, str("EC_FC_"+x), takeable=False)
            ecfc.append(ecfcvalue) 
        except KeyError:
            ecfc.append(0)
    return ecfc

# Gets the forecast for a single Sku DC
def fc_(redcat_pd, sku_whse, num_w_0_list):
    fc = []
    for x in num_w_0_list:
        fcvalue = redcat_pd.get_value(sku_whse, str("FC"+x), takeable=False)
        fcvalue = int(fcvalue)
        fc.append(fcvalue)
    return fc

# Gets the block for a single Sku DC
def blocks_(redcat_pd, sku_whse, num_w_0_list,txt):
    fc = []
    for x in num_w_0_list:
        fcvalue = redcat_pd.get_value(sku_whse, str(txt+x), takeable=False)
        fcvalue = int(fcvalue)
        fc.append(fcvalue)
    return fc

# Gets the forecast for a single Sku DC
def fc_avg_(fc, wk_no):
    fc_avg = []
    
    for x in range(len(fc)):
        if x +wk_no> len(fc):
            y = len(fc)
        else:
            y=x+wk_no
        if x-y == 0:
            fcavgvalue = sum(fc[x : y])
        else:
            fcavgvalue = sum(fc[x : y])/(y-x)
        fc_avg.append(fcavgvalue)
    return fc_avg


# Get the WOS based on the average forecast
def wos_(fc_avg,poh):
    wos_whse =[]
    for x in range(len(fc_avg)):
        try:
            wosvalue = poh[x]/fc_avg[x]
        except ZeroDivisionError:
            wosvalue = 0
        except:
            wosvalue = 0
        wos_whse.append(wosvalue)
    return wos_whse

# Gets the DD for a single sku DC
def dd_(dd_pd, sku_whse, num_w_0_list):
    dd = []
    for x in num_w_0_list:
        try:
            ddvalue = float(dd_pd.get_value(sku_whse, str("DD_"+x), takeable=False))
            dd.append(ddvalue)
        except KeyError:
            dd.append(0)
    return dd

# Gets the POs for a single Sku DC
def po_(po_pd, sku_whse, num_w_0_list):
    po = []
    for x in num_w_0_list:
        try:
            povalue = po_pd.get_value(sku_whse, str("PO"+x), takeable=False)
            if povalue != povalue:
                povalue = 0
            po.append(povalue)
        except KeyError:
            po.append(0)
    return po

# Gets the index for the last PO
def last_po_(po):
    last_po=0
    for x in range(len(po)):
        if po[x] > 0:
            last_po = x
    return last_po
    
# Gets the StrSS for a single Sku DC
def strss_(strss_pd, sku_whse, num_w_0_list):
    strss = []
    for x in num_w_0_list:
        try:
            strssvalue = strss_pd.get_value(sku_whse, str("Store_SS"+x), takeable=False)
            strss.append(strssvalue)
        except KeyError:
            strss.append(0)
    return strss
        
# Gets the WhseSS for a single Sku DC    
def whsess_(whsess_pd, sku_whse, num_w_0_list):
    whsess = []
    for x in num_w_0_list:
        try:
            whsessvalue = whsess_pd.get_value(sku_whse, str("S"+x), takeable=False)
            whsess.append(whsessvalue) 
        except KeyError:
            whsess.append(0)
    return whsess
    

def shrink_(fc_avg, shrink_percent):
    shrink = []
    for x in range(len(fc_avg)):
        shrinkvalue = round(fc_avg[x]*shrink_percent,0)
        shrink.append(shrinkvalue)
    return shrink

#Returns the index where a suggested order should be placed. 
def need_index_(whse_poh,whsess,run_state, wks2run,lt):
    if run_state == 'present':
        need_index=lt
        need = False
        while need_index < wks2run and need == False:            
            if whse_poh[need_index]>=whsess[need_index]:
                need_index +=1
            elif whse_poh[need_index]<whsess[need_index]:
                need = True
        return need_index
    else:
        need_index=0
        need = False
        while need_index < wks2run and need == False:
            if whse_poh[need_index]>=whsess[need_index]:
                need_index+=1
            elif whse_poh[need_index]<whsess[need_index]:
                need = True
        return need_index

#Returns message
def message_(lt, need_index):
    if need_index == lt:
        message = 'At Lead Time'
    elif need_index <= (lt + 4):
        message = 'At LT +4'
    else:
        message = ''
    return message
    
# Order quanity logic            
def ord_qty_(need_index, whsess, whse_poh,fc_avg, fcl_20, fcl_40, fcl_40hq,mor_cost,dil_cost,moq,whse,mcq,wks2run):
    if whse == 953:
        cost  = mor_cost
    elif whse == 952:
        cost = dil_cost
    else:
        cost = dil_cost
    
    if need_index <= wks2run-4:
        wss = max(whsess[need_index],whsess[need_index+1],whsess[need_index+2],whsess[need_index+3])
    else:
        wss = whsess[need_index]
    
    ord_trueneed = wss-whse_poh[need_index] # changed here 

        
    if fcl_40hq >1 and fcl_40hq < 8*fc_avg[need_index]:
        ord_qty = fcl_40hq
    elif fcl_40 >1 and fcl_40 < 8*fc_avg[need_index]:
        ord_qty = fcl_40
    elif fcl_20 >1 and fcl_20 < 8*fc_avg[need_index]:
        ord_qty = fcl_20
    else:
        if fc_avg[need_index]<=0:
            ord_qty = fcl_20
        else:                
            ord_qty = round(max(moq,fc_avg[need_index]*4+ord_trueneed,0)/mcq,0)*mcq
    if ord_qty == 0:
        ord_qty = round(max(moq,fc_avg[need_index]*4+ord_trueneed,0)/mcq,0)*mcq
    if ord_qty*cost<1000:
        round((1000/cost/mcq)+.4999,0)*mcq
    return ord_qty
        
def header_creator_(wks2run,txt):
    header = ['Sku_whse']
    for x in range(wks2run):
        if x+1<10:
            headervalue = txt+'0'+str(x+1)
        else:
            headervalue =txt+str(x+1)
        header.append(headervalue)
    return header

def header_creator_3_(wks2run,txt):
    header = ['Sku_whse','Sku', 'Whse']
    for x in range(wks2run):
        if x+1<10:
            headervalue = txt+'0'+str(x+1)
        else:
            headervalue =txt+str(x+1)
        header.append(headervalue)
    return header
        
def whse_risk_wo_sugg_(whse_poh, dd,whsess):
    whse_risk_wo_sugg = []
    for x in range(len(dd)):
        if whse_poh[x] <= dd[x]:
            riskvalue = 'Very High'
        elif whse_poh[x] <= dd[x] + whsess[x]*0.5:
            riskvalue = 'High'
        elif whse_poh[x] <= dd[x] + whsess[x]:
            riskvalue = 'Moderate'
        else:
            riskvalue = 'Low'
        whse_risk_wo_sugg.append(riskvalue)
    return whse_risk_wo_sugg

def top_range_(wks2run,fc_avg,wos_max,whse_ss):
    top_range = []
    for x in range(wks2run):
        topvalue = fc_avg[x]*wos_max+whse_ss[x]
        top_range.append(topvalue)
    return top_range
        
        
        
        
        
        
        
        
        
        
        
        
        
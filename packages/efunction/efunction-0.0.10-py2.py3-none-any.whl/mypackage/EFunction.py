from IPython.core.magic import (register_line_magic,register_cell_magic)
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import (argument, magic_arguments,parse_argstring)
from IPython import get_ipython
import win32com.client
import pandas as pd
import numpy as np

@register_line_magic
@magic_arguments()
@argument('arg',  help='将数据导入到Excel，数据为dataframe格式数据')
def ef_set(arg):

    args = parse_argstring(ef_set, arg)
    data = eval(args.arg, get_ipython().user_ns, get_ipython().user_ns)
    pfD =None
    if isinstance(data, str):
        items = globals().items()
        
        for key,values in items:
            
            if data ==key:
                pfD = values
                break
    else:
        
        if isinstance(data, pd.DataFrame): # 数据框
            pfD = data
            columns = pfD.columns
            columns = columns.tolist()
            indic={}
            for i in range(0,len(columns)):
                if columns[i]  in indic:
                    indic[columns[i]] = indic[columns[i]] +1
                    columns[i] = str(columns[i])+str(indic[columns[i]]+1)
                else:
                    indic[columns[i]] = 0
                    
            pfD.columns = columns
            
            
        else:
            if isinstance(data, pd.Series):
                pfD = data
            else:
                try:
                    pfD =  pd.DataFrame(data) # 数据转化
                    columns = pfD.columns
                    new_list = ['结果数据_' + str(x) for x in columns.tolist()]
                    pfD.columns = new_list
                    
                except BaseException as Argument:
                    print( Argument)
                    return
    
    # 数据框格式处理
    StartRow = 1
    StartCol = 1
    excel = win32com.client.Dispatch("Excel.Application")
    ws = excel.ActiveSheet
    pfD = pfD.where(pd.notnull(pfD), None)
    dataResult = pfD.values
    
    if isinstance(pfD, pd.Series):
        resultData =np.ascontiguousarray(dataResult).tolist()
        resultData.insert(0,pfD.name)
        resultData = list(map(lambda el:[el], resultData))
        ws.Range(ws.Cells(StartRow,StartCol),# Cell to start the "paste"
                 ws.Cells(StartRow+len(pfD.index)-1,
                          StartCol)
                 ).Value =resultData
    else:
        resultData =np.ascontiguousarray(dataResult).tolist()
        resultData.insert(0,pfD.columns.tolist())
        ws.Range(ws.Cells(StartRow,StartCol),# Cell to start the "paste"
                 ws.Cells(StartRow+len(pfD.index),
                          StartCol+len(pfD.columns)-1)
                 ).Value =resultData
        
    
    
@register_line_magic
@magic_arguments()
@argument('--arg', '-a',default='all', help='将Excel之中表格导出到Python环境')
def ef_get(arg):
    args = parse_argstring(ef_get, arg)
    
    range = args.arg
    if range=='all':
        excel = win32com.client.Dispatch("Excel.Application")
        address = excel.ActiveSheet.UsedRange.address
        range ='$A$1:'+ address.split(':')[-1]
        data = excel.ActiveSheet.Range(range).Value
        pfD = pd.DataFrame(data[1:],columns=data[0])
        return pfD
    else:
    
        excel = win32com.client.Dispatch("Excel.Application")
        data = excel.ActiveSheet.Range(range).Value
        pfD = pd.DataFrame(data[1:],columns=data[0])
        return pfD
    

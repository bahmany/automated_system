hamkaraan_factors = """
 SELECT 
 fi.[VchItmId] as [InvoiceItemID],
 fi.[VchHdrRef] as [InvoiceItemInvoiceRef],
 p.PartCode as [InvoiceItemProductNumber], 
 SUBSTRING(p.PartCode, 1, 2) as [sharh],
 SUBSTRING(p.PartCode, 3, 1) as [BP],
 SUBSTRING(p.PartCode, 4, 1) as [TEMPER],
 SUBSTRING(p.PartCode, 5, 1) as [sath],
 SUBSTRING(p.PartCode, 6, 2) as [zekhamat],
 SUBSTRING(p.PartCode, 8, 3) as [arz],
 SUBSTRING(p.PartCode, 11, 1) as [darajeh],
 SUBSTRING(p.PartCode, 12, 3) as [tool],
 SUBSTRING(p.PartCode, 6, 2)+'-'+SUBSTRING(p.PartCode, 8, 3) as [zekhamat_arz],
 SUBSTRING(p.PartCode, 6, 2)+'-'+SUBSTRING(p.PartCode, 8, 3)+'-'+SUBSTRING(p.PartCode, 12, 3) as [zekhamat_arz_tool],
 SUBSTRING(p.PartCode, 6, 2)+'-'+SUBSTRING(p.PartCode, 8, 3)+'-'+SUBSTRING(p.PartCode, 12, 3)+'-'+SUBSTRING(p.PartCode, 4, 1)+'-'+SUBSTRING(p.PartCode, 1, 2) as [zekhamat_arz_tool_temper_keshvar],
p.[PartName] as [InvoiceItemProductName],
 dl.Title  as [InvoiceItemRecipient],
cs.CstmrCode as [InvoiceItemRecipientCode],
fi.vchdate as [InvoiceItemDeliveryDate],

 u.UnitName as [InvoiceItemTotalPrice], 
 fi.Qty as [InvoiceItemQuantity],
 fi.UnitPrice as [InvoiceItemFee],  
 fi.qty*fi.unitprice as  [InvoiceItemTotalPrice],
 'ریال' as [InvoiceItemCurrencyTitle]



FROM       sle.SLEFactItm fi     
                         INNER JOIN  sle.SLECstmrs cs ON fi.CstmrRef=cs.cstmrcode
						 INNER JOIN   Acc.DL dl on dl.AccNum=cs.cstmrcode 
						 INNER JOIN inv.Part p ON fi.PartRef = p.Serial 
						 INNER JOIN inv.MUnit u ON fi.MUnitRef = u.Serial  
WHERE        (fi.[Status] <> 3) and fi.year <= 99

order by fi.[VchItmId]"""

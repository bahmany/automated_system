rahkaraan_factors = """
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (99000) vrp.[InvoiceItemID]
      ,vrp.[InvoiceItemInvoiceRef]
      ,vrp.[InvoiceItemProductNumber],
	   SUBSTRING(vrp.InvoiceItemProductNumber, 1, 2) as [sharh],
 SUBSTRING(vrp.InvoiceItemProductNumber, 3, 1) as [BP],
 SUBSTRING(vrp.InvoiceItemProductNumber, 4, 1) as [TEMPER],
 SUBSTRING(vrp.InvoiceItemProductNumber, 5, 1) as [sath],
 SUBSTRING(vrp.InvoiceItemProductNumber, 6, 2) as [zekhamat],
 SUBSTRING(vrp.InvoiceItemProductNumber, 8, 3) as [arz],
 SUBSTRING(vrp.InvoiceItemProductNumber, 11, 1) as [darajeh],
 SUBSTRING(vrp.InvoiceItemProductNumber, 12, 3) as [tool],
 SUBSTRING(vrp.InvoiceItemProductNumber, 6, 2)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 8, 3) as [zekhamat_arz],
 SUBSTRING(vrp.InvoiceItemProductNumber, 6, 2)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 8, 3)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 12, 3) as [zekhamat_arz_tool],
 SUBSTRING(vrp.InvoiceItemProductNumber, 6, 2)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 8, 3)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 12, 3)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 4, 1)+'-'+SUBSTRING(vrp.InvoiceItemProductNumber, 1, 2) as [zekhamat_arz_tool_temper_keshvar],
       vrp.[InvoiceItemProductName],
       vrp.[InvoiceItemDeliveryDate],
	  vrp.[InvoiceItemRecipient]
      ,vrp.[InvoiceItemUnitName]
      ,vrp.[InvoiceItemQuantity]
      ,vrp.[InvoiceItemFee]
      ,vrp.[InvoiceItemTotalPrice]
      ,vrp.[InvoiceItemCurrencyTitle]

  FROM [RahkaranDB].[SLS3].[vwRPTSalesNewInvoiceItem] as vrp
"""
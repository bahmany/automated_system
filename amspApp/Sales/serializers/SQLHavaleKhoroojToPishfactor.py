havaleh_khrooj_sql = lambda referenceNumber: """


select top 3000
	ordi.OrderRef as OrderItemOrderID,
	ordi.OrderItemID,
	ordi.RowNumber as OrderItemRowNumber,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then 'درخواست فروش'
		when ISNULL(Q.QuotationID, 0) != 0 then 'پیش فاکتور'
		else 'نامشخص'
	end as OrderItemSourceType,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then SR.Number
		when ISNULL(Q.QuotationID, 0) != 0 then Q.Number
		else 'نامشخص'
	end as OrderItemSourceNumber,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then SR.Number
		when ISNULL(Q.QuotationID, 0) != 0 then cast(Q.QuotationID as nvarchar(100))
		else 'نامشخص'
	end as OrderItemSourceNumberRef,
	pat.TechnicalSpecification as OrderItemPartTechnicalSpecification,--مشخصه فنی
	majorun.Name as OrderItemMajorUnitName,--واحد سنجش اصلی
	un.Name as OrderItemUnitName,--واحد سنجش
	priceBaseUnit.Name AS OrderItemPriceBaseUnitName,--واحد سنجش مرجع
	prd.Number as OrderItemProductNumber,
	prd.Name as OrderItemProductName,
	ordi.Quantity as OrderItemQuantity,
	ordi.PriceBaseFee as OrderItemPriceBaseFee,
	ordi.Fee as OrderItemFee,
	ordi.Price as OrderItemPrice,
	ordi.AdditionAmount as OrderItemAdditionAmount,
	ordi.ReductionAmount as OrderItemReductionAmount,
	ordi.SettlementRespite as OrderItemSettlementRespite,-- مدت تسویه
	case 
		when ordi.State = 1 then 'ثبت شده'
		when ordi.State = 2 then 'تاییده شده'
		when ordi.State = 3 then 'در حال استفاده'
		when ordi.State = 4 then 'بسته شده'
		when ordi.State = 5 then 'معلق'
		when ordi.State = 6 then 'باطل شده'
		when ordi.State = 7 then 'مسدود'
	end as OrderItemState,
	sa.Code as OrderItemSalesAreaCode,
	sa.Name as OrderItemSalesAreaName,
	--sch.Code as OrderItemSalesChanelCode,
	--sch.Name as OrderItemSalesChanelName,
	--div.Code as OrderItemDivisionCode,
	--div.Name as OrderItemDivisionName,
	--so.Code as OrderItemSalesOrganizationCode,
	--so.Name as OrderItemSalesOrganizationName,
	(ordi.InitialQuantity - ordi.Quantity) as OrderItemBlockedQuantity,
	ordi.Description as OrderItemDescription,
	ordiDeliveryAddress.Details as OrderItemDeliveryAddress,--آدرس محل تحویل
	case 
		when ISNULL(province.RegionalDivisionID, 0) != 0 then province.Name
	end as OrderItemDeliveryAddressProvinceName,--استان محل تحویل
	case 
		when ISNULL(city1.RegionalDivisionID, 0) != 0 then city1.Name
	end as OrderItemDeliveryAddressCity1Name,--شهر محل تحویل
	case 
		when ISNULL(city2.RegionalDivisionID, 0) != 0 then city2.Name
	end as OrderItemDeliveryAddressCity2Name,--شهرستان محل تحویل
	case
		when ordi.RecipientType = 1
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientCustomer.Number, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
		when ordi.RecipientType = 2
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientBroker.Number, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
		when ordi.RecipientType = 4
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientCarrier.Code, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
	end as OrderItemRecipient,--تحویل گیرنده
	shPoint.Code as OrderItemShippingPointCode,
	shPoint.Name as OrderItemShippingPointName,
	loPoint.Code as OrderItemLoadingPointCode,
	loPoint.Name as OrderItemLoadingPointName
	from SLS3.OrderItem as ordi 
	
	INNER JOIN SYS3.EntityLookup OIEL 
		ON OIEL.EntityName = 'SystemGroup.Sales.OrderManagement,OrderItem'
		
	INNER JOIN SYS3.EntityLookup QIEL 
		ON QIEL.EntityName = 'SystemGroup.Sales.OrderManagement,QuotationItem'
		
	--LEFT JOIN SYS3.EntityLookup SSIEL 
	--	ON SSIEL.EntityName = 'SystemGroup.Sales.Brokerage,SalesStatementItem'		
		
	INNER JOIN SYS3.EntityLookup SRIEL
		ON SRIEL.EntityName = 'SystemGroup.Sales.OrderManagement,SaleRequestItem'
	
	LEFT JOIN SYS3.EntityRelation AS QI2OIER 
		ON QI2OIER.SourceType = QIEL.Code 
		AND QI2OIER.TargetType = OIEL.Code 
		AND QI2OIER.TargetRef = ordi.OrderItemID		
	LEFT JOIN SLS3.QuotationItem AS QI 
		ON QI2OIER.SourceRef = QI.QuotationItemID
	LEFT JOIN SLS3.Quotation AS Q 
		ON QI.QuotationRef = Q.QuotationID 
		
	LEFT JOIN SYS3.EntityRelation AS SRI2OIER 
		ON SRI2OIER.SourceType = SRIEL.Code 
		AND SRI2OIER.TargetType = OIEL.Code 
		AND SRI2OIER.TargetRef = ordi.OrderItemID		
	LEFT JOIN SLS3.SaleRequestItem AS SRI 
		ON SRI2OIER.SourceRef = SRI.SaleRequestItemID
	LEFT JOIN SLS3.SaleRequest AS SR
		ON SRI.SaleRequestRef = SR.SaleRequestID
		
	--LEFT JOIN SYS3.EntityRelation AS SSI2OIER 
	--	ON SSI2OIER.SourceType = SSIEL.Code 
	--	AND SSI2OIER.TargetType = OIEL.Code 
	--	AND SSI2OIER.TargetRef = ordi.OrderItemID		
	--LEFT JOIN SLS3.SalesStatementItem AS SSI 
	--	ON SSI2OIER.SourceRef = SSI.SalesStatementItemID
	--LEFT JOIN SLS3.SalesStatement AS SS
		--ON SSI.SalesStatementRef = SS.SalesStatementID
	

	
	inner join SLS3.Product as prd on ordi.ProductRef = prd.ProductID
	left join LGS3.Part as pat on prd.PartRef = pat.PartID
	left join gnr3.Unit as majorun on pat.MajorUnitRef = majorun.UnitID
	inner join gnr3.Unit as un on ordi.ProductUnitRef = un.UnitID
	inner join gnr3.Unit as priceBaseUnit on ordi.PriceBaseUnitRef = priceBaseUnit.UnitID
	inner join SLS3.SalesArea as sa on ordi.SalesAreaRef = sa.SalesAreaID
	--inner join SLS3.SalesChannel as sch on sa.SalesChannelRef = sch.SalesChannelID
	--inner join SLS3.Division as div on sa.DivisionRef = div.DivisionID
	--inner join SLS3.SalesOrganization as so on sa.SalesOrganizationRef = so.SalesOrganizationID
	
	left join gnr3.Address as ordiDeliveryAddress on ordi.BaseDeliveryAddressRef = ordiDeliveryAddress.AddressID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 2
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as province on ordiDeliveryAddress.RegionalDivisionRef = province.RegionalDivisionID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 3 
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as city1 on ordiDeliveryAddress.RegionalDivisionRef = city1.RegionalDivisionID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 4
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as city2 on ordiDeliveryAddress.RegionalDivisionRef = city2.RegionalDivisionID
	left join gnr3.Party as ordiParty on ordi.RecipientPartyRef = ordiParty.PartyID
	left join SLS3.Customer as ordiRecipientCustomer on ordi.RecipientRef = ordiRecipientCustomer.CustomerID
	left join SLS3.Broker as ordiRecipientBroker on ordi.RecipientRef = ordiRecipientBroker.BrokerID
	left join LGS3.Carrier as ordiRecipientCarrier on ordi.RecipientRef = ordiRecipientCarrier.CarrierID
	left join lgs3.ShippingPoint shPoint on ordi.ShippingPointRef = shPoint.ShippingPointID
	left join lgs3.LoadingPoint as loPoint on ordi.LoadingPointRef = loPoint.LoadingPointID
	where 
	ordi.State != 6
	and 
	(case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then SR.Number
		when ISNULL(Q.QuotationID, 0) != 0 then cast(Q.QuotationID as nvarchar(100))
		else 'نامشخص'
	end ) = '%s'
""" % (referenceNumber)
havaleh_khrooj_sql_order_id = lambda orderID: """


select top 10000
	ordi.OrderRef as OrderItemOrderID,
	ordi.OrderItemID,
	ordi.RowNumber as OrderItemRowNumber,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then 'درخواست فروش'
		when ISNULL(Q.QuotationID, 0) != 0 then 'پیش فاکتور'
		else 'نامشخص'
	end as OrderItemSourceType,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then SR.Number
		when ISNULL(Q.QuotationID, 0) != 0 then Q.Number
		else 'نامشخص'
	end as OrderItemSourceNumber,
	case 
		when ISNULL(SR.SaleRequestID, 0) != 0 then SR.Number
		when ISNULL(Q.QuotationID, 0) != 0 then cast(Q.QuotationID as nvarchar(100))
		else 'نامشخص'
	end as OrderItemSourceNumberRef,
	pat.TechnicalSpecification as OrderItemPartTechnicalSpecification,--مشخصه فنی
	majorun.Name as OrderItemMajorUnitName,--واحد سنجش اصلی
	un.Name as OrderItemUnitName,--واحد سنجش
	priceBaseUnit.Name AS OrderItemPriceBaseUnitName,--واحد سنجش مرجع
	prd.Number as OrderItemProductNumber,
	prd.Name as OrderItemProductName,
	ordi.Quantity as OrderItemQuantity,
	ordi.PriceBaseFee as OrderItemPriceBaseFee,
	ordi.Fee as OrderItemFee,
	ordi.Price as OrderItemPrice,
	ordi.AdditionAmount as OrderItemAdditionAmount,
	ordi.ReductionAmount as OrderItemReductionAmount,
	ordi.SettlementRespite as OrderItemSettlementRespite,-- مدت تسویه
	case 
		when ordi.State = 1 then 'ثبت شده'
		when ordi.State = 2 then 'تاییده شده'
		when ordi.State = 3 then 'در حال استفاده'
		when ordi.State = 4 then 'بسته شده'
		when ordi.State = 5 then 'معلق'
		when ordi.State = 6 then 'باطل شده'
		when ordi.State = 7 then 'مسدود'
	end as OrderItemState,
	sa.Code as OrderItemSalesAreaCode,
	sa.Name as OrderItemSalesAreaName,
	--sch.Code as OrderItemSalesChanelCode,
	--sch.Name as OrderItemSalesChanelName,
	--div.Code as OrderItemDivisionCode,
	--div.Name as OrderItemDivisionName,
	--so.Code as OrderItemSalesOrganizationCode,
	--so.Name as OrderItemSalesOrganizationName,
	(ordi.InitialQuantity - ordi.Quantity) as OrderItemBlockedQuantity,
	ordi.Description as OrderItemDescription,
	ordiDeliveryAddress.Details as OrderItemDeliveryAddress,--آدرس محل تحویل
	case 
		when ISNULL(province.RegionalDivisionID, 0) != 0 then province.Name
	end as OrderItemDeliveryAddressProvinceName,--استان محل تحویل
	case 
		when ISNULL(city1.RegionalDivisionID, 0) != 0 then city1.Name
	end as OrderItemDeliveryAddressCity1Name,--شهر محل تحویل
	case 
		when ISNULL(city2.RegionalDivisionID, 0) != 0 then city2.Name
	end as OrderItemDeliveryAddressCity2Name,--شهرستان محل تحویل
	case
		when ordi.RecipientType = 1
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientCustomer.Number, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
		when ordi.RecipientType = 2
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientBroker.Number, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
		when ordi.RecipientType = 4
			then
				case
					when ISNULL(ordiParty.PartyID, 0) != 0 then ISNULL(ordiRecipientCarrier.Code, '') + '/' + ISNULL(ordiParty.CompanyName, '') + ' ' + ISNULL(ordiParty.FirstName, '') + ' ' + ISNULL(ordiParty.LastName, '')
				end
	end as OrderItemRecipient,--تحویل گیرنده
	shPoint.Code as OrderItemShippingPointCode,
	shPoint.Name as OrderItemShippingPointName,
	loPoint.Code as OrderItemLoadingPointCode,
	loPoint.Name as OrderItemLoadingPointName
	from SLS3.OrderItem as ordi 
	
	INNER JOIN SYS3.EntityLookup OIEL 
		ON OIEL.EntityName = 'SystemGroup.Sales.OrderManagement,OrderItem'
		
	INNER JOIN SYS3.EntityLookup QIEL 
		ON QIEL.EntityName = 'SystemGroup.Sales.OrderManagement,QuotationItem'
		
	--LEFT JOIN SYS3.EntityLookup SSIEL 
	--	ON SSIEL.EntityName = 'SystemGroup.Sales.Brokerage,SalesStatementItem'		
		
	INNER JOIN SYS3.EntityLookup SRIEL
		ON SRIEL.EntityName = 'SystemGroup.Sales.OrderManagement,SaleRequestItem'
	
	LEFT JOIN SYS3.EntityRelation AS QI2OIER 
		ON QI2OIER.SourceType = QIEL.Code 
		AND QI2OIER.TargetType = OIEL.Code 
		AND QI2OIER.TargetRef = ordi.OrderItemID		
	LEFT JOIN SLS3.QuotationItem AS QI 
		ON QI2OIER.SourceRef = QI.QuotationItemID
	LEFT JOIN SLS3.Quotation AS Q 
		ON QI.QuotationRef = Q.QuotationID 
		
	LEFT JOIN SYS3.EntityRelation AS SRI2OIER 
		ON SRI2OIER.SourceType = SRIEL.Code 
		AND SRI2OIER.TargetType = OIEL.Code 
		AND SRI2OIER.TargetRef = ordi.OrderItemID		
	LEFT JOIN SLS3.SaleRequestItem AS SRI 
		ON SRI2OIER.SourceRef = SRI.SaleRequestItemID
	LEFT JOIN SLS3.SaleRequest AS SR
		ON SRI.SaleRequestRef = SR.SaleRequestID
		
	--LEFT JOIN SYS3.EntityRelation AS SSI2OIER 
	--	ON SSI2OIER.SourceType = SSIEL.Code 
	--	AND SSI2OIER.TargetType = OIEL.Code 
	--	AND SSI2OIER.TargetRef = ordi.OrderItemID		
	--LEFT JOIN SLS3.SalesStatementItem AS SSI 
	--	ON SSI2OIER.SourceRef = SSI.SalesStatementItemID
	--LEFT JOIN SLS3.SalesStatement AS SS
		--ON SSI.SalesStatementRef = SS.SalesStatementID
	

	
	inner join SLS3.Product as prd on ordi.ProductRef = prd.ProductID
	left join LGS3.Part as pat on prd.PartRef = pat.PartID
	left join gnr3.Unit as majorun on pat.MajorUnitRef = majorun.UnitID
	inner join gnr3.Unit as un on ordi.ProductUnitRef = un.UnitID
	inner join gnr3.Unit as priceBaseUnit on ordi.PriceBaseUnitRef = priceBaseUnit.UnitID
	inner join SLS3.SalesArea as sa on ordi.SalesAreaRef = sa.SalesAreaID
	--inner join SLS3.SalesChannel as sch on sa.SalesChannelRef = sch.SalesChannelID
	--inner join SLS3.Division as div on sa.DivisionRef = div.DivisionID
	--inner join SLS3.SalesOrganization as so on sa.SalesOrganizationRef = so.SalesOrganizationID
	
	left join gnr3.Address as ordiDeliveryAddress on ordi.BaseDeliveryAddressRef = ordiDeliveryAddress.AddressID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 2
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as province on ordiDeliveryAddress.RegionalDivisionRef = province.RegionalDivisionID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 3 
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as city1 on ordiDeliveryAddress.RegionalDivisionRef = city1.RegionalDivisionID
	left join
	(
		select
				T.RegionalDivisionID, 
				P.Name
			from (
				select  rd.RegionalDivisionID , MIN(prd.[LEFT]) MinPrd
				from GNR3.RegionalDivision as rd 
				INNER JOIN gnr3.RegionalDivision as prd 
					on rd.[Left] >= prd.[Left] 
					and rd.[Left] <= prd.[Right]
				where 
					prd.Type = 4
				group by rd.RegionalDivisionID ) T
			INNER JOIN GNR3.RegionalDivision P ON
				T.MinPrd = P.[Left]
	) as city2 on ordiDeliveryAddress.RegionalDivisionRef = city2.RegionalDivisionID
	left join gnr3.Party as ordiParty on ordi.RecipientPartyRef = ordiParty.PartyID
	left join SLS3.Customer as ordiRecipientCustomer on ordi.RecipientRef = ordiRecipientCustomer.CustomerID
	left join SLS3.Broker as ordiRecipientBroker on ordi.RecipientRef = ordiRecipientBroker.BrokerID
	left join LGS3.Carrier as ordiRecipientCarrier on ordi.RecipientRef = ordiRecipientCarrier.CarrierID
	left join lgs3.ShippingPoint shPoint on ordi.ShippingPointRef = shPoint.ShippingPointID
	left join lgs3.LoadingPoint as loPoint on ordi.LoadingPointRef = loPoint.LoadingPointID
	where 
	ordi.State != 6
	and 
	ordi.OrderItemID = %s
""" % (orderID)

get_qotation_by_id = lambda quotationid: """
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (10000) [QuotationID]
      ,[QuotationNumber]
      ,[QuotationDate]
      ,[QuotationNetPrice]
      ,[QuotationPrice]
      ,[QuotationAdditionAmount]
      ,[QuotationReductionAmount]
      ,[SettlementRespite]
      ,[QuotationExpirationDate]
      ,[QuotationCreatorUserID]
      ,[QuotationCreatorUserName]
      ,[QuotationAcceptorUserID]
      ,[QuotationAcceptorUserName]
      ,[QuotationFiscalYear]
      ,[QuotationCurrencyID]
      ,[QuotationCurrencyTitle]
      ,[QuotationState]
      ,[QuotationStateTitle]
      ,[QuotationSalesOfficeID]
      ,[QuotationSalesOfficeCode]
      ,[QuotationSalesOfficeName]
      ,[QuotationSalesAreaCode]
      ,[QuotationSalesAreaName]
      ,[QuotationCustomerNumber]
      ,[QuotationCustomerName]
      ,[QuotationCustomerEconomicCode]
      ,[QuotationCustomerMobile]
      ,[QuotationCustomerRegistrationCode]
      ,[QuotationCustomerEmail]
      ,[QuotationCustomerTypeCode]
      ,[QuotationCustomerType]
      ,[QuotationCustomerAddress]
      ,[QuotationCustomerProvinceName]
      ,[QuotationCustomerCity1Name]
      ,[QuotationCustomerCity2Name]
      ,[QuotationCustomerPostalCode]
      ,[QuotationCustomerPhoneNumber]
      ,[QuotationCustomerFaxNumber]
      ,[QuotationOneTimeCustomerID]
      ,[QuotationOneTimeCustomerNumber]
      ,[QuotationOneTimeCustomerPhoneNumber]
      ,[QuotationOneTimeCustomerName]
      ,[QuotationOneTimeCustomerAddress]
      ,[QuotationBrokerID]
      ,[QuotationBrokerNumber]
      ,[QuotationBrokerName]
      ,[QuotationSalesType]
      ,[QuotationPayerAccountNumber]
      ,[QuotationPayerAccountName]
      ,[QuotationCustomerDL]
      ,[QuotationBrokerDL]
      ,[QuotationRecipientNumber]
      ,[QuotationRecipientName]
      ,[QuotationDeliveryAddress]
      ,[QuotationPlantNumber]
      ,[QuotationPlantName]
      ,[QuotationPayer]
      ,[QuotationCompanyName]
      ,[QuotationCompanyEconomicCode]
      ,[QuotationCompanyRegistrationCode]
      ,[QuotationCompanyEmail]
      ,[QuotationCompanyAddress]
      ,[QuotationCompanyProvince]
      ,[QuotationCompanyCity1]
      ,[QuotationCompanyCity2]
      ,[QuotationCompanyPostalCode]
      ,[QuotationCompanyPhoneNumber]
      ,[QuotationCompanyFaxNumber]
      ,[QuotationNoteDate]
      ,[QuotationNoteTitle]
      ,[QuotationNoteDescription]
  FROM [RahkaranDB].[SLS3].[vwRptSalesNewQuotation] 
  where QuotationID = %s
""" % (quotationid)

get_qotation_items_by_id = lambda quotationid: """
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (10000) [QuotationItemQuotationID]
      ,[QuotationItemID]
      ,[QuotationItemRowNumber]
      ,[QuotationItemSourceType]
      ,[QuotationItemSourceNumber]
      ,[QuotationItemPartTechnicalSpecification]
      ,[QuotationItemMajorUnitName]
      ,[QuotationItemUnitName]
      ,[QuotationItemPriceBaseUnitName]
      ,[QuotationItemProductNumber]
      ,[QuotationItemProductName]
      ,[QuotationItemQuantity]
      ,[QuotationItemPriceBaseFee]
      ,[QuotationItemFee]
      ,[QuotationItemPrice]
      ,[QuotationItemAdditionAmount]
      ,[QuotationItemReductionAmount]
      ,[QuotationItemSettlementRespite]
      ,[QuotationItemState]
      ,[QuotationItemSalesAreaCode]
      ,[QuotationItemSalesAreaName]
      ,[QuotationItemBlockedQuantity]
      ,[QuotationItemDescription]
      ,[QuotationItemDeliveryAddress]
      ,[QuotationItemDeliveryAddressProvinceName]
      ,[QuotationItemDeliveryAddressCity1Name]
      ,[QuotationItemDeliveryAddressCity2Name]
      ,[QuotationItemRecipient]
      ,[QuotationItemShippingPointCode]
      ,[QuotationItemShippingPointName]
  FROM [RahkaranDB].[SLS3].[vwRptSalesNewQuotationItem]
  where [QuotationItemQuotationID] = %s
""" % (quotationid)

get_qotation_desc_by_id = lambda quotationid: """
SELECT [t0].[CustomerRef], [t0].[QuotationID] AS [ID], 
[t0].[Number], [t0].[State], [t0].[Price], [t0].[AdditionAmount], [t0].[ReductionAmount], [t0].[NetPrice], [t0].[CurrencyRef], [t0].[Date], 
[t0].[SalesOfficeRef], [t0].[CompanyRef], [t0].[SalesAreaRef], [t0].[PayerType], [t0].[RecipientType], [t0].[RecipientRef], [t0].[BrokerRef], 
[t0].[AgentRef], [t0].[ShippingPointRef], [t0].[DeliveryAddressRef], [t0].[ExpirationDate], [t0].[Creator], [t0].[CreationDate], [t0].[LastModifier], 
[t0].[LastModificationDate], [t0].[Version], [t0].[DeliveryAddressType], [t0].[OneTimeCustomerRef], [t0].[CustomerType], [t0].[PlantRef], [t0].[CalculationDate], 
[t0].[EffectiveNetPrice], [t0].[PayerAccountRef], [t0].[RecipientPartyRef], [t0].[BranchRef], [t0].[FiscalYearRef], [t0].[PaymentAgreementRef], [t0].[SalesTypeRef], 
[t0].[InventoryRef], [t0].[Description], [t0].[CustomerAcceptance], [t0].[PrePaidAmount], [t0].[ContractRef], [t0].[PolicyCalculationDateType], [t0].[IncludedPolicies], 
[t0].[ExcludedPolicies], [t0].[SettlementRespite], [t0].[IsSettlementRespiteCalculated], [t0].[OperationalCurrencyExchangeRateRef], [t0].[OperationalCurrencyExchangeRate], 
[t0].[OperationalCurrencyExchangeRateIsReversed], [t1].[QuotationPolicyResultID] AS [ID2], [t1].[QuotationRef], [t1].[BusinessPolicyRef], 
 (
    SELECT COUNT(*)
    FROM [SLS3].[QuotationPolicyResult] AS [t2]
    WHERE [t2].[QuotationRef] = [t0].[QuotationID]
    ) AS [value2]
FROM [SLS3].[Quotation] AS [t0]
LEFT OUTER JOIN [SLS3].[QuotationPolicyResult] AS [t1] ON [t1].[QuotationRef] = [t0].[QuotationID]
WHERE ([t0].[QuotationID] =%s)
ORDER BY [t0].[QuotationID], [t1].[QuotationPolicyResultID]
""" % (quotationid)

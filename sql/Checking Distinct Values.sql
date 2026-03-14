Select Gender, Count(Gender) as TotalCount,
Count(Gender) * 100.0/ (Select Count(*) from stg_Churn) as Percentage
From stg_Churn
Group By Gender


SELECT Contract, Count(Contract) as TotalCount,
Count(Contract)*100.0/(Select Count(*) from stg_Churn) as Percentage
from stg_Churn
Group By Contract


SELECT Customer_Status, Count(Customer_Status) as TotalCount, Sum(Total_Revenue) as TotalRev,
Sum(Total_Revenue) *100/ (Select sum(Total_Revenue) from stg_Churn)  as RevPercentage
from stg_Churn
Group by Customer_Status


SELECT State, Count(State) as TotalCount,
Count(State)  * 100.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by State
Order by Percentage desc


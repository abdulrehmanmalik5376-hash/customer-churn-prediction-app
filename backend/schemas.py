from pydantic import BaseModel


class Customer(BaseModel):

    Gender: int
    Senior_Citizen: int
    Partner: int
    Dependents: int
    Tenure_Months: int
    Phone_Service: int
    Multiple_Lines: int
    Internet_Service: int
    Online_Security: int
    Online_Backup: int
    Device_Protection: int
    Tech_Support: int
    Streaming_TV: int
    Streaming_Movies: int
    Contract: int
    Paperless_Billing: int
    Payment_Method: int
    Monthly_Charges: float
    Total_Charges: float
# Helper function to calculate the commission
def calc_commission(sale_price):
    if sale_price < 100000:
        commission = 0.1*sale_price
    elif 100000 <= sale_price < 200000:
        commission = 0.075*sale_price
    elif 200000 <= sale_price < 500000:
        commission = 0.06*sale_price
    elif 500000 <= sale_price < 1000000:
        commission = 0.05*sale_price
    elif sale_price >= 1000000:
        commission = 0.04*sale_price
    return commission

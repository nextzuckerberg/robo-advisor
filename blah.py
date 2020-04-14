
def reccommendation(recent_low, latest_closing):

    rec = str
    reason = str    

    if float(recent_low)/float(latest_closing) >= 0.8:
        
        reason = "The stock is most likely undervalued. This is because the latest close price is 20% or closer from the 52 week low." #provi
    else:
        
        reason = "The stock is most likely overvalued. This is because the latest close price is more than 20% away from the 52 week low." #provide some more explanation
   
    
    return reason


print(reccommendation(10,5))





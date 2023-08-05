
Volkeno Paydunya Gateway Py
===
Integrate paydunya quickly in your backend

Detailed documentation is in the "docs" directory.

## Quick start

1. Install the module:

         pip install volkeno_paydunya_gateway_py

2. EXAMPLE OF PAYMENT WITH REDIRECTION

   ### Import module

         from volkeno_paydunya_gateway_py.job import PaymentAR
   ### Initialize payment
            MASTER_KEY = MASTER_KEY_OF_YOUR_APP
            MASTER_KEY = PRIVATE_KEY_OF_YOUR_APP
            PAYDUNYA_TOKEN = TOKEN_KEY
            STORE = YOUR APP NAME or your STORE NAME

            payment = Payment(MASTER_KEY,MASTER_KEY,PAYDUNYA_TOKEN,STORE)
   ### Create an transaction:
      
            payment.payment_create(total_amount,return_url,return_url_parameter)

      ## Example

            total_amount = str(total)
            return_url = YOUR_API_URL+ "/api/payment-status"
            // You can add one parameter or many parameter in your return url
            #One parameter
                  return_url_parameter = "/?seller=2"
            #Many parameter
                  return_url_parameter = "/?seller=2&amount=400"
            
            successful, result = payment.payment_create(total_amount,return_url,return_url_parameter)
            if successful:
                  if 'response_text' in result:
                        url=result['response_text']
                        return Response({"url":url},status=200)
                  return Response({"message":result},status=400)
            else:
                  return Response({"message":result},status=400)

   ### Check if transaction is done or not 
            successful,response = payment.payment_result(token)
            if successful:
                  //Do this
                  else:
                  //Do that

import requests
import json

class Snapdeal:
    ## Constructor
    def __init__(self, userName, userPassword):
        self.userName = userName
        self.userPassword = userPassword
        ## create a session to POST data
        self.session = requests.Session()
        self.header = {'Content-Type': 'application/json;charset: utf-8'}

    ## Function to Log in to the API server 
    def userLogin(self):
        url = 'https://mobileapi.snapdeal.com/service/user/login/v2/loginWithMobile/'
        ##Login data
        json_data = {
            "password": self.userPassword,
            "requestProtocol": "PROTOCOL_JSON",
            "apiKey": "snapdeal",
            "responseProtocol": "PROTOCOL_JSON",
            'mobileNumber': self.userName
        }
        response = self.session.post(url, json= json_data, headers=self.header )
        return response

    ## Function to set product details (in this case the the details are fixed)
    ## and add the product to the cart
    def addtoCart(self,login_token):             
        pinCode = "201306"
        vendorCode = 'S667db'
        supc = 'SDL044719313'
        catalogId = 643083255133
        qty = 1

        url = 'https://mobileapi.snapdeal.com/service/nativeCart/v2/insertItemToCart'

        ##Product details
        cart_data ={"pincode": pinCode,
                    "items": [{"vendorCode": vendorCode,
                               "supc": supc,
                               "catalogId": catalogId,
                               "quantity": qty}
                              ],
                    "loginToken": login_token
                    }
        cart_response = self.session.post(url, json = cart_data, headers = self.header)
        return cart_response
        
    ## Function to Sign out from the API server.
    def logOut(self,login_token):
        signouturl = 'https://mobileapi.snapdeal.com/service/signout/'
        signout_data = {'loginToken': login_token}
        lout_response = self.session.post(signouturl,json=signout_data, headers = self.header )
        return lout_response
            
def main():
        print("---"*15)
        ##Enter the details
        userName = input('Enter phone number : ')
        userPassword = input('Enter the password : ')
        print("---"*15)
        # Initializing the Snapdeal class
        item = Snapdeal(userName, userPassword)
        print("---"*15)
        ##Login 
        login_response = item.userLogin()   

        ##Validation of Login Session
        if login_response.json().get('status') == 'SUCCESS':
            print('You are Successfully Logged in..')
        else:
            print('Something went wrong\n')
            print(login_response.json().get('exceptions')[0].get('errorMessage'))
        ##Login token received from successfully login
        login_token =login_response.headers.get('Login-Token')
        print("---"*15)
        ##AddtoCart 
        cart_response = item.addtoCart(login_token)

        ##Validation of AddtoCart Session
        if cart_response.json().get('successful'):
            print((cart_response.json().get('messages')))
        else:
            print('Product was not added, something went wrong')
        print("---"*15)
        ##logOut
        logout_response = item.logOut(login_token)

        ##Validatation of Logout Session
        if logout_response.json().get('status') == 'true':
            print('You are Successfully Logged out..')
        else:
            print(logout_response.json().get('code'))
        print("---"*15)
        
if __name__ == '__main__':
    main()            

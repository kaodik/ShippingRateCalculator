from datetime import datetime, timezone
import tkinter as tk
from tkinter import ttk
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NSUsername = os.getenv('NSUsername')
NSPassword = os.getenv('NSPassword')
UPSUsername = os.getenv('UPSUsername')
UPSPassword = os.getenv('UPSPassword')
refreashToken = os.getenv('refreashToken')
getCodeURL = os.getenv('getCodeURL')
getCodeRedirectURL = os.getenv("getCodeRedirectURL")
NSCompanyid = os.getenv('NSCompanyid')
CompanyName = os.getenv('CompanyName')
UPSShippingNumber = os.getenv('UPSShippingNumber')
AccessLicenseNumber = os.getenv('AccessLicenseNumber')
FreightDBEndpoint = os.getenv('FreightDBEndpoint')
AuthBasicKey = os.getenv('AuthBasicKey')
count = 0
NSkey = ''
NSResults = ''
weight = 333
bearerToken = ''





## getCode
def getCode():
    r = requests.get(getCodeURL)
    ##get and print redirect url

    f'''
    This successfully logs in as me
    import requests

    url = getCodeRedirectURL

    payload=f'email={NSUsername}%40{CompanyName}.com&password={NSPassword}'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'au_lsid_PRODUCTION=1661908429226#2ff7afea-9d39-4199-8d7f-ed9e81c87d51; NS_ROUTING_VERSION=LAGGING'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    '''
    print(r.url)
    payload = f'redirect=%2Fapp%2Flogin%2Foauth2%2Fauthorize.nl%3Fredirect_uri%3Dhttps%253A%252F%252Flocalhost%26client_id%3D61295393a2da3a6611f00951fdb0f06e4dd102228808450be54a27b729adfc4f%26response_type%3Dcode%26scope%3Drest_webservices%26state%3Dykv2XLx1BpT5Q0F3MRPHb94j%26prompt%3D%26s%3Dr%26nonce%26whence%3D&c={NSCompanyid}&email={NSUsername}%40{CompanyName}.com&password={NSPassword}&submitButton='
    # headers =
    r = requests.post(

    )
    ##redirect is a logon page after logged in as nsadmin it will redirect again and may provide a code


# getCode()


## get refresh token with bearer token
def getRefreshToken():
    url = f"https://{NSCompanyid}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"

    payload = 'code=24a4b9e49eeddced80e0a434ed1a9d0274be6a62c317409bdc3e6fbf0e632eac&redirect_uri=https%3A%2F%2Flocalhost&grant_type=authorization_code'
    headers = {
        'Authorization': f'Basic {AuthBasicKey}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def QueryUPS(weight, fromAddress, fromCity, fromState, fromZipcode, toAddress, toCity, toState, toZip):

    payload = {
        "UPSSecurity": {
            "UsernameToken": {
                "Username": f"{UPSUsername}",
                "Password": f"{UPSPassword}"
            },
            "ServiceAccessToken": {
                "AccessLicenseNumber": f"{AccessLicenseNumber}"
            }
        },
        "RateRequest": {
            "Request": {
                "RequestOption": "Rate",
                "TransactionReference": {
                    "CustomerContext": "Your Customer Context"
                }
            },
            "Shipment": {
                "Shipper": {
                    "Name": "Shipper Name",
                    "ShipperNumber": f"{UPSShippingNumber}",
                    "Address": {
                        "AddressLine": f"{fromAddress}]",
                        "City": f"{fromCity}",
                        "StateProvinceCode": f"{fromState}",
                        "PostalCode": f"{fromZipcode}",
                        "CountryCode": "US"
                    }
                },
                "ShipTo": {
                    "Name": "",
                    "Address": {
                        "AddressLine": f"{toAddress}",
                        "City": f"{toCity}",
                        "StateProvinceCode": f"{toState}",
                        "PostalCode": f"{toZip}",
                        "CountryCode": "US"
                    }
                },
                "ShipFrom": {
                    "Name": "",
                    "Address": {
                        "AddressLine": f"{fromAddress}",
                        "City": f"{fromCity}",
                        "StateProvinceCode": f"{fromState}",
                        "PostalCode": f"{fromZipcode}",
                        "CountryCode": "US"
                    }
                },
                "Service": {
                    "Code": "03",
                    "Description": "User Id and Shipper Number combinations is not qualified to receive negotaited rates/ Ground"
                },
                "ShipmentTotalWeight": {
                    "UnitOfMeasurement": {
                        "Code": "LBS",
                        "Description": "Pounds"
                    },
                    "Weight": f"{weight}"
                },
                "Package": {
                    "PackagingType": {
                        "Code": "02",
                        "Description": "Pounds"
                    },
                    "Dimensions": {
                        "UnitOfMeasurement": {
                            "Code": "IN"
                        },
                        "Length": "20",
                        "Width": "20",
                        "Height": "20"
                    },
                    "PackageWeight": {
                        "UnitOfMeasurement": {
                            "Code": "LBS"
                        },
                        "Weight": f"{weight}"
                    }
                }
            }
        }
    }

    r = requests.post('https://wwwcie.ups.com/rest/Rate', json=payload)

    data = json.loads(r.text)
    print("ups data query attempt")
    print(data['RateResponse']['RatedShipment']['TotalCharges']['MonetaryValue'])
    return(data['RateResponse']['RatedShipment']['TotalCharges']['MonetaryValue'])
# QueryUPS(weight)

##Query FreightDB for key

def queryFreightDBKey():
    url = FreightDBEndpoint
    r = requests.get(url)
    data = json.loads(r.text)
    # print(data[0]['key'])
    return data[0]['key']


NSkey = queryFreightDBKey()


## Query FreightDB for time
def queryFreightDBUpdateTime():
    url = FreightDBEndpoint
    r = requests.get(url)
    data = json.loads(r.text)
    # print(data[0]['key'])
    return data[0]['update']


## Update FreightDB

def updateFreightDB(key):
    url = FreightDBEndpoint + '/2'
    payload = {
        'key': f"{key}"
    }
    r = requests.patch(url, data=payload)

    data = json.loads(r.text)
    # print(data[0]['key'])
    print(data['key'])

# updateFreightDB()

## Query NS
def queryNS(NS_api_key,SO):
    global count
    global weight

    url = f"https://{NSCompanyid}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit=40"

    # payload = "{\r\n    \"q\": \"SELECT c.email AS email, c.companyName AS company, t.tranId AS document,t.tranDate AS date from customer c, transaction t WHERE t.entity = c.id and t.type = 'SalesOrd'\"\r\n}"
    payload = f"{{\r\n    \"q\": \"SELECT  Transaction.TranID, BUILTIN.DF ( Transaction.Type) AS Type, BUILTIN.DF( Transaction.Status) AS Status, TransactionLine.Rate AS Rates, Item.ItemID, Item.Description AS ItemDescription,Item.Weight,BUILTIN.DF( TransactionLine.Item) AS Item from transaction inner join entity on ( Entity.ID = Transaction.Entity) inner join TransactionLine ON (TransactionLine.Transaction = Transaction.ID) inner join Item on (Item.ID = TransactionLine.Item) WHERE (transaction.TranID = '{SO.get()}')\"\r\n}}"
    # Currently using SO349903 as SO for input as example.
    # payload = "{\r\n    \"q\": \"SELECT * from CUSTOMLIST_MATRIX_LENGTH \"\r\n}"
    # payload = "{\r\n    \"q\": \"SELECT * from Item where Item.ItemID = '393124'  \"\r\n}"
    # payload = "{\r\n    \"q\": \"SELECT  * from transaction inner join entity on ( Entity.ID = Transaction.Entity) inner join TransactionLine ON (TransactionLine.Transaction = Transaction.ID) inner join Item on (Item.ID = TransactionLine.Item) WHERE (transaction.TranID = 'SO349903')\"\r\n}"

    headers = {
        'Prefer': 'transient',
        'Authorization': 'Bearer ' + NS_api_key,
        'Content-Type': 'text/plain',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    r = requests.post(url, headers=headers, data=payload)
    data = json.loads(r.text)
    print(data, type(data))
    print(data["items"][0]["weight"])
    weight = data["items"][0]["weight"]
    print(int(weight))
    print(SO.get())
    return (weight)
    # if data['title'] == 'Unauthorized':
    #     return print(data['title'])


# QueryUPS(weight)

##Request New NS Token
def getNewNSKey():
    global NSkey
    url = f"https://{NSCompanyid}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"

    payload = f'grant_type=refresh_token&refresh_token={refreashToken}'
    headers = {
        'Authorization': f'Basic {AuthBasicKey}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    r = requests.request("POST", url, headers=headers, data=payload)

    print('New Token\n')
    print(r.text)
    print(r.text, type(r.text))
    NSkey = r.text.split('"')[3]
    print(NSkey)

    updateFreightDB(NSkey)
    return NSkey



# getNewNSKey()


## Test UPS URL
# https://wwwcie.ups.com/rest/Rate


# class MainApp(tk.Frame):
#     def __init__(self, master, *args, **kwargs):
#         tk.Frame.__init__(self, master, *args, **kwargs)
#         self.master = master
#         self.configure_interface()
#         self.create_widgets()
#
#     def configure_interface(self):
#         self.master.title('Freight Rate Calculator')
#         self.master.geometry('350x150')
#         self.master.resizable(False, False)
#         self.master.config(background='#626a77')
#
#
#
#     def create_widgets(self):
#         submit_button = tk.Button(self.master, text='Submit', command=queryFreightDB)
#         submit_button.place(x=150, y=100)
#
#         SO_Label = tk.Label(self.master, text='SO Number:', bg='#626a77')
#         SO_Label.place(x=20, y=29)
#
#         SO_input = tk.Entry(self.master)
#         SO_input.place(x=100, y=30, width=100)
#
#         Location_Label = tk.Label(self.master, text='Location:', bg='#626a77')
#         Location_Label.place(x=35, y=59)
#
#         Location_ComboBox = ttk.Combobox(self.master, textvariable='selected_printer',
#                                          values=['Lake Bluff', 'New York'], width=35, state='readonly')
#         Location_ComboBox.place(x=100, y=60, width=100)


## workSpace.

def date_diff_in_Seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds





class MainApp(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.configure_interface()
        self.create_widgets()

    def SubmitTask(self, SO, location, address, city, state, zip):
        global NSkey
        global weight
        fromAddress = ''
        fromCity = ''
        fromState= ''
        fromZip =''
        # print(location.get())

        if(location.get() == "New York"):
            fromAddress= os.getenv("fromAddress1")
            fromCity= os.getenv("fromCity1")
            fromState= os.getenv("fromState1")
            fromZip= os.getenv("fromZip1")

        elif(location.get() == "Lake Bluff"):
            fromAddress = os.getenv("fromAddress2")
            fromCity = os.getenv("fromCity2")
            fromState = os.getenv("fromState2")
            fromZip = os.getenv("fromZip2")

        # updateFreightDB()
        currentTime = str(datetime.now(timezone.utc)).split('.')[0]
        # print(currentTime,type(currentTime))
        currentTime_obj = datetime.strptime(currentTime, '%Y-%m-%d %H:%M:%S')
        # print(currentTime_obj, type(currentTime_obj))

        print('break')
        updatedKeyTime = queryFreightDBUpdateTime().replace('T', ' ').split('.')[0]
        # print(updatedKeyTime,type(updatedKeyTime))

        updatedKeyTime_obj = datetime.strptime(updatedKeyTime, '%Y-%m-%d %H:%M:%S')
        # print(updatedKeyTime_obj, type(updatedKeyTime_obj))

        diff = int("\n%d" % (date_diff_in_Seconds(updatedKeyTime_obj, currentTime_obj)))
        print(diff, type(diff))
        if (abs(diff) <= 3000):
            print('Good key')
            print(NSkey)
            queryNS(NSkey, SO)

            r =QueryUPS(weight, fromAddress, fromCity, fromState, fromZip, str(address.get()), str(city.get()),str(state.get()),str(zip.get()))
            Output_Label.configure(text = '$'+r)
            # NSResults = "results with good init key"
        else:
            print('Need new key')
            NSkey = getNewNSKey()
            print(NSkey)
            queryNS(NSkey, SO)
            QueryUPS(weight, fromAddress, fromCity, fromState,fromZip)
            # queryNS()
            # NSResults = "results with new key"

    def configure_interface(self):
        self.master.title('Freight Rate Calculator')
        self.master.geometry('550x150')
        self.master.resizable(False, False)
        self.master.config(background='#626a77')

    def create_widgets(self):
        global Output_Label
        submit_button = tk.Button(self.master, text='Submit', command=lambda: self.SubmitTask(SO_input, Location_ComboBox, toAddress_input,toCity_input,toState_input,toZip_input))
        submit_button.place(x=400, y=115)

        SO_Label = tk.Label(self.master, text='SO Number:', bg='#626a77')
        SO_Label.place(x=20, y=29)

        SO_input = tk.Entry(self.master)
        SO_input.place(x=100, y=30, width=100)

        Location_Label = tk.Label(self.master, text='Location:', bg='#626a77')
        Location_Label.place(x=35, y=59)

        Location_ComboBox = ttk.Combobox(self.master, textvariable='selected_printer',
                                         values=['Lake Bluff', 'New York'], width=35, state='readonly')
        Location_ComboBox.place(x=100, y=60, width=100)
        Location_ComboBox.current(0)

        results_Label = tk.Label(self.master, text='results:', bg='#626a77')
        results_Label.place(x=400, y=29)

        toAddress_Label = tk.Label(self.master, text='Address:', bg='#626a77')
        toAddress_Label.place(x=220, y=29)
        toAddress_input = tk.Entry(self.master)
        toAddress_input.place(x=270, y=30, width=100)

        toCity_Label = tk.Label(self.master, text='City:', bg='#626a77')
        toCity_Label.place(x=220, y=59)
        toCity_input = tk.Entry(self.master)
        toCity_input.place(x=270, y=60, width=100)

        toState_Label = tk.Label(self.master, text='State:', bg='#626a77')
        toState_Label.place(x=220, y=89)

        toState_input = tk.Entry(self.master)
        toState_input.place(x=270, y=90, width=100)

        toZip_Label = tk.Label(self.master, text='ZipCode:', bg='#626a77')
        toZip_Label.place(x=220, y=119)

        toZip_input = tk.Entry(self.master)
        toZip_input.place(x=270, y=120, width=100)

        Output_Label = tk.Label(self.master, text='$ ', bg='#626a77')
        Output_Label.place(x=440, y=29)


if __name__ == '__main__':
    root = tk.Tk()
    MainApp(root)
    # at.start(MainApp(root).callKey())
    root.mainloop()


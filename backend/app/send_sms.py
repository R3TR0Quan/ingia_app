import africastalking
import sqlite3

# Initialize Africa's Talking
username = 'moconnect-shortcode-ordering-app'
api_key = '95a517f3cdffdbd685d3a6c6fc23cffa07b278fdcf519dd1975ef3144fcec8aa'

africastalking.initialize(username, api_key)

# #connect to users.db
# conn = sqlite3.connect('data.db')
# cursor = conn.cursor()

# #pull destination, phone_no, vehicle_no, time from the visits table of the  database
# cursor.execute("SELECT visitor_destination, phone, visit_time FROM Visits")
# result = cursor.fetchall()

# destination = result[0][0]
# phone_no = result[0][1]
# # vehicle_no = result[0][]
# time = result[0][2]
# print(f"{phone_no}")

# send sms
class send_sms():

    sms = africastalking.SMS

    def sending(self, visitor_name, visitor_destination, visitor_phone, visit_time):
        # Connect to the SQLite database
        conn = sqlite3.connect('shipping.db')
        cursor = conn.cursor()

        #TODO: Send message
        recipients = [visitor_phone]

        message = f"Welcome kind visitor, {visitor_name}.\n You are authorized to enter the premises.\nDestination:{visitor_destination},\nPhone_No:{visitor_phone}\nVehicle_No:X\nTime:{visit_time}"
    
        #sender ID or shortcode
        sender = "33276"

        try:

            response = self.sms.send(message, recipients)
            print (response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')
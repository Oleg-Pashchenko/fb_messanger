import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('vitalik-418717-545018ff6fcd.json', scope)
client = gspread.authorize(credentials)

sheet = client.open('Facebook Autoposting')
accounts = sheet.worksheet('Accounts')
groups = sheet.worksheet('Groups')
banners = sheet.worksheet('Banners')


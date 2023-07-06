import requests

# Get

list_of_users = [
  {
    'username': 'Arlene',
    'firstname': 'Nadia',
    'middlename': 'Frazier',
    'lastname': 'Whitfield',
    'email': 'frazierwhitfield@imageflow.com',
    'birthdate': '2018-10-06',
    'password': 'JewellPrice'
  },
  {
    'username': 'Buckner',
    'firstname': 'Rosario',
    'middlename': 'Matthews',
    'lastname': 'Fowler',
    'email': 'matthewsfowler@imageflow.com',
    'birthdate': '2017-10-18',
    'password': 'HaydenHale'
  },
  {
    'username': 'Mayra',
    'firstname': 'Ball',
    'middlename': 'Whitney',
    'lastname': 'Battle',
    'email': 'whitneybattle@imageflow.com',
    'birthdate': '2020-05-21',
    'password': 'KelliPadilla'
  },
  {
    'username': 'Weiss',
    'firstname': 'David',
    'middlename': 'Nixon',
    'lastname': 'Ferguson',
    'email': 'nixonferguson@imageflow.com',
    'birthdate': '2020-06-05',
    'password': 'AlvarezDelaney'
  },
  {
    'username': 'Joanne',
    'firstname': 'Esperanza',
    'middlename': 'Tracy',
    'lastname': 'Rollins',
    'email': 'tracyrollins@imageflow.com',
    'birthdate': '2015-06-03',
    'password': 'BetsyGibson'
  }
]

login_info = [
  {
    'username': 'Buckner',
    'password': 'HaydenHale',
    'ipaddress': '142.143.22.55'
  },
  {
    'username': 'Mayra',
    'password': 'KelliPadilla',
    'ipaddress': '142.143.22.55'
  },
  {
    'username': 'Weiss',
    'password': 'AlvarezDelaney',
    'ipaddress': '142.143.22.55'
  }
]

for a in list_of_users:
    requests.post("http://localhost:5000/user/insert", json=a)

for a in list_of_users:
    requests.post("http://localhost:5000/user/insert", json=a)

r = requests.get("http://localhost:5000/user/list")
data = r.json()
print(str(data))

for a in login_info:
  requests.post("http://localhost:5000/login", json=a)


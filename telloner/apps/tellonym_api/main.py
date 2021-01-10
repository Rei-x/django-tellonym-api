from tellonym import Tellonym as client
from time import sleep


token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjU0MzIwODMsImlhdCI6MTYwOTg3MjMzMn0.Phw72nnhx5QuUGfUrQ1n3u5vCEBCDwUOcZ1nGrpKZJc"
try:
    piesek = client.Tellonym("test_account_1", "123456", auth=token)
    print(piesek.auth)
except KeyError as err:
    print(f"Prawdopodobnie za często się logowałeś. \nKod błędu: {err}")
for tells in piesek.get_tells():
    print(tells.tell)

print(piesek.get_user('spotted_zsoketrzyn', exact_match=True))
sleep(1)


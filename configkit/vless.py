edited = []
num = 80

#vless://uuid@add.com:443?security=tls&encryption=none&headerType=none&type=tcp&sni=sni#Tag
#vless://uuid@add.com:80?security=none&encryption=none&host=host&type=ws#tag
#vless://uuid@add.com:80?security=none&encryption=none&host=host&type=ws#tag%23%C4%91h
def edit(link, set_uuid=None, set_sni=None, set_tag=None):
  global edited, num
  link = link.split('://')[1]
  uuid = link.split('@')[0]
  ip, port = link.split('@')[1].split('?')[0].split(':')
  if port == 443:
    sni, tag = link.split('sni=')[1].split('#')
  else:
    sni = link.split('host=')[1].split('&')[0]
    
  
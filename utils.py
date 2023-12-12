import base64
import json
import requests
import re
import concurrent.futures
import time
import os 

workers = os.getenv("WORKERS")

def get_links_from_response(response):
    links = []
    if any(proto in response for proto in ["vmess:", "trojan:", "vless:"]):
      links.extend(response.splitlines())
    else:
      try:
        decoded_line = base64.b64decode(response).decode('utf-8')
        links.extend(decoded_line.splitlines())
      except Exception as e:
        return {'status':'error','message': str(e)}
    return links

def get_links_from_http(response, headers):
    links = []
    for line in response.splitlines():
        try:
          x = 3
          x += 1
          if line.startswith('http'):
            sub_response = requests.get(line, headers=headers, params={"flag":"v2rayn"}, timeout=x).text
            if 'vmess://' in sub_response or 'trojan://' in sub_response or 'vless://' in sub_response:
                links.extend(sub_response.splitlines())
            else:
                decoded_line = base64.b64decode(sub_response).decode('utf-8')
                if 'vmess://' in decoded_line or 'trojan://' in decoded_line or 'vless://' in decoded_line:
                  links.extend(decoded_line.splitlines())
        except:
            pass
    return links

def get_links_from_https(response, headers, proxy):
    links = []
    x = 2
    def process_url(url):
        nonlocal x
        x += 1
        try:
            sub_response = requests.get(url, headers=headers, params={"flag":"v2rayn"}, timeout=x)
            if sub_response.status_code != 200:
              sub_response = requests.get(workers, headers=headers, params={"url": url}, timeout=x)
            sub_response = sub_response.text
            if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
                links.extend(sub_response.splitlines())
            else:
                decoded_line = base64.b64decode(sub_response).decode('utf-8')
                if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
                  links.extend(decoded_line.splitlines())
        except:
            pass
    def proxy_process(url):
        nonlocal x
        x += 1
        try:
            sub_response = requests.get(workers, headers=headers, params={"url": url}, timeout=x).text
            if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
                links.extend(sub_response.splitlines())
            else:
                decoded_line = base64.b64decode(sub_response).decode('utf-8')
                if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
                  links.extend(decoded_line.splitlines())
        except:
            pass
    if proxy == "true":
      with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(proxy_process, response.splitlines())
    else:
      with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_url, response.splitlines())
    return links

def process_links(links, uuid, sni):
    processed_links = []
    for link in links:
        prefix = ''
        if link.startswith('vmess://'):
            prefix = 'vmess://'
            link = link.replace('vmess://', '')
        elif link.startswith('trojan://'):
            prefix = 'trojan://'
            link = link.replace('trojan://', '')
        elif link.startswith('vless://'):
            prefix = 'vless://'
            link = link.replace('vless://', '')
        if prefix not in  ['trojan://', 'vless://']:
            try:
                decoded_link = base64.b64decode(link).decode('utf-8')
                processed_links.append((prefix, decoded_link))
            except:
                processed_links.append((prefix, link))
        else:
            processed_links.append((prefix, link))
    final_links = set()
    for prefix, link in processed_links:
        if prefix == 'trojan://':
            try:
                split_link = link.split('@')
                if split_link[1].split(':')[0] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    split_link[0] = uuid
                if sni:
                    split_link[1] = re.sub(r'sni=[^#]*', f'sni={sni}', split_link[1])
                final_link = '@'.join(split_link)
            except:
                final_link = link
        elif prefix == 'vless://':
            try:
                split_link = link.split('@')
                if split_link[1].split(':')[0] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    split_link[0] = uuid
                if sni:
                    if 'host=' in split_link[1]:
                      split_link[1] = re.sub(r'host=[^#]*', f'host={sni}', split_link[1])
                    else:
                      split_link[1] = re.sub(r'sni=[^#]*', f'sni={sni}', split_link[1])
                final_link = '@'.join(split_link)
            except:
                final_link = link
        else:
            try:
                link_json = json.loads(link)
                if link_json["add"] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    link_json['id'] = uuid
                if sni:
                    link_json['sni'] = sni
                    link_json['host'] = sni
                final_link = json.dumps(link_json)
            except:
                final_link = link
        if prefix and prefix not in ['trojan://','vless://']:
            encoded_link = base64.b64encode(final_link.encode('utf-8')).decode('utf-8')
            final_link = f'{prefix}{encoded_link}'
        else:
            final_link = f'{prefix}{final_link}'
        final_links.add(final_link)
    return list(final_links)

def process_multi(links, uuid, sni):
    batch_size = 1
    final_links = set()
    for i in range(0, len(links), batch_size):
        batch = links[i:i + batch_size]
        process_batch(batch, uuid, sni, final_links)
    return list(final_links)

def process_batch(batch, uuid, sni, final_links):
    processed_batch = []
    for link in batch:
        prefix = ''
        if link.startswith('vmess://'):
            prefix = 'vmess://'
            link = link.replace('vmess://', '')
        elif link.startswith('trojan://'):
            prefix = 'trojan://'
            link = link.replace('trojan://', '')
        elif link.startswith('vless://'):
            prefix = 'vless://'
            link = link.replace('vless://', '')
        if prefix not in ['trojan://', 'vless://']:
            try:
                decoded_link = base64.b64decode(link).decode('utf-8')
                processed_batch.append((prefix, decoded_link))
            except:
                processed_batch.append((prefix, link))
        else:
            processed_batch.append((prefix, link))
    for prefix, link in processed_batch:
        if prefix == 'trojan://':
            try:
                split_link = link.split('@')
                if split_link[1].split(':')[0] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    split_link[0] = uuid
                if sni:
                    split_link[1] = re.sub(r'sni=[^#]*', f'sni={sni}', split_link[1])
                final_link = '@'.join(split_link)
            except:
                final_link = link
        elif prefix == 'vless://':
            try:
                split_link = link.split('@')
                if split_link[1].split(':')[0] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    split_link[0] = uuid
                if sni:
                    if 'host=' in split_link[1]:
                      split_link[1] = re.sub(r'host=[^#]*', f'host={sni}', split_link[1])
                    else:
                      split_link[1] = re.sub(r'sni=[^#]*', f'sni={sni}', split_link[1])
                final_link = '@'.join(split_link)
            except:
                final_link = link
        else:
            try:
                link_json = json.loads(link)
                if link_json["add"] in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
                    continue
                if uuid:
                    link_json['id'] = uuid
                if sni:
                    link_json['sni'] = sni
                    link_json['host'] = sni
                final_link = json.dumps(link_json)
            except:
                final_link = link
        if prefix and prefix not in ['trojan://', 'vless://']:
            encoded_link = base64.b64encode(final_link.encode('utf-8')).decode('utf-8')
            final_link = f'{prefix}{encoded_link}'
        else:
            final_link = f'{prefix}{final_link}'
        final_links.add(final_link)
    

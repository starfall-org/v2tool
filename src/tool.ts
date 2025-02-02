function editTrojan(
  link: string,
  setUuid?: string,
  setSni?: string,
  setTag?: string
): [string, string] | undefined {
  const url = new URL(link);
  const [uuid, hostPort] = url.username
    ? [url.username, url.hostname + ":" + url.port]
    : url.hostname.split("@");
  const ip = hostPort.split(":")[0];

  if (["127.0.0.1", "1.1.1.1", "0.0.0.0", "8.8.8.8"].includes(ip)) {
    return undefined;
  }

  if (setUuid) {
    url.username = setUuid;
  }

  if (setSni) {
    url.searchParams.set("sni", setSni);
  }

  if (setTag) {
    url.hash = setTag;
  }

  return [url.toString(), `${uuid}@${hostPort}`];
}

async function editTrojanAsync(
  link: string,
  setUuid?: string,
  setSni?: string,
  setTag?: string
): Promise<[string, string] | undefined> {
  const url = new URL(link);
  const [uuid, hostPort] = url.username
    ? [url.username, url.hostname + ":" + url.port]
    : url.hostname.split("@");
  const ip = hostPort.split(":")[0];

  if (["127.0.0.1", "1.1.1.1", "0.0.0.0", "8.8.8.8"].includes(ip)) {
    return undefined;
  }

  if (setUuid) {
    url.username = setUuid;
  }

  if (setSni) {
    url.searchParams.set("sni", setSni);
  }

  if (setTag) {
    url.hash = setTag;
  }

  return [url.toString(), `${uuid}@${hostPort}`];
}
// URL processing for Vless protocol
function editVless(
  link: string,
  setUuid?: string,
  setSni?: string,
  setTag?: string
): [string, string] | undefined {
  const url = new URL(link);
  const [uuid, hostPort] = url.username
    ? [url.username, url.hostname + ":" + url.port]
    : url.hostname.split("@");
  const ip = hostPort.split(":")[0];

  if (["127.0.0.1", "1.1.1.1", "0.0.0.0", "8.8.8.8"].includes(ip)) {
    return undefined;
  }

  if (setUuid) {
    url.username = setUuid;
  }

  if (setSni) {
    if (url.searchParams.get("type") === "tcp") {
      url.searchParams.set("sni", setSni);
    } else {
      url.searchParams.set("host", setSni);
    }
  }

  if (setTag) {
    url.hash = setTag;
  }

  return [url.toString(), `${uuid}@${hostPort}`];
}

function editVmess(
  link: string,
  setUuid?: string,
  setSni?: string,
  setTag?: string
): [string, string] | undefined {
  const code = link.split("://")[1];
  // Use this helper function for decoding
  const safeAtob = (str: string) => {
    try {
      return decodeURIComponent(escape(atob(str)));
    } catch {
      return atob(str);
    }
  };

  // Use this helper function for encoding
  const safeBtoa = (str: string) => {
    return btoa(unescape(encodeURIComponent(str)));
  };

  const config = JSON.parse(safeAtob(code));
  const netloc = `${config.id}@${config.add}:${config.port}`;
  const ip = config.add;

  if (["127.0.0.1", "1.1.1.1", "0.0.0.0", "8.8.8.8"].includes(ip)) {
    return undefined;
  }

  if (setTag) {
    config.ps = setTag;
  }

  if (setUuid) {
    config.id = setUuid;
  }

  if (setSni) {
    if (config.net === "tcp") {
      config.sni = setSni;
    } else {
      config.host = setSni;
    }
  }

  const newCode = safeBtoa(JSON.stringify(config));
  return [`vmess://${newCode}`, netloc];
}

export function processes(
  links: string[],
  uuid?: string,
  sni?: string,
  tag?: string
): string[] {
  const duplicate: string[] = [];
  const results: string[] = [];

  for (const link of links) {
    try {
      let result: [string, string] | undefined;

      if (link.startsWith("vmess://")) {
        result = editVmess(link, uuid, sni, tag);
      } else if (link.startsWith("trojan://")) {
        result = editTrojan(link, uuid, sni, tag);
      } else if (link.startsWith("vless://")) {
        result = editVless(link, uuid, sni, tag);
      } else {
        results.push(link);
        continue;
      }

      if (result && !duplicate.includes(result[1])) {
        results.push(result[0]);
        duplicate.push(result[1]);
      }
    } catch (e) {
      console.error(e);
      continue;
    }
  }

  return results;
}

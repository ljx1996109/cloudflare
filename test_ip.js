async function 整理成数组(内容) {
	var 替换后的内容 = 内容.replace(/[	"'\r\n]+/g, ',').replace(/,+/g, ',');
	if (替换后的内容.charAt(0) == ',') 替换后的内容 = 替换后的内容.slice(1);
	if (替换后的内容.charAt(替换后的内容.length - 1) == ',') 替换后的内容 = 替换后的内容.slice(0, 替换后的内容.length - 1);
	const 地址数组 = 替换后的内容.split(',');
	return 地址数组;
}

async function 生成随机IP(cnIspCode, count = 16, 指定端口 = -1) {
	const 运营商文件标识 = cnIspCode;
	const 运营商名称映射 = {
		cmcc: 'CF移动优选',
		cu: 'CF联通优选',
		ct: 'CF电信优选',
		cf: 'CF官方优选',
	};
	const cfname = 运营商名称映射[运营商文件标识] || 'CF官方优选';
	const cfport = [443, 2053, 2083, 2087, 2096, 8443];

	const api_url = 运营商文件标识 === 'cf' ? `https://addressesapi.090227.xyz/CloudFlareYes` : `https://addressesapi.090227.xyz/${运营商文件标识}`;
	
	let ipList = [];
	try {
		const res = await fetch(api_url); 
		if (res.ok) {
			const text = await res.text();
			ipList = text.split('\n').map(line => line.trim()).filter(Boolean);
		}
	} catch (e) {
        console.error(e)
    }

	if (ipList.length === 0) {
        console.log("FALLBACK TO CIDR!");
		const cidr_url = 运营商文件标识 === 'cf' ? `https://raw.githubusercontent.com/ljx1996109/cloudflare/main/cidr/CF-CIDR.txt` : `https://raw.githubusercontent.com/ljx1996109/cloudflare/main/cidr/${运营商文件标识}.txt`;
		try { 
			const res = await fetch(cidr_url); 
			const cidrList = res.ok ? await 整理成数组(await res.text()) : ['104.16.0.0/13'];
			const generateRandomIPFromCIDR = (cidr) => {
				const [baseIP, prefixLength] = cidr.split('/'), prefix = parseInt(prefixLength), hostBits = 32 - prefix;
				const ipInt = baseIP.split('.').reduce((a, p, i) => a | (parseInt(p) << (24 - i * 8)), 0);
				const randomOffset = Math.floor(Math.random() * Math.pow(2, hostBits));
				const mask = (0xFFFFFFFF << hostBits) >>> 0, randomIP = (((ipInt & mask) >>> 0) + randomOffset) >>> 0;
				return [(randomIP >>> 24) & 0xFF, (randomIP >>> 16) & 0xFF, (randomIP >>> 8) & 0xFF, randomIP & 0xFF].join('.');
			};
			ipList = Array.from({ length: Math.max(count, 50) }, () => generateRandomIPFromCIDR(cidrList[Math.floor(Math.random() * cidrList.length)]));
		} catch { ipList = ['104.16.1.1', '104.16.2.2']; }
	}

	ipList = ipList.sort(() => Math.random() - 0.5).slice(0, count);

	const randomIPs = ipList.map((item, index) => {
		let ip = item;
		if (ip.includes('#')) ip = ip.split('#')[0];
		
		const 目标端口 = 指定端口 === -1 ? cfport[Math.floor(Math.random() * cfport.length)] : 指定端口;
		
		let hasPort = false;
		if (ip.startsWith('[')) {
			hasPort = /\]:\d+$/.test(ip);
		} else {
			const colonIndex = ip.lastIndexOf(':');
			hasPort = colonIndex > -1 && /^\d+$/.test(ip.substring(colonIndex + 1));
			if (colonIndex > -1 && !hasPort && !ip.startsWith('[')) {
				ip = `[${ip}]`;
			}
		}

		if (hasPort) {
			return `${ip}#${cfname}${index + 1}`;
		} else {
			return `${ip}:${目标端口}#${cfname}${index + 1}`;
		}
	});

	return [randomIPs, randomIPs.join('\n')];
}

(async () => {
    console.log(await 生成随机IP('ct', 5));
})();

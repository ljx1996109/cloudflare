async function 整理成数组(内容) {
	var 替换后的内容 = 内容.replace(/[\t"'\r\n]+/g, ',').replace(/,+/g, ',');
	if (替换后的内容.charAt(0) == ',') 替换后的内容 = 替换后的内容.slice(1);
	if (替换后的内容.charAt(替换后的内容.length - 1) == ',') 替换后的内容 = 替换后的内容.slice(0, 替换后的内容.length - 1);
	const 地址数组 = 替换后的内容.split(',');
	return 地址数组;
}

async function test() {
    let customIPs = "1.1.1.1\n2.2.2.2\n3.3.3.3:443#Name";
    let list = await 整理成数组(customIPs);
    console.log("List:", list);
    
    const regex = /^(\[[\da-fA-F:]+\]|[\d.]+|[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*)(?::(\d+))?(?:#(.+))?$/;
    let mapped = list.map(item => {
        const match = item.match(regex);
        if (match) return match[1] + ":" + (match[2]||"443");
        return null;
    });
    console.log("Mapped:", mapped);
}
test();

import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_func = """async function 自动优选最佳IP(env, config_JSON, request) {
	try {
		let 完整优选列表 = [];
		const req = request || {url: 'http://localhost'};
		const baseReqUrl = req.url.split('?')[0] + '?';
		const port = -1; // 随机端口
		
		// 自动获取三大运营商各20个
		完整优选列表.push(...(await 生成随机IP(new Request(baseReqUrl + '&cnIspCode=ct'), 20, port))[0]);
		完整优选列表.push(...(await 生成随机IP(new Request(baseReqUrl + '&cnIspCode=cu'), 20, port))[0]);
		完整优选列表.push(...(await 生成随机IP(new Request(baseReqUrl + '&cnIspCode=cmcc'), 20, port))[0]);
		
		if (完整优选列表.length === 0) {
			完整优选列表.push(...(await 生成随机IP(new Request(baseReqUrl + '&cnIspCode=cf'), 60, port))[0]);
		}
		
		const top60 = 完整优选列表.join('\\n');
		await env.KV.put('ADD.txt', top60);
		
		if (config_JSON && config_JSON.优选订阅生成) {
			config_JSON.优选订阅生成.local = true;
			if (config_JSON.优选订阅生成.本地IP库) {
				config_JSON.优选订阅生成.本地IP库.随机IP = false;
				config_JSON.优选订阅生成.本地IP库.使用自定义IP = true; // 强制启用自定义
			}
			await env.KV.put('config.json', JSON.stringify(config_JSON, null, 2));
		}
	} catch (e) {
		console.error('自动优选IP失败:', e);
	}
}"""

# Using regex to replace the old function block
pattern = re.compile(r"async function 自动优选最佳IP\(env, config_JSON, request\) \{.*?\}(?=\n$|$)", re.DOTALL)
code = pattern.sub(new_func, code)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(code)

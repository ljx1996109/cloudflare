import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_endpoint = """						} else if (区分大小写访问路径 === 'admin/get-ips') {
							try {
								const endpoints = ['CloudFlareYes', 'ct', 'cu', 'cmcc'];
								let allIps = [];
								for (const ep of endpoints) {
									try {
										const r = await fetch('https://addressesapi.090227.xyz/' + ep);
										if (r.ok) {
											const text = await r.text();
											allIps.push(...text.split('\\n').map(l => l.trim()).filter(Boolean));
										}
									} catch (e) {}
								}
								allIps = [...new Set(allIps)];
								return new Response(allIps.join('\\n'), { status: 200, headers: { 'Content-Type': 'text/plain;charset=utf-8' } });
							} catch (error) {
								return new Response('Error', { status: 500, headers: { 'Content-Type': 'text/plain;charset=utf-8' } });
							}
"""

code = code.replace("						} else if (区分大小写访问路径 === 'admin/ADD.txt') { // 保存自定义优选IP",
                    new_endpoint + "						} else if (区分大小写访问路径 === 'admin/ADD.txt') { // 保存自定义优选IP")

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(code)

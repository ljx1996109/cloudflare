import re
with open('pages/admin.html', 'r', encoding='utf-8') as f:
    code = f.read()

new_logic = """				// 2. 从后端中转接口拉取全量 IP
				const r = await fetch('/admin/get-ips', { method: 'POST' });
				if (!r.ok) {
					showToast('获取源 IP 失败，请检查网络', 'error');
					return;
				}
				const allIpsStr = await r.text();
				let allIps = allIpsStr.split('\\n').map(l => l.trim()).filter(Boolean);
				allIps = [...new Set(allIps)];
				
				if (allIps.length === 0) {
					showToast('获取源 IP 为空', 'error');
					return;
				}"""

pattern = re.compile(r"// 2\. 从 API 聚合拉取近 500 个 IP.*?if \(allIps\.length === 0\) \{\n[^\n]*\n[^\n]*\n\t\t\t\t\}", re.DOTALL)
code = pattern.sub(new_logic, code)

with open('pages/admin.html', 'w', encoding='utf-8') as f:
    f.write(code)

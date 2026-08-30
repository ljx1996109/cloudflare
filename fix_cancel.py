import re

def remove_function(code, func_name):
    # Find all occurrences of "function func_name"
    pattern = f"function {func_name}\\s*\\("
    while True:
        match = re.search(pattern, code)
        if not match:
            break
        
        start_idx = match.start()
        
        # Find the opening brace
        brace_start = code.find('{', start_idx)
        if brace_start == -1:
            break
            
        # Find the matching closing brace
        brace_count = 1
        end_idx = brace_start + 1
        while brace_count > 0 and end_idx < len(code):
            if code[end_idx] == '{':
                brace_count += 1
            elif code[end_idx] == '}':
                brace_count -= 1
            end_idx += 1
            
        if brace_count == 0:
            code = code[:start_idx] + code[end_idx:]
        else:
            break # Unbalanced
    return code

with open('pages/admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Clean up all cancelEdit functions
html = remove_function(html, 'cancelEdit')

# Now insert the correct cancelEdit function right before function showECHHelpModal()
correct_cancel_edit = """
		function cancelEdit(section) {
			if (section === 'notification') {
				const telegramCheckbox = document.getElementById('telegramEnabled');
				const originalEnabled = originalConfig.TG?.启用 ?? false;
				telegramCheckbox.checked = originalEnabled;
				currentConfig.TG.启用 = originalEnabled;
			} else {
				currentConfig = JSON.parse(JSON.stringify(originalConfig));

				if (section === 'sub') {
					if (currentConfig.优选订阅生成 && currentConfig.优选订阅生成.本地IP库) {
						const isCustom = !!currentConfig.优选订阅生成.本地IP库.使用自定义IP;
						const toggleEl = document.getElementById('useCustomIPsToggle');
						if (toggleEl) {
							toggleEl.checked = isCustom;
							toggleCustomIPs();
						}
						document.getElementById('ctCount').value = currentConfig.优选订阅生成.本地IP库.CT !== undefined ? currentConfig.优选订阅生成.本地IP库.CT : 20;
						document.getElementById('cuCount').value = currentConfig.优选订阅生成.本地IP库.CU !== undefined ? currentConfig.优选订阅生成.本地IP库.CU : 20;
						document.getElementById('cmccCount').value = currentConfig.优选订阅生成.本地IP库.CMCC !== undefined ? currentConfig.优选订阅生成.本地IP库.CMCC : 20;
						document.getElementById('specifiedPort').value = currentConfig.优选订阅生成.本地IP库.指定端口 !== undefined ? currentConfig.优选订阅生成.本地IP库.指定端口 : -1;
					}
				} else if (section === 'config') {
					document.getElementById('subName').value = currentConfig.优选订阅生成?.SUBNAME || '';
					document.getElementById('nodeHost').value = currentConfig.HOST || '';
					document.getElementById('nodeUUID').value = currentConfig.UUID || '';
					document.getElementById('nodePATH').value = currentConfig.PATH || '';
					document.getElementById('protocol').value = currentConfig.协议类型 || 'VLESS';
				} else if (section === 'convert') {
					if (currentConfig.订阅转换配置) {
						if (currentConfig.订阅转换配置.SUBLIST !== undefined) document.getElementById('subList').checked = currentConfig.订阅转换配置.SUBLIST;
						if (currentConfig.订阅转换配置.UDP !== undefined) document.getElementById('udp').checked = currentConfig.订阅转换配置.UDP;
						if (currentConfig.订阅转换配置.XUDP !== undefined) document.getElementById('xudp').checked = currentConfig.订阅转换配置.XUDP;
						if (currentConfig.订阅转换配置.TLS13 !== undefined) document.getElementById('tls13').checked = currentConfig.订阅转换配置.TLS13;
						if (currentConfig.订阅转换配置.APPEND_TYPE !== undefined) document.getElementById('appendType').checked = currentConfig.订阅转换配置.APPEND_TYPE;
						if (currentConfig.订阅转换配置.SORT !== undefined) document.getElementById('sort').checked = currentConfig.订阅转换配置.SORT;
					}
				}
			}
			
			// 只重置DOM中的按钮，不调用 renderUI 以保持展开状态
			document.querySelectorAll(`.panel[data-section="${section}"] .btn-group .btn.success`).forEach(btn => btn.style.display = 'none');
			document.querySelectorAll(`.panel[data-section="${section}"] .btn-group .btn.secondary`).forEach(btn => btn.style.display = 'none');
			document.querySelectorAll(`.panel[data-section="${section}"] .btn-group .btn:not(.success):not(.secondary)`).forEach(btn => btn.style.display = 'inline-flex');
		}
"""

html = html.replace('function showECHHelpModal()', correct_cancel_edit + '\n\t\tfunction showECHHelpModal()')

with open('pages/admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

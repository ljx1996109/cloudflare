const fs = require('fs');
const html = fs.readFileSync('pages/admin.html', 'utf8');
const scriptRegex = /<script>([\s\S]*?)<\/script>/g;
let match;
let i = 1;
while ((match = scriptRegex.exec(html)) !== null) {
    try {
        new Function(match[1]);
        console.log(`Script ${i} is valid.`);
    } catch (e) {
        console.error(`Script ${i} syntax error:`, e.message);
    }
    i++;
}

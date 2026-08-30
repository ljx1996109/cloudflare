const { JSDOM } = require("jsdom");
const dom = new JSDOM(`<button id="btn">Click me</button>`);
const btn = dom.window.document.getElementById('btn');
btn.addEventListener('click', async () => {
    throw new Error('Sync error inside async listener');
});
try {
    btn.click();
    console.log("click() DID NOT throw");
} catch (e) {
    console.log("click() THREW:", e.message);
}

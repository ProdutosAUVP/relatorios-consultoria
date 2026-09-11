import { chromium } from 'playwright';
import { readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
function fc(){const b=process.env.PLAYWRIGHT_BROWSERS_PATH;if(!b||!existsSync(b))return undefined;
for(const d of readdirSync(b).filter(x=>x.startsWith('chromium-')).sort().reverse()){const e=join(b,d,'chrome-linux','chrome');if(existsSync(e))return e;}}
let br;try{br=await chromium.launch();}catch(e){br=await chromium.launch({executablePath:fc()});}
const pg=await br.newPage({viewportSize:{width:1400,height:800},deviceScaleFactor:2});
await pg.goto('file://'+process.argv[2]);await pg.waitForTimeout(400);
const s=await pg.$$('.page,.slide');
for(const i of process.argv[4].split(',').map(Number)) await s[i-1].screenshot({path:`${process.argv[3]}/s${i}.png`});
await br.close();

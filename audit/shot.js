const { chromium } = require('playwright');
(async () => {
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch({ proxy: proxy ? { server: proxy } : undefined, args: ['--ignore-certificate-errors'] });
  const targets = JSON.parse(process.argv[2]);
  for (const t of targets) {
    for (const vp of [{name:'mobile', width:390, height:844, mobile:true}, {name:'desktop', width:1440, height:900, mobile:false}]) {
      const ctx = await browser.newContext({ viewport:{width:vp.width,height:vp.height}, isMobile: vp.mobile, deviceScaleFactor: vp.mobile?2:1, ignoreHTTPSErrors: true, userAgent: vp.mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 audit-RCprints' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36 audit-RCprints', locale:'de-CH' });
      const page = await ctx.newPage();
      let bytes=0, reqs=0, byType={};
      page.on('response', async r => { try { const h=r.headers(); const l=parseInt(h['content-length']||'0'); const ct=(h['content-type']||'').split(';')[0]; reqs++; bytes+=l; byType[ct]=(byType[ct]||0)+l; } catch(e){} });
      await page.addInitScript(() => {
        window.__lcp=0; window.__cls=0;
        new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.renderTime||e.loadTime; }).observe({type:'largest-contentful-paint', buffered:true});
        new PerformanceObserver(l => { for (const e of l.getEntries()) if(!e.hadRecentInput) window.__cls += e.value; }).observe({type:'layout-shift', buffered:true});
      });
      const t0=Date.now();
      try { await page.goto(t.url, { waitUntil: 'networkidle', timeout: 60000 }); } catch(e) { console.log('goto warn', t.name, vp.name, e.message.slice(0,80)); }
      await page.waitForTimeout(1500);
      const m = await page.evaluate(() => { const nav=performance.getEntriesByType('navigation')[0]||{}; const res=performance.getEntriesByType('resource'); const tb=res.reduce((a,r)=>a+(r.transferSize||0),0); const imgs=[...document.images].map(i=>({w:i.naturalWidth,h:i.naturalHeight,dw:i.clientWidth,dh:i.clientHeight,src:(i.currentSrc||i.src).slice(-60),alt:i.alt})); const small=[...document.querySelectorAll('a,button,input,select')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.width<44||r.height<44)&&r.top<window.innerHeight*3;}).length; return { lcp: Math.round(window.__lcp), cls: +window.__cls.toFixed(3), domContentLoaded: Math.round(nav.domContentLoadedEventEnd||0), load: Math.round(nav.loadEventEnd||0), resources: res.length, transferKB: Math.round(tb/1024), scrollH: document.documentElement.scrollHeight, imgs: imgs.length, oversizedImgs: imgs.filter(i=>i.dw>0&&i.w>i.dw*2.2).length, smallTapTargets: small, title: document.title, fonts: [...document.fonts].map(f=>f.family).filter((v,i,a)=>a.indexOf(v)===i), hasStickyATC: !!document.querySelector('[class*="sticky"] button[name="add"], .sticky-atc, [class*="sticky-add"]'), cookieBanner: !!document.querySelector('#shopify-pc__banner, [class*="cookie"], [id*="cookie"], [class*="consent"]'), h1: [...document.querySelectorAll('h1')].map(h=>h.innerText.trim()).slice(0,3), atcText: (document.querySelector('button[name="add"], form[action*="/cart/add"] button[type="submit"]')||{}).innerText, price: (document.querySelector('.price, [class*="price"]')||{}).innerText } });
      const file = `shots/${t.name}-${vp.name}.png`;
      await page.screenshot({ path: file, fullPage: true });
      const fold = `shots/${t.name}-${vp.name}-fold.png`;
      await page.screenshot({ path: fold, fullPage: false });
      console.log(JSON.stringify({ page:t.name, vp:vp.name, url:t.url, elapsedMs: Date.now()-t0, reqs, ...m }));
      await ctx.close();
    }
  }
  await browser.close();
})();

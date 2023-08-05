import{_ as t,s as e,e as i,t as o,$ as s,dv as n,ar as a,n as r}from"./main-ac83c92b.js";import{aG as h,aH as c,aI as l}from"./c.3e14cfd3.js";import{h as d}from"./c.027db416.js";import"./c.8cbd7110.js";const u=t=>t.reduce(((t,e)=>t+parseFloat(e.state)),0)/t.length,f=t=>parseFloat(t[t.length-1].state)||0,g=(t,e,i,o,s)=>{t.forEach((t=>{t.state=Number(t.state)})),t=t.filter((t=>!Number.isNaN(t.state)));const n=void 0!==(null==s?void 0:s.min)?s.min:Math.min(...t.map((t=>t.state))),a=void 0!==(null==s?void 0:s.max)?s.max:Math.max(...t.map((t=>t.state))),r=(new Date).getTime(),h=(t,i,o)=>{const s=r-new Date(i.last_changed).getTime();let n=Math.abs(s/36e5-e);return o?(n=60*(n-Math.floor(n)),n=Number((10*Math.round(n/10)).toString()[0])):n=Math.floor(n),t[n]||(t[n]=[]),t[n].push(i),t};if(t=t.reduce(((t,e)=>h(t,e,!1)),[]),o>1&&(t=t.map((t=>t.reduce(((t,e)=>h(t,e,!0)),[])))),t.length)return((t,e,i,o,s,n)=>{const a=[];let r=(n-s)/80;r=0!==r?r:80;let h=i/(e-(1===o?1:0));h=isFinite(h)?h:i;const c=t.filter(Boolean)[0];let l=[u(c),f(c)];const d=(t,e,i=0,o=1)=>{if(o>1&&t)return t.forEach(((t,i)=>d(t,e,i,o-1)));const n=h*(e+i/6);t&&(l=[u(t),f(t)]);const c=82.5-((t?l[0]:l[1])-s)/r;return a.push([n,c])};for(let e=0;e<t.length;e+=1)d(t[e],e,0,o);return 1===a.length&&(a[1]=[i,a[0][1]]),a.push([i,a[a.length-1][1]]),a})(t,e,i,o,n,a)};t([r("hui-graph-base")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i()],key:"coordinates",value:void 0},{kind:"field",decorators:[o()],key:"_path",value:void 0},{kind:"method",key:"render",value:function(){return s`
      ${this._path?n`<svg width="100%" height="100%" viewBox="0 0 500 100">
          <g>
            <mask id="fill">
              <path
                class='fill'
                fill='white'
                d="${this._path} L 500, 100 L 0, 100 z"
              />
            </mask>
            <rect height="100%" width="100%" id="fill-rect" fill="var(--accent-color)" mask="url(#fill)"></rect>
            <mask id="line">
              <path
                fill="none"
                stroke="var(--accent-color)"
                stroke-width="${5}"
                stroke-linecap="round"
                stroke-linejoin="round"
                d=${this._path}
              ></path>
            </mask>
            <rect height="100%" width="100%" id="rect" fill="var(--accent-color)" mask="url(#line)"></rect>
          </g>
        </svg>`:n`<svg width="100%" height="100%" viewBox="0 0 500 100"></svg>`}
    `}},{kind:"method",key:"willUpdate",value:function(t){this.coordinates&&t.has("coordinates")&&(this._path=(t=>{if(!t.length)return"";let e,i,o="",s=t.filter(Boolean)[0];o+=`M ${s[0]},${s[1]}`;for(const c of t)e=c,n=s[0],a=s[1],r=e[0],h=e[1],i=[(n-r)/2+r,(a-h)/2+h],o+=` ${i[0]},${i[1]}`,o+=` Q${e[0]},${e[1]}`,s=e;var n,a,r,h;return o+=` ${e[0]},${e[1]}`,o})(this.coordinates))}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      :host {
        display: flex;
        width: 100%;
      }
      .fill {
        opacity: 0.1;
      }
    `}}]}}),e);const _=["counter","input_number","number","sensor"];let m=t([r("hui-graph-header-footer")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.735eb1c3.js"),document.createElement("hui-graph-footer-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,e,i){return{type:"graph",entity:h(t,1,e,i,_,(t=>!isNaN(Number(t.state))&&!!t.attributes.unit_of_measurement))[0]||""}}},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"type",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"field",decorators:[o()],key:"_coordinates",value:void 0},{kind:"field",key:"_date",value:void 0},{kind:"field",key:"_stateHistory",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){if(null==t||!t.entity||!_.includes(d(t.entity)))throw new Error("Specify an entity from within the sensor domain");const e={detail:1,hours_to_show:24,...t};e.hours_to_show=Number(e.hours_to_show),e.detail=1===e.detail||2===e.detail?e.detail:1,this._config=e}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?this._coordinates?this._coordinates.length?s`
      <hui-graph-base .coordinates=${this._coordinates}></hui-graph-base>
    `:s`
        <div class="container">
          <div class="info">No state history found.</div>
        </div>
      `:s`
        <div class="container">
          <ha-circular-progress active size="small"></ha-circular-progress>
        </div>
      `:s``}},{kind:"method",key:"shouldUpdate",value:function(t){return c(this,t)}},{kind:"method",key:"updated",value:function(t){if(this._config&&this.hass&&(!this._fetching||t.has("_config")))if(t.has("_config")){const e=t.get("_config");e&&e.entity===this._config.entity||(this._stateHistory=[]),this._getCoordinates()}else Date.now()-this._date.getTime()>=6e4&&this._getCoordinates()}},{kind:"method",key:"_getCoordinates",value:async function(){var t;this._fetching=!0;const e=new Date,i=this._date&&null!==(t=this._stateHistory)&&void 0!==t&&t.length?this._date:new Date((new Date).setHours(e.getHours()-this._config.hours_to_show));if(this._stateHistory.length){const t=[],i=[];this._stateHistory.forEach((o=>(e.getTime()-new Date(o.last_changed).getTime()<=36e5*this._config.hours_to_show?t:i).push(o))),i.length&&t.push(i[i.length-1]),this._stateHistory=t}const o=await l(this.hass,this._config.entity,i,e,Boolean(this._stateHistory.length));o.length&&o[0].length&&this._stateHistory.push(...o[0]),this._coordinates=g(this._stateHistory,this._config.hours_to_show,500,this._config.detail,this._config.limits)||[],this._date=e,this._fetching=!1}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      ha-circular-progress {
        position: absolute;
        top: calc(50% - 14px);
      }
      .container {
        display: flex;
        justify-content: center;
        position: relative;
        padding-bottom: 20%;
      }
      .info {
        position: absolute;
        top: calc(50% - 16px);
        color: var(--secondary-text-color);
      }
    `}}]}}),e);export{m as HuiGraphHeaderFooter};
